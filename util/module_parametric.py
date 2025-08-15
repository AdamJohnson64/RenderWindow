import math
from collections import namedtuple

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