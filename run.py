#!/usr/bin/env python

import pyglet
from pyglet.window import key
from pavara.vecmath import Vector3
from pavara.world import create_world, World
from pavara.objects.block import Block
from pavara.objects.ground import Ground
import random

pyglet.options['debug_gl'] = False

window = pyglet.window.Window(1280, 800)
#world = create_world(window, 'maps/icebox-classic.xml')

world = World(window)
ground = Ground(world, (0.6, 0.6, 1, 1))
platform = Block(world, (0, 4, 0), (6, 1, 6), (1, 0, 0, 1))
platform.rotate(45, 0, 0)
block = Block(world, (0, 10, 0), (2, 2, 2), (0, 0, 1, 1), mass=10)

#center = Block(world, (0, 1, 0), (2, 2, 2), (1, 0, 0, 1))
#slider = Block(world, (7, 1, 5), (2, 2, 2), (0, 0, 1, 1), mass=10)

def update(dt):
    world.tick(dt)
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
    if symbol == key.F:
        for o in world.objects:
            if o.mass:
                x = random.uniform(-1.0, 1.0) * 10.0
                y = random.random() * 10.0
                z = random.uniform(-1.0, 1.0) * 10.0
                o.apply_force(Vector3(x, y, z))
        #world.objects[25].apply_force(Vector3(-10.0, 10.0, -1.0))
        #slider.apply_force(Vector3(-3, 0, -3))

# enable face culling, depth testing
pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)

def vec(*args):
    return (pyglet.gl.GLfloat * len(args))(*args)

# lighting
#pyglet.gl.glEnable(pyglet.gl.GL_LIGHTING)
#pyglet.gl.glEnable(pyglet.gl.GL_LIGHT0)
#pyglet.gl.glLightfv(pyglet.gl.GL_LIGHT0, pyglet.gl.GL_POSITION, vec(.5, .5, 1, 0))
#pyglet.gl.glLightfv(pyglet.gl.GL_LIGHT0, pyglet.gl.GL_SPECULAR, vec(.5, .5, 1, 1))
#pyglet.gl.glLightfv(pyglet.gl.GL_LIGHT0, pyglet.gl.GL_DIFFUSE, vec(1, 1, 1, 1))

pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)

pyglet.app.run()
