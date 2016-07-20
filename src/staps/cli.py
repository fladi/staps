#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016, OpenServices e.U.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Standard Library
import logging

from cement.core.controller import CementBaseController
from cement.core.controller import expose
from cement.core.foundation import CementApp

# Staps
from staps.server import IndexHandler
from staps.server import PikaClient
from staps.server import SocketHandler


class DaemonController(CementBaseController):
    class Meta:
        label = 'base'
        arguments = [
            (['--mode'], dict(help='Set permissions on socket')),
            (['--amqp'], dict(help='AMQP connection URL')),
            (['--socket'], dict(nargs='*', help='Unix domain socket paths')),
            (['--port'], dict(nargs='*', help='Unix domain socket paths')),
        ]
        config_defaults = dict(
            mode='0o600',
            amqp='amqp://staps:@localhost/',
            socket=['/var/run/staps/staps.sock'],
            port=[],
        )

    @expose(hide=True)
    def default(self):
        from tornado import web, ioloop
        from tornado.netutil import bind_unix_socket, bind_sockets
        from tornado.httpserver import HTTPServer

        self.app.daemonize()

        logging.basicConfig(level=self.app.log.backend.level)

        application = web.Application([
            (r'/(.*)', IndexHandler),
            (r'/(.*)', SocketHandler),
        ])

        server = HTTPServer(application)
        for endpoint in self.app.config.get('controller.base', 'socket'):
            self.app.log.info('Listening on socket {}.'.format(endpoint))
            socket = bind_unix_socket(
                endpoint,
                mode=int(self.app.config.get('controller.base', 'mode'), 8)
            )
            server.add_socket(socket)

        for endpoint in self.app.config.get('controller.base', 'port'):
            self.app.log.info('Listening on {}.'.format(endpoint))
            sockets = bind_sockets(endpoint)
            server.add_sockets(sockets)

        io_loop = ioloop.IOLoop.instance()

        # PikaClient is our rabbitmq consumer
        application.pc = PikaClient(
            io_loop,
            self.app.config.get('controller.base', 'amqp')
        )
        application.pc.connect()

        self.app.log.debug('Starting tornado IO loop.')
        try:
            io_loop.start()
        except KeyboardInterrupt:
            io_loop.stop()


class Application(CementApp):
    class Meta:
        label = 'staps'
        arguments_override_config = True
        base_controller = DaemonController
        extensions = ['daemon', 'colorlog']
        log_handler = 'colorlog'
