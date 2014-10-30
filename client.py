#!/usr/bin/env python

import pyglet
from pyglet.window import key
from pavara.vecmath import Vector3
from pavara.world import create_world, World
from pavara.objects.block import Block
from pavara.objects.ground import Ground
import random

from pavara.network.client import Client
from pavara.network.packet import *

window = pyglet.window.Window(640, 400)
world = create_world(window, 'maps/icebox-classic.xml')
client = Client('127.0.0.1', 5400)

def update(dt):
    world.tick(dt)
    client.tick(dt, world)
pyglet.clock.schedule_interval(update, 1.0 / 60.0)

@window.event
def on_draw():
    window.clear()
    world.draw()
#    print pyglet.clock.get_fps()

@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    pyglet.gl.glViewport(0, 0, width, height)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(60.0, width / float(height), .1, 1000.)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluLookAt(40, 20, 0, 0, 0, 0, 0, 1, 0)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        pass
    elif symbol == key.F:
        client.write(Packet(KIND_GAME_START, client.nextseq))
    elif symbol == key.J:
        client.write(Packet(KIND_PLAYER_JOIN, client.nextseq))
    elif symbol == key.L:
        client.write(Packet(KIND_LOAD_MAP, client.nextseq, payload=b'maps/icebox-classic.xml'))

# enable face culling, depth testing
pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)

pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)

pyglet.app.run()
