import numpy
from OpenGL.GL import *
from OpenGL.GLUT import *

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("RenderWindow")

mesh = numpy.empty(2, dtype = numpy.uint32)

glGenBuffers(2, mesh)
glBindBuffer(GL_ARRAY_BUFFER, mesh[0])
glBufferData(GL_ARRAY_BUFFER, 24, numpy.array([0, 0, 1, 0, 0, 1], dtype=numpy.float32), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, mesh[1]);
glBufferData(GL_ARRAY_BUFFER, 6, numpy.array([0, 1, 2], dtype=numpy.uint16), GL_STATIC_DRAW)

def showScreen():
    glClearColor(0,0,1,1)
    glClearDepth(1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, mesh[0])
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh[1])
    glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
    
    glutSwapBuffers()

glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)

glutMainLoop()