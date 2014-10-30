from pavara.vecmath import Matrix4, Point3
import pyglet

_intersect = lambda A, B: (A[1] > B[0] and B[1] > A[0])
_overlap = lambda p1, p2: min(max(p1[0], p1[1]), max(p2[0], p2[1])) - max(min(p1[0], p1[1]), min(p2[0], p2[1]))

def axes(*polys):
    for poly in polys:
        for i, p in enumerate(poly.points):
            q = poly.points[(i + 1) % len(poly.points)]
            yield p.cross(q).normalize()
            yield (q - p).normalize()

class Collision (object):
    normal = None
    depth = None

    def __init__(self, normal, depth):
        self.normal = normal
        self.depth = depth

class Polygon (object):
    
    def __init__(self, color, *points):
        self.color = color
        self.points = points
        self.vertices = []
        self.colors = []
        self.n = len(self.points)
        for p in self.points:
            self.vertices.extend((p.x, p.y, p.z))
            self.colors.extend(self.color)
        self._normal = None
        self._centroid = None
    
    def reset(self):
        for p in self.points:
            p.revert()
    
    @property
    def normal(self):
        if not self._normal:
            a = self.points[0] - self.points[1]
            b = self.points[0] - self.points[2]
            self._normal = a.cross(b).normalize()
        return self._normal
    
    @property
    def centroid(self):
        if not self._centroid:
            x, y, z, n = 0.0, 0.0, 0.0, self.n
            for p in self.points:
                x += p.x
                y += p.y
                z += p.z
            self._centroid = Point3(x / n, y / n, z / n)
        return self._centroid
    
    def transform(self, mat):
        for idx, p in enumerate(self.points):
            mat.itransform(p)
            i = idx * 3
            self.vertices[i + 0] = p.x
            self.vertices[i + 1] = p.y
            self.vertices[i + 2] = p.z
        # Clear the cached normal vector and centroid
        self._normal = None
        self._centroid = None
    
    def project(self, axis):
        projected_points = [axis.dot(p) for p in self.points]
        return min(projected_points), max(projected_points)

    def collide(self, other):
        overlap = float('inf')
        axis = None
        for a in axes(self, other):
            p1 = self.project(a)
            p2 = other.project(a)
            if not _intersect(p1, p2):
                return None
            else:
                o = _overlap(p1, p2)
                if o < overlap:
                    overlap = o
                    axis = a
        return Collision(self.normal, overlap)

    def draw(self, batch):
        batch.add(self.n, pyglet.gl.GL_QUADS, None,
            ('v3f', self.vertices),
            ('c4f', self.colors),
        )
        if False:
            n = self.centroid + self.normal
            batch.add(2, pyglet.gl.GL_LINES, None,
                ('v3f', (self.centroid.x, self.centroid.y, self.centroid.z, n.x, n.y, n.z)),
            )

class Geom (object):

    def __init__(self, *polys):
        self.polygons = polys
        self.transform = Matrix4()
        self.radius = max([max([p.magnitude() for p in poly.points]) for poly in self.polygons])
        self.translation = Matrix4()
        self.rotation = Matrix4()

    def draw(self, batch):
        for poly in self.polygons:
            poly.draw(batch)

    def reset(self):
        for poly in self.polygons:
            poly.reset()

    def apply(self):
        for poly in self.polygons:
            poly.reset()
            #poly.transform(self.transform)
            poly.transform(self.rotation)
            poly.transform(self.translation)

    def translate(self, x, y, z):
        self.translation = Matrix4().set_translation(x, y, z)
        self.transform.set_translation(x, y, z)
        self.apply()

    def rotate(self, yaw, pitch, roll):
        self.rotation = Matrix4().set_rotation(yaw, pitch, roll)
        self.transform.set_rotation(yaw, pitch, roll)
        self.apply()

    def collide(self, other):
        for p1 in self.polygons:
            for p2 in other.polygons:
                c = p1.collide(p2)
                if c:
                    return c

    @property
    def top(self):
        return max([max([p.y for p in poly.points]) for poly in self.polygons])

    @property
    def bottom(self):
        return min([min([p.y for p in poly.points]) for poly in self.polygons])
