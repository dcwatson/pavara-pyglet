from .base import PhysicsObject
from pavara.geom import builder
from pavara.geom.utils import parse_vector, parse_color, parse_float
from .block import Block

class Ground (Block):

    def __init__(self, world, color):
        super(Ground, self).__init__(world, (0, -0.5, 0), (1000, 1.0, 1000), color)

def create(world, element):
    return Ground(
        world,
        parse_color(element['color'])
    )
