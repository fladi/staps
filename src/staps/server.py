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

import logging
import uuid

import pika
from tornado import web, websocket

logger = logging.getLogger(__name__)


class PikaClient(object):

    exchange = 'staps'

    def __init__(self, io_loop, url):
        self.io_loop = io_loop
        self.param = pika.URLParameters(url)

        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

    def connect(self):
        if self.connecting:
            logger.info('PikaClient: Already connecting to RabbitMQ')
            return

        logger.info('PikaClient: Connecting to RabbitMQ')
        self.connecting = True

        self.connection = pika.adapters.TornadoConnection(
            self.param,
            on_open_callback=self.on_connected,
            on_open_error_callback=self.on_error,
            on_close_callback=self.on_closed,
            custom_ioloop=self.io_loop,
            stop_ioloop_on_close=False
        )

    def on_connected(self, connection):
        logger.info('PikaClient: connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        logger.info('PikaClient: Channel %s open, Declaring exchange', channel)
        self.channel = channel
        self.channel.exchange_declare(
            exchange=self.exchange,
            type='direct'
        )

    def on_closed(self, connection):
        logger.info('PikaClient: rabbit connection closed')
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.connect()

    def on_error(self, connection, error):
        logger.error('PikaClient: amqp connection error: {}'.format(error))
        return


class IndexHandler(web.RequestHandler):

    def get(self, path):
        self.render('index.html', path=path)


class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, pk):
        self.amqp = False
        self.backlog = []
        logger.debug('WebSocket: Incoming connection: {}'.format(pk))
        self.uuid = uuid.uuid4()
        self.pk = pk
        self.application.pc.connection.channel(self.amqp_channel_ok)

    def amqp_channel_ok(self, channel):
        logger.debug('WebSocket: Channel established: {}'.format(channel))
        self.channel = channel
        self.channel.queue_declare(
            self.amqp_queue_ok,
            exclusive=True,
            auto_delete=True
        )
        self.amqp = True
        while self.backlog:
            self.publish(self.backlog.pop())

    def amqp_queue_ok(self, queue):
        logger.debug('WebSocket: Queue declared: {}'.format(queue))
        self.queue = queue.method.queue
        self.channel.queue_bind(
            self.amqp_bind_ok,
            routing_key=self.pk,
            exchange=self.application.pc.exchange,
            queue=self.queue
        )

    def amqp_bind_ok(self, bind):
        logger.debug('WebSocket: Bind established: {}'.format(bind))
        self.channel.basic_consume(
            self.amqp_basic_consume,
            queue=self.queue,
            no_ack=True
        )

    def amqp_basic_consume(self, channel, method, properties, body):
        if (properties.correlation_id != str(self.uuid)):
            logger.debug('WebSocket: Consuming message: {}'.format(body))
            self.write_message(body)

    def on_message(self, message):
        logger.debug('WebSocket: Message received: {}'.format(message))
        if not self.amqp:
            logger.warn('WebSocket: Message backlogged: {}'.format(message))
            self.backlog.append(message)
        else:
            self.publish(message)

    def publish(self, message):
        self.channel.basic_publish(
            exchange=self.application.pc.exchange,
            routing_key=self.pk,
            body=message,
            properties=pika.BasicProperties(
                correlation_id=str(self.uuid),
            )
        )

    def on_close(self):
        logger.info('WebSocket: Connection closed: {}'.format(self.pk))
        self.channel.queue_unbind(
            self.amqp_queue_unbind,
            queue=self.queue,
            exchange=self.application.pc.exchange,
            routing_key=self.pk
        )

    def amqp_queue_unbind(self, queue):
        logger.info('WebSocket: Queue unbound: {}'.format(queue))
        self.channel.close()
