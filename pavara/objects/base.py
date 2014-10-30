from pavara.vecmath import Vector3, Point3, Matrix4
import pyglet

class WorldObject (object):
    index = None
    world = None
    moved = False

    def __init__(self, world):
        self.world = world
        self.world.add(self)

class PhysicsObject (WorldObject):
    position = None
    velocity = None
    mass = None
    geom = None
    shape = None

    def __init__(self, world, position, mass):
        self.position = Point3(*position)
        self.velocity = Vector3()
        self.mass = mass
        super(PhysicsObject, self).__init__(world)

    @property
    def inv_mass(self):
        if self.mass:
            return 1.0 / self.mass
        return 0.0

    def tick(self, dt):
        if self.mass > 0:
            r = self.position
            v = self.velocity
            a = lambda pos: self.world.gravity
            r_new = r + v*dt + a(r)*dt**2/2
            v_new = v + (a(r) + a(r_new))/2 * dt
            if v and r_new != self.position:
                self.moved = True
            self.position = r_new
            self.velocity = v_new
            self.sync()

    def sync(self):
        if self.geom:
            self.geom.translate(self.position.x, self.position.y, self.position.z)
        if self.shape:
            self.shape.setPosition((self.position.x, self.position.y, self.position.z))

    def draw(self, batch):
        if self.geom:
            self.geom.draw(batch)
    
    def apply_force(self, vec):
        self.velocity += vec
        self.sync()
    
    def moveto(self, x, y, z):
        self.position.set(x, y, z, save=False)
        self.sync()
    
    def rotate(self, yaw, pitch, roll):
        if self.geom:
            self.geom.rotate(yaw, pitch, roll)
        if self.shape:
            t = Matrix4().set_rotation(yaw, pitch, roll)
            self.shape.setRotation((t.a, t.b, t.c, t.e, t.f, t.g, t.i, t.j, t.k))

    # Collision Detection
    
    def bounds_check(self, other):
        d = self.position.distance_squared(other.position)
        return d <= ((self.geom.radius + other.geom.radius) ** 2)
    
    def collide(self, other):
        return self.geom.collide(other.geom)
