#!/usr/bin/env python

from pavara.network.server import Server
import pyglet

server = Server(5400)

def update(dt):
    server.tick(dt)
pyglet.clock.schedule_interval(update, 1.0 / 30.0)

pyglet.app.run()
