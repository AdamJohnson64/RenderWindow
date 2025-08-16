import math
from collections import namedtuple
from module_mesh import *

###############################################################################
# Parametrics
###############################################################################

# A XZ plane
def planePos(u: float, v: float) -> tuple[float, float, float]:
    return (u - 0.5, 0, 0.5 - v)

def planeNor(u: float, v: float) -> tuple[float, float, float]:
    return [0, 1, 0]

# A sphere
def spherePos(u: float, v: float) -> tuple[float, float, float]:
    au = (2 * math.pi) * u
    av = (1 * math.pi) * v
    s = math.sin(av)
    return (s * math.cos(au), math.cos(av), s * math.sin(au))

def torusPos(major: float, minor: float):
    def function(u: float, v: float) -> tuple[float, float, float]:
        au = (2 * math.pi) * u
        av = (2 * math.pi) * v
        #x = (R + rcos(v))cos(u), y = (R + rcos(v))sin(u), and z = rsin(v). 
        return ((major + minor * math.cos(av)) * math.cos(au), minor * math.sin(av), (major + minor * math.cos(av)) * math.sin(au))
    return function

def unitUV(u: float, v: float) -> tuple[float, float]:
    return [u, v]

parametricClass = namedtuple("Parametric", ["Pos", "Nor", "ST0"])

def getParametricPlane() -> tuple:
    return parametricClass(Pos = planePos, Nor = planeNor, ST0 = unitUV)

def getParametricSphere() -> tuple:
    return parametricClass(Pos = spherePos, Nor = spherePos, ST0 = unitUV)

def getParametricTorus(major, minor) -> tuple:
    return parametricClass(Pos = torusPos(major, minor), Nor = torusPos(0, 1), ST0 = unitUV)

###############################################################################
# Parametric Buffer Construction
###############################################################################

# Generate 3D UV vertices for a given UV parametric object
# U,V define the number of quads in U and V directions respectively
def createParametricVecN(n: int, usteps: int, vsteps: int, fn: callable):
    us = usteps + 1
    vs = vsteps + 1
    for v in range(vs):
        for u in range(us):
            xyz = fn(u / usteps, v / vsteps)
            for i in range(n):
                yield xyz[i]

# Generate UV indices to match the above vertices
# U,V define the number of quads in U and V directions respectively
def createParametricIndices(usteps: int, vsteps: int):
    us = usteps + 1
    vs = vsteps + 1
    for v in range(vsteps):
        for u in range(usteps):
            yield (u + 0) + (v + 0) * us
            yield (u + 1) + (v + 0) * us
            yield (u + 1) + (v + 1) * us
            yield (u + 1) + (v + 1) * us
            yield (u + 0) + (v + 1) * us
            yield (u + 0) + (v + 0) * us

def createParametric(usteps: int, vsteps: int, fn: callable) -> tuple:
    # Generate the vertex and index buffers
    vtx = createParametricVecN(3, usteps, vsteps, fn.Pos)
    nor = createParametricVecN(3, usteps, vsteps, fn.Nor)
    st0 = createParametricVecN(2, usteps, vsteps, fn.ST0)
    idx = createParametricIndices(usteps, vsteps)
    # Return the generators for all buffers
    return meshGenClass(vtx = vtx, nor = nor, st0 = st0, idx = idx)