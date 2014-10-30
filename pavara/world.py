import drill
import importlib
import pyglet
from .vecmath import Vector3
import ode

from pavara.objects.ground import Ground

TIMESTEP = 1.0 / 60.0

def process_elements(world, root, context=None):
    context = context or {}
    for elem in root.children():
        if elem.tagname == 'set':
            ctx = context.copy()
            ctx.update(elem.attrs)
            process_elements(world, elem, context=ctx)
        else:
            try:
                mod = importlib.import_module('pavara.objects.%s' % elem.tagname)
                elem.attrs.update(context)
                mod.create(world, elem)
            except:
                pass

class World (object):
    window = None

    def __init__(self, window=None):
        self.window = window
        self.reset()

    def reset(self):
        self.gravity = Vector3(0, -9.8, 0)
        self.space = ode.HashSpace()
        self.objects = []
        self.t = 0.0
        self.accum = 0.0

    def add(self, obj):
        obj.index = len(self.objects)
        self.objects.append(obj)

    def tick(self, dt):
        self.accum += dt
        while self.accum >= TIMESTEP:
            for obj in self.objects:
                obj.tick(TIMESTEP)
            self.space.collide(TIMESTEP, self.check_collisions)
            self.accum -= TIMESTEP
            self.t += TIMESTEP

    def check_collisions(self, dt, geom1, geom2):
        contacts = ode.collide(geom1, geom2)
        if contacts:
            obj1 = geom1.pavara_object
            obj2 = geom2.pavara_object
            if not obj1.mass:
                return
            v1 = obj1.velocity
            v2 = obj2.velocity
            pos, norm, depth, g1, g2 = contacts[0].getContactGeomParams()
            n = Vector3(*norm)
            obj1.position += (n * depth)
            if obj2.mass:
                obj1.velocity = ((v1 * (obj1.mass - obj2.mass)) + (v2 * (2 * obj2.mass))) / (obj1.mass + obj2.mass)
                obj2.velocity = ((v2 * (obj2.mass - obj1.mass)) + (v1 * (2 * obj1.mass))) / (obj1.mass + obj2.mass)
            else:
                proj = n * v1.dot(n)
                obj1.velocity -= proj
            #self.corrections.extend(obj1.corrections(contacts, obj2))

    def draw(self):
        batch = pyglet.graphics.Batch()
        for obj in self.objects:
            obj.draw(batch)
        batch.draw()

    def load(self, map_name):
        root = drill.parse(map_name)
        process_elements(self, root)


def create_world(window, map_name):
    world = World(window)
    root = drill.parse(map_name)
    process_elements(world, root)
    return world
