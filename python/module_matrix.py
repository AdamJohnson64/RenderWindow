import math
import numpy

def matLookAt(eye, center, up):
    f = numpy.subtract(center, eye)
    f = f / math.sqrt(f.dot(f))
    s = numpy.cross(f, up)
    s = s / math.sqrt(s.dot(s))
    u = numpy.cross(s, f)
    return numpy.array([
        [s[0], u[0], -f[0], 0],
        [s[1], u[1], -f[1], 0],
        [s[2], u[2], -f[2], 0],
        [-numpy.dot(s, eye), -numpy.dot(u, eye), numpy.dot(f, eye), 1]], dtype=numpy.float32)

def matProjection(fov, near, far):
    f = 1 / math.tan((fov / 2) * (math.pi / 180))
    N = (far + near) / (near - far)
    F = (2 * far * near) / (near - far)
    return numpy.array([
        [f, 0, 0,  0],
        [0, f, 0,  0],
        [0, 0, N, -1],
        [0, 0, F,  0]], dtype = numpy.float32)

def matScale(x, y, z):
    return numpy.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]], dtype = numpy.float32)

def matTranslate(x, y, z):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]], dtype = numpy.float32)