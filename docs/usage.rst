=====
Usage
=====

staps provides publish-subscribe channels that are meant to be temporary. They can be created by simply connecting a websocket client to an URL. Each channel is
identified by the URL path that is passed to staps. The first client to connect to a distinct path will create an anonymous pub/sub-channel. Each subsequent
client that connects to the same URL will join the channel.

All clients in a channel are equal which means each one of them can publish messages while being subscribed to messages from other clients. Messages will not be
echoed back to the client that published them.

.. graphviz:: staps.dot

staps is intended to be used as a daemon controlled by systemd. It listens for websocket connections on a unix domain socket. In order to make staps available
over network a websocket-capable reverse-proxy like nginx is required.

.. DANGER::
   There is no authentication or authorization. Everyone who knows the URL to a channel can join it and can snoop on published messages or can publish malicious
   messages themself! URLs should be treated als confidential! Do not use staps with a webbrowser!



systemd
-------

A service unit file for systemd is included with staps. To enable this unit copy the staps.service file to /etc/systemd/system/staps.service. Then run::

  sudo systemctl enable staps.service
  sudo systemctl start staps.service

The configuration file should be placed at /etc/staps/staps.conf or ~/.staps.conf::

  [staps]
  socket = /run/staps/staps.sock
  mode = 0660
  amqp = amqp://staps:@localhost/

  [daemon]
  user = staps
  group = staps
  dir = /var/lib/staps/
  pid_file = /var/run/staps/staps.pid
  umask = 0

nginx
-----

Currently only nginx is supported as a frontend for staps. To have nginx handle all websocket connections at http://example.com/<uuid4> use the following
example configuration. The regex for the location block matches only UUID4 paths and is the recommended way to generate throw-away pub/sub URLs.

.. code::

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  upstream websocket {
    server unix:/run/staps/staps.sock;
  }

  server {
    ...

    location ~* "^/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$" {
      proxy_pass http://websocket;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
    }

    ...
  }

Apache
------

While Apache should be able to act as a frontend for staps it is currnetly not possible to use mod_proxy_wstunnel with unix domain sockets.
