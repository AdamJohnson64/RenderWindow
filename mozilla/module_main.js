const canvasGL = document.querySelector("#gl-canvas");
const gl = canvasGL.getContext("webgl2");
if (gl === null) {
	throw new Error();
}

const canvasTexture = document.querySelector("#gl-texture");
const ctx = canvasTexture.getContext("2d");
ctx.fillStyle = "red";
ctx.fillRect(0, 0, 256, 256);
ctx.fillStyle = "green";
ctx.fillRect(16, 16, 256 - 32, 256 - 32);
ctx.fillStyle = "black";
ctx.moveTo(0, 0);
ctx.lineTo(256, 256);
ctx.moveTo(256, 0);
ctx.lineTo(0, 256);
ctx.stroke();
ctx.font = "bold 48px serif";
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.fillText("Texture", 128, 128);

///////////////////////////////////////////////////////////////////////////////
// Create the default GLSL program from vertex and fragment shaders
let glProgramDefault = glCompileProgram(glShaderVertex, glShaderFragment);
const glMeshPlane = glCreateParametric(plane, 20, 20);
const glMeshSphere = glCreateParametric(sphere, 20, 20);
let frame = 0

///////////////////////////////////////////////////////////////////////////////
// Create the texture from the HTML5 canvas element
const glTextureDefault = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, glTextureDefault);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvasTexture);
gl.generateMipmap(gl.TEXTURE_2D);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

function glRender() {
  ////////////////////////////////////////
  // Clean up the framebuffer
  //gl.clearColor(Math.random(), Math.random(), Math.random(), 1.0);
  gl.clearColor(0, 0, 0, 0);
  gl.clearDepth(1);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LESS);
  ////////////////////////////////////////
  // Begin scene
  gl.useProgram(glProgramDefault);
  let uniforms = getTransformEmpty();
  setUniformTime(uniforms, frame);
  setTransformProjection(uniforms, matProjection(90, 0.001, 100.0));
  setTransformView(uniforms, matLookAt([25 * Math.cos(frame), 10 * (1 - Math.cos(frame * 0.2)), 10 * Math.sin(frame)],[0,0,0],[0,1,0]));
  // Draw a plane
  {
    setTransformModel(uniforms, matMultiply(matScale(50, 1, 50), matTranslate(0, -6, 0)));
    glSetUniforms(uniforms);
    glRenderMesh(glMeshPlane);
  }
  // Draw some spheres
  for (let z = -5; z <= 5; ++z) {
    for (let y = -5; y <= 5; ++y) {
      for (let x = -5; x <= 5; ++x) {
        setTransformModel(uniforms, matTranslate(x, y, z));
        glSetUniforms(uniforms);
        glRenderMesh(glMeshSphere);
      }
    }  
  }
  // Draw a big sphere on top
  setTransformModel(uniforms, matMultiply(matScale(5, 5, 5), matTranslate(0, 10, 0)));
  glSetUniforms(uniforms);
  glRenderMesh(glMeshSphere);
  // End Scene
  ////////////////////////////////////////
  frame = frame + 0.01;
}

///////////////////////////////////////////////////////////////////////////////
// Install event handler to process shaders
const codeedit_vertex = document.querySelector("#gl-vertexshader");
const codeedit_fragment = document.querySelector("#gl-fragmentshader");
const codeedit_error = document.querySelector("#gl-error");

function update() {
  try {
    glProgramDefault = glCompileProgram(codeedit_vertex.value, codeedit_fragment.value);
    codeedit_error.value = "Success"
  } catch (e) {
    codeedit_error.value = e;
  }
}

codeedit_vertex.addEventListener('input', update);
codeedit_fragment.addEventListener('input', update);
codeedit_vertex.value = glShaderVertex;
codeedit_fragment.value = glShaderFragment;
update();
///////////////////////////////////////////////////////////////////////////////

setInterval(glRender, 1000 / 60);