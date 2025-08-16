import numpy
from collections import namedtuple
from OpenGL.GL import *
from module_mesh import *

meshClass = namedtuple("Mesh", ["id_vertex", "id_normal", "id_index", "id_texcoord", "triangle_count"])

def glxCreateMesh(meshgen: tuple) -> tuple:
    # Generate the vertex and index buffers
    vtx = numpy.array(list(meshgen.vtx), dtype = numpy.float32)
    nor = numpy.array(list(meshgen.nor), dtype = numpy.float32)
    st0 = numpy.array(list(meshgen.st0), dtype = numpy.float32)
    idx = numpy.array(list(meshgen.idx), dtype = numpy.uint16)
    # Construct vertex and index OpenGL buffers
    buffers = numpy.empty(4, dtype = numpy.uint32)
    glGenBuffers(4, buffers)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glBufferData(GL_ARRAY_BUFFER, 4 * vtx.size, vtx, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glBufferData(GL_ARRAY_BUFFER, 4 * nor.size, nor, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[2]);
    glBufferData(GL_ARRAY_BUFFER, 4 * st0.size, st0, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[3]);
    glBufferData(GL_ARRAY_BUFFER, 2 * idx.size, idx, GL_STATIC_DRAW)
    return meshClass(id_vertex = buffers[0], id_normal = buffers[1], id_texcoord = buffers[2], id_index = buffers[3], triangle_count = idx.size)

def glxRenderMesh(mesh: tuple) -> None:
    # (0, 1, 2) => (vertex_buffer_id, index_buffer_id, index_count)
    # Enable vertex positions
    glBindBuffer(GL_ARRAY_BUFFER, mesh.id_vertex)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    # Enable and establish normals
    #glBindBuffer(GL_ARRAY_BUFFER, mesh.id_normal)
    #glEnableClientState(GL_NORMAL_ARRAY)
    #glNormalPointer(3, GL_FLOAT, 12, ctypes.c_void_p(0))
    ########################################
    # DEBUG: Enable and establish colors
    glBindBuffer(GL_ARRAY_BUFFER, mesh.id_normal)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 12, ctypes.c_void_p(0))
    ########################################
    # Enable texture coordinates
    glBindBuffer(GL_ARRAY_BUFFER, mesh.id_texcoord)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glTexCoordPointer(2, GL_FLOAT, 8, ctypes.c_void_p(0))
    # Bind the indices and draw
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.id_index)
    glDrawElements(GL_TRIANGLES, mesh.triangle_count, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))