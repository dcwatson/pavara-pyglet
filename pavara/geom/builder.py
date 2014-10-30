from pavara.vecmath import Point3
from .base import Geom, Polygon

def block(color, size):
    x_shift = size[0] / 2.0
    y_shift = size[1] / 2.0
    z_shift = size[2] / 2.0

    vertices = (
        Point3(-x_shift, +y_shift, +z_shift),
        Point3(-x_shift, -y_shift, +z_shift),
        Point3(+x_shift, -y_shift, +z_shift),
        Point3(+x_shift, +y_shift, +z_shift),
        Point3(+x_shift, +y_shift, -z_shift),
        Point3(+x_shift, -y_shift, -z_shift),
        Point3(-x_shift, -y_shift, -z_shift),
        Point3(-x_shift, +y_shift, -z_shift),
    )

    faces = (
        # XY
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        # XZ
        [vertices[0], vertices[3], vertices[4], vertices[7]],
        [vertices[6], vertices[5], vertices[2], vertices[1]],
        # YZ
        [vertices[5], vertices[4], vertices[3], vertices[2]],
        [vertices[7], vertices[6], vertices[1], vertices[0]],
    )

    return Geom(
        Polygon(color, *faces[0]),
        Polygon(color, *faces[1]),
        Polygon(color, *faces[2]),
        Polygon(color, *faces[3]),
        Polygon(color, *faces[4]),
        Polygon(color, *faces[5])
    )
