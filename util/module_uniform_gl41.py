import numpy
from OpenGL.GL import *

def glxSetMatrix(program, name, matrix):
    uniform = glGetUniformLocation(program, name)
    glUniformMatrix4fv(uniform, 1, GL_FALSE, numpy.ascontiguousarray(matrix))