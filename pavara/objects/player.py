from .base import PhysicsObject
from pavara.geom import builder

class Player (PhysicsObject):
    def __init__(self, world, name):
        super(Player, self).__init__(world, (0, 0, 0), 0)
        self.geom = builder.block(color, size)
        self.shape = ode.GeomBox(world.space, lengths=size)
        self.shape.pavara_object = self
