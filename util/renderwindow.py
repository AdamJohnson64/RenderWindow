import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

###############################################################################
# Parametrics
###############################################################################

# A XZ plane
def uvPlane(u, v):
   return [u - 0.5, 0, 0.5 - v]

# A sphere
def uvSphere(u, v):
  au = (2 * math.pi) * u
  av = (1 * math.pi) * v
  s = math.sin(av)
  return [s * math.cos(au), math.cos(av), s * math.sin(au)]

# Generate 3D UV vertices for a given UV parametric object
# U,V define the number of quads in U and V directions respectively
def uvVertex(usteps, vsteps, fn):
   us = usteps + 1
   vs = vsteps + 1
   for v in range(vs):
      for u in range(us):
         xyz = fn(u / usteps, v / vsteps)
         yield xyz[0]
         yield xyz[1]
         yield xyz[2]

# Generate UV indices to match the above vertices
# U,V define the number of quads in U and V directions respectively
def uvIndex(usteps, vsteps):
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

###############################################################################
# OpenGL Primary Initialization
###############################################################################

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("RenderWindow")

###############################################################################
# OpenGL Resource Initialization
###############################################################################

# Generate the vertex and index buffers
vtx = numpy.array(list(uvVertex(10, 10, uvSphere)), dtype = numpy.float32)
idx = numpy.array(list(uvIndex(10, 10)), dtype = numpy.uint16)

# Construct vertex and index OpenGL buffers
mesh = numpy.empty(2, dtype = numpy.uint32)
glGenBuffers(2, mesh)
glBindBuffer(GL_ARRAY_BUFFER, mesh[0])
glBufferData(GL_ARRAY_BUFFER, 4 * vtx.size, vtx, GL_STATIC_DRAW)
#glBufferData(GL_ARRAY_BUFFER, 36, numpy.array([0, 0, 0,  1, 0, 0,  0, 1, 0], dtype=numpy.float32), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, mesh[1]);
glBufferData(GL_ARRAY_BUFFER, 2 * idx.size, idx, GL_STATIC_DRAW)
#glBufferData(GL_ARRAY_BUFFER, 6, numpy.array([0, 1, 2], dtype=numpy.uint16), GL_STATIC_DRAW)

time = 0

# Draw OpenGL frame (clear, drawcalls)
def showScreen():
   global time
   # Clear the color and depth buffers
   glClearColor(0,0,1,1)
   glClearDepth(1)
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   # Set up the transform stack
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   gluPerspective(90, 1, 0.001, 1000.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   #setTransformView(uniforms, matLookAt([25 * Math.cos(time), 10 * (1 - Math.cos(time * 0.2)), 10 * Math.sin(time)],[0,0,0],[0,1,0]));
   gluLookAt(25 * math.cos(time), 10 * (1 - math.cos(time * 0.2)), 10 * math.sin(time),  0, 0, 0,  0, 1, 0)
   # Draw some content
   for z in range(-5, 6, 2):
      for y in range(-5, 6, 2):
         for x in range(-5, 6, 2):
            glPushMatrix()
            glTranslate(x, y, z)
            glBindBuffer(GL_ARRAY_BUFFER, mesh[0])
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh[1])
            glDrawElements(GL_TRIANGLES, idx.size, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
            glPopMatrix()
   # Show the backbuffer
   glutSwapBuffers()
   time = time + 0.01

###############################################################################
# OpenGL Display Finalization (draw call, window loop)
###############################################################################
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()