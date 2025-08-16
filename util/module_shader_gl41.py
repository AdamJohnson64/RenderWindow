###############################################################################
# Shader Handling
###############################################################################

from OpenGL.GL import *

glShaderVertex = """#version 410 core
precision highp float;

layout(location = 0) in vec3 inPos;
layout(location = 1) in vec3 inNor;
layout(location = 2) in vec2 inST0;
out vec3 outPos;
out vec3 outNor;
out vec2 outST0;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 modelview;
uniform mat4 viewprojection;
uniform mat4 modelviewprojection;

void main(void) {
    gl_Position = modelviewprojection * vec4(inPos, 1.0);
    outNor = inNor; //normalize(mat3(model) * inNor);
    outST0 = inST0;
}
"""

glShaderFragment = """#version 410 core
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;
out vec4 outCol;

void main(void) {
    outCol = vec4(outNor, 1.0);
}
"""

def glxCompileShader(type, code, name):
    id_shader = glCreateShader(type)
    glShaderSource(id_shader, code)
    glCompileShader(id_shader)
    infolog = glGetShaderInfoLog(id_shader)
    version = glGetString(GL_SHADING_LANGUAGE_VERSION)
    if glGetShaderInfoLog(id_shader):
        error = name + " Shader Compiler Error: " + glGetShaderInfoLog(id_shader).decode('utf-8')
        glDeleteShader(id_shader)
        raise Exception(error)
    return id_shader

def glxCompileProgram(code_vertex, code_fragment):
    id_program = glCreateProgram()
    id_shader_vertex = glxCompileShader(GL_VERTEX_SHADER, code_vertex, "Vertex")
    id_shader_fragment = glxCompileShader(GL_FRAGMENT_SHADER, code_fragment, "Fragment")
    glAttachShader(id_program, id_shader_vertex)
    glAttachShader(id_program, id_shader_fragment)
    glLinkProgram(id_program)
    return id_program