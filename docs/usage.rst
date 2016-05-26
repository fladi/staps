=====
Usage
=====

staps is intende to be used as a daemon controlled by systemd. It listens for websocket connections on a unix domain socket. In order to make staps available
over network a websocket-capable reverse-proxy like nginx is required.

systemd
-------

A service unit file for systemd is included with staps. To enable this unit copy the staps.service file to /etc/systemd/system/staps.service. Then run::

  sudo systemctl enable staps.service
  sudo systemctl start staps.service

The configuration file should be placed at /etc/staps/staps.conf or ~/.staps.conf::

  [staps]
  socket = /var/run/staps/staps.sock
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
example configuration. The regex for the location block matches only UUID4 paths and is the recommended way to generate trow-away pub/sub URLs.

.. code::

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  upstream websocket {
    server unix:/run/staps.sock;
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
