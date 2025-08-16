import glfw
from OpenGL.GL import *
from module_parametric import *
from module_matrix import *
from module_mesh_gl41 import *
from module_shader_gl41 import *
from module_uniform_gl41 import *

# Initialize GLFW
glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
window = glfw.create_window(500, 500, "Render Window", None, None)
glfw.set_window_pos(window, 100, 100) 
glfw.make_context_current(window)
# Enable the Z-Buffer
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Create Geometry
plane = glxCreateMesh(createParametric(100, 100, getParametricPlane()))
sphere = glxCreateMesh(createParametric(100, 100, getParametricSphere()))
torus = glxCreateMesh(createParametric(100, 100, getParametricTorus(10, 1)))

# Create Shader Programs
program = glxCompileProgram(glShaderVertex, glShaderFragment);
glUseProgram(program)

time = 0

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0,0,1,1)
    glClearDepth(1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    v = matLookAt([25 * math.cos(time), 10 * (1 - math.cos(time * 0.2)), 10 * math.sin(time)], [0,0,0], [0,1,0])
    p = matProjection(90, 0.001, 100.0)
    ########################################
    # Begin scene
    # Draw a plane
    m = matScale(50, 1, 50) @ matTranslate(0, -6, 0)
    glxSetMatrix(program, "modelviewprojection", m @ v @ p)
    glxRenderMesh(plane)
    # Draw some spheres
    for z in range(-5, 6, 2):
        for y in range(-5, 6, 2):
            for x in range(-5, 6, 2):
                m = matTranslate(x, y, z)
                glxSetMatrix(program, "modelviewprojection", m @ v @ p)
                glxRenderMesh(sphere)
    # Draw a big sphere on top
    m = matScale(5, 5, 5) @ matTranslate(0, 10, 0)
    glxSetMatrix(program, "modelviewprojection", m @ v @ p)
    glxRenderMesh(sphere)
    # Draw a torus
    m = matTranslate(0, 1, 0)
    glxSetMatrix(program, "modelviewprojection", m @ v @ p)
    glxRenderMesh(torus)
    # End Scene
    ########################################
    time = time + 0.01
    glfw.swap_buffers(window)