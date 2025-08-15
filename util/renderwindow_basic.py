import math
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *

from module_parametric import *
from module_gl_parametric import *

glfw.init()
window = glfw.create_window(500, 500, "Render Window", None, None)
glfw.set_window_pos(window, 100, 100) 
glfw.make_context_current(window)

plane = glCreateParametric(100, 100, getParametricPlane())
sphere = glCreateParametric(100, 100, getParametricSphere())
torus = glCreateParametric(100, 100, getParametricTorus(10, 1))

# Enable the Z-Buffer
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

time = 0

while not glfw.window_should_close(window):
   glfw.poll_events()
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
   gluLookAt(25 * math.cos(time), 10 * (1 - math.cos(time * 0.2)), 10 * math.sin(time),  0, 0, 0,  0, 1, 0)
   ########################################
   # Begin scene
   # Draw a plane
   glPushMatrix()
   glTranslate(0, -6, 0)
   glScale(50, 1, 50)
   glRenderMesh(plane)
   glPopMatrix()
   # Draw some spheres
   for z in range(-5, 6, 2):
      for y in range(-5, 6, 2):
         for x in range(-5, 6, 2):
            glPushMatrix()
            glTranslate(x, y, z)
            glRenderMesh(sphere)
            glPopMatrix()
   # Draw a big sphere on top
   glPushMatrix()
   glTranslate(0, 10, 0)
   glScale(5, 5, 5)
   glRenderMesh(sphere)
   glPopMatrix()
   # Draw a torus
   glPushMatrix()
   glTranslate(0, 1, 0)
   glRenderMesh(torus)
   glPopMatrix()
   # End Scene
   ########################################
   # Show the backbuffer
   time = time + 0.01
   glfw.swap_buffers(window)