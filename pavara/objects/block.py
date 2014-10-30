from .base import PhysicsObject
from pavara.geom import builder
from pavara.geom.base import Collision
from pavara.geom.utils import parse_vector, parse_color, parse_float
from pavara.vecmath import Point3, Vector3
import ode

class Block (PhysicsObject):

    def __init__(self, world, position, size, color, mass=0):
        super(Block, self).__init__(world, position, mass)
        self.geom = builder.block(color, size)
        self.shape = ode.GeomBox(world.space, lengths=size)
        self.shape.pavara_object = self
        self.moveto(*position)

def create(world, element):
    return Block(
        world,
        parse_vector(element['center']),
        parse_vector(element['size']),
        parse_color(element['color']),
        mass=parse_float(element['mass'])
    )
