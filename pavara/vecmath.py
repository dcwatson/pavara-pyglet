import math

class Vector3 (object):
    __slots__ = ('x', 'y', 'z', '_x', '_y', '_z')
    __hash__ = None
    
    def __init__(self, x=0, y=0, z=0):
        self.x = self._x = x
        self.y = self._y = y
        self.z = self._z = z
    
    def __copy__(self):
        return self.__class__(self.x, self.y, self.z)
    
    copy = __copy__
    
    def __repr__(self):
        return 'Vector3(%.2f, %.2f, %.2f)' % (self.x, self.y, self.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z
    
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z
    
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z
    
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z
    
    def __nonzero__(self):
        return self.x != 0 or self.y != 0 or self.z != 0
    
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __iadd__(self, other):
        self._x = self.x
        self._y = self.y
        self._z = self.z
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __mul__(self, other):
        return self.__class__(self.x * other, self.y * other, self.z * other)
    
    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self
    
    def __div__(self, other):
        return self.__class__(self.x / other, self.y / other, self.z / other)
    
    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other
        return self
    
    __truediv__ = __div__
    __itruediv__ = __idiv__
    
    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)
    
    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2
    
    def magnitude(self):
        return math.sqrt(self.magnitude_squared())

    def normalize(self):
        d = self.magnitude()
        if d:
            self.x /= d
            self.y /= d
            self.z /= d
        return self
    
    def normalized(self):
        return self.copy().normalize()
    
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def cross(self, other):
        return self.__class__(
            (self.y * other.z) - (self.z * other.y),
            (-self.x * other.z) + (self.z * other.x),
            (self.x * other.y) - (self.y * other.x)
        )
    
    def project(self, other):
        n = other.normalized()
        return n * self.dot(n)
    
    def distance_squared(self, other):
        return ((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2)
    
    def set(self, x, y, z, save=True):
        self._x = self.x if save else x
        self._y = self.y if save else y
        self._z = self.z if save else z
        self.x = x
        self.y = y
        self.z = z
        return self
    
    def revert(self):
        self.x = self._x
        self.y = self._y
        self.z = self._z
        return self

class Point3 (Vector3):
    
    def velocity(self):
        return Vector3(self.x - self._x, self.y - self._y, self.z - self._z)

    def verlet(self, a, dt):
        tx = self.x
        ty = self.y
        tz = self.z
        m = a * (dt * dt)
        self.x += (self.x - self._x) + m.x
        self.y += (self.y - self._y) + m.y
        self.z += (self.z - self._z) + m.z
        self._x = tx
        self._y = ty
        self._z = tz

#  a b c d
#  e f g h
#  i j k l
#  m n o p

class Matrix4 (object):
    __slots__ = list('abcdefghijklmnop')

    def __init__(self):
        self.identity()

    def __copy__(self):
        M = self.__class__()
        M.a = self.a
        M.b = self.b
        M.c = self.c
        M.d = self.d
        M.e = self.e 
        M.f = self.f
        M.g = self.g
        M.h = self.h
        M.i = self.i
        M.j = self.j
        M.k = self.k
        M.l = self.l
        M.m = self.m
        M.n = self.n
        M.o = self.o
        M.p = self.p
        return M

    copy = __copy__

    def __repr__(self):
        return ('Matrix4([% 8.2f % 8.2f % 8.2f % 8.2f\n'  \
                '         % 8.2f % 8.2f % 8.2f % 8.2f\n'  \
                '         % 8.2f % 8.2f % 8.2f % 8.2f\n'  \
                '         % 8.2f % 8.2f % 8.2f % 8.2f])') \
                % (self.a, self.b, self.c, self.d,
                   self.e, self.f, self.g, self.h,
                   self.i, self.j, self.k, self.l,
                   self.m, self.n, self.o, self.p)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            Aa = self.a
            Ab = self.b
            Ac = self.c
            Ad = self.d
            Ae = self.e
            Af = self.f
            Ag = self.g
            Ah = self.h
            Ai = self.i
            Aj = self.j
            Ak = self.k
            Al = self.l
            Am = self.m
            An = self.n
            Ao = self.o
            Ap = self.p
            Ba = other.a
            Bb = other.b
            Bc = other.c
            Bd = other.d
            Be = other.e
            Bf = other.f
            Bg = other.g
            Bh = other.h
            Bi = other.i
            Bj = other.j
            Bk = other.k
            Bl = other.l
            Bm = other.m
            Bn = other.n
            Bo = other.o
            Bp = other.p
            C = Matrix4()
            C.a = Aa * Ba + Ab * Be + Ac * Bi + Ad * Bm
            C.b = Aa * Bb + Ab * Bf + Ac * Bj + Ad * Bn
            C.c = Aa * Bc + Ab * Bg + Ac * Bk + Ad * Bo
            C.d = Aa * Bd + Ab * Bh + Ac * Bl + Ad * Bp
            C.e = Ae * Ba + Af * Be + Ag * Bi + Ah * Bm
            C.f = Ae * Bb + Af * Bf + Ag * Bj + Ah * Bn
            C.g = Ae * Bc + Af * Bg + Ag * Bk + Ah * Bo
            C.h = Ae * Bd + Af * Bh + Ag * Bl + Ah * Bp
            C.i = Ai * Ba + Aj * Be + Ak * Bi + Al * Bm
            C.j = Ai * Bb + Aj * Bf + Ak * Bj + Al * Bn
            C.k = Ai * Bc + Aj * Bg + Ak * Bk + Al * Bo
            C.l = Ai * Bd + Aj * Bh + Ak * Bl + Al * Bp
            C.m = Am * Ba + An * Be + Ao * Bi + Ap * Bm
            C.n = Am * Bb + An * Bf + Ao * Bj + Ap * Bn
            C.o = Am * Bc + An * Bg + Ao * Bk + Ap * Bo
            C.p = Am * Bd + An * Bh + Ao * Bl + Ap * Bp
            return C
        elif isinstance(other, Point3):
            A = self
            B = other
            x = A.a * B.x + A.b * B.y + A.c * B.z + A.d
            y = A.e * B.x + A.f * B.y + A.g * B.z + A.h
            z = A.i * B.x + A.j * B.y + A.k * B.z + A.l
            return Point3(x, y, z)
        elif isinstance(other, Vector3):
            A = self
            B = other
            x = A.a * B.x + A.b * B.y + A.c * B.z
            y = A.e * B.x + A.f * B.y + A.g * B.z
            z = A.i * B.x + A.j * B.y + A.k * B.z
            return Vector3(x, y, z)

    def __imul__(self, other):
        assert isinstance(other, Matrix4)
        Aa = self.a
        Ab = self.b
        Ac = self.c
        Ad = self.d
        Ae = self.e
        Af = self.f
        Ag = self.g
        Ah = self.h
        Ai = self.i
        Aj = self.j
        Ak = self.k
        Al = self.l
        Am = self.m
        An = self.n
        Ao = self.o
        Ap = self.p
        Ba = other.a
        Bb = other.b
        Bc = other.c
        Bd = other.d
        Be = other.e
        Bf = other.f
        Bg = other.g
        Bh = other.h
        Bi = other.i
        Bj = other.j
        Bk = other.k
        Bl = other.l
        Bm = other.m
        Bn = other.n
        Bo = other.o
        Bp = other.p
        self.a = Aa * Ba + Ab * Be + Ac * Bi + Ad * Bm
        self.b = Aa * Bb + Ab * Bf + Ac * Bj + Ad * Bn
        self.c = Aa * Bc + Ab * Bg + Ac * Bk + Ad * Bo
        self.d = Aa * Bd + Ab * Bh + Ac * Bl + Ad * Bp
        self.e = Ae * Ba + Af * Be + Ag * Bi + Ah * Bm
        self.f = Ae * Bb + Af * Bf + Ag * Bj + Ah * Bn
        self.g = Ae * Bc + Af * Bg + Ag * Bk + Ah * Bo
        self.h = Ae * Bd + Af * Bh + Ag * Bl + Ah * Bp
        self.i = Ai * Ba + Aj * Be + Ak * Bi + Al * Bm
        self.j = Ai * Bb + Aj * Bf + Ak * Bj + Al * Bn
        self.k = Ai * Bc + Aj * Bg + Ak * Bk + Al * Bo
        self.l = Ai * Bd + Aj * Bh + Ak * Bl + Al * Bp
        self.m = Am * Ba + An * Be + Ao * Bi + Ap * Bm
        self.n = Am * Bb + An * Bf + Ao * Bj + Ap * Bn
        self.o = Am * Bc + An * Bg + Ao * Bk + Ap * Bo
        self.p = Am * Bd + An * Bh + Ao * Bl + Ap * Bp
        return self

    def transform(self, point):
        A = self
        B = point
        x = A.a * B.x + A.b * B.y + A.c * B.z + A.d
        y = A.e * B.x + A.f * B.y + A.g * B.z + A.h
        z = A.i * B.x + A.j * B.y + A.k * B.z + A.l
        w = A.m * B.x + A.n * B.y + A.o * B.z + A.p
        if w != 0:
            x /= w
            y /= w
            z /= w
        return Point3(x, y, z)
    
    def itransform(self, point):
        A = self
        B = point
        B.x = A.a * B.x + A.b * B.y + A.c * B.z + A.d
        B.y = A.e * B.x + A.f * B.y + A.g * B.z + A.h
        B.z = A.i * B.x + A.j * B.y + A.k * B.z + A.l
        w =   A.m * B.x + A.n * B.y + A.o * B.z + A.p
        if w != 0:
            B.x /= w
            B.y /= w
            B.z /= w
        return B
    
    def identity(self):
        self.a = self.f = self.k = self.p = 1.0
        self.b = self.c = self.d = self.e = self.g = self.h = self.i = self.j = self.l = self.m = self.n = self.o = 0
        return self
    
    def set_translation(self, x, y, z):
        self.d = x
        self.h = y
        self.l = z
        return self
    
    def set_rotation(self, yaw, pitch, roll):
        ch = math.cos(yaw)
        sh = math.sin(yaw)
        ca = math.cos(pitch)
        sa = math.sin(pitch)
        cb = math.cos(roll)
        sb = math.sin(roll)
        
        self.a = ch * ca
        self.b = sh * sb - ch * sa * cb
        self.c = ch * sa * sb + sh * cb
        self.e = sa
        self.f = ca * cb
        self.g = -ca * sb
        self.i = -sh * ca
        self.j = sh * sa * cb + ch * sb
        self.k = -sh * sa * sb + ch * cb
        
        self.m = self.n = self.o = 0
        self.p = 1.0
        
        return self
