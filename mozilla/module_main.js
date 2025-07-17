const canvas = document.querySelector("#gl-canvas");
const gl = canvas.getContext("webgl");
if (gl === null) {
	alert("WebGL Unavailable.");
	throw new Error();
}

const code_vertex = `#version 100
attribute vec3 pos;
attribute vec3 nor;
varying highp vec3 nor2;
uniform mat4 mvp;

void main(void) {
  gl_Position = mvp * vec4(pos.x, pos.y, pos.z, 1.0);
  nor2 = nor + vec3(0.5, 0.5, 0.5);
}
`;

const code_fragment = `#version 100
varying highp vec3 nor2;

void main(void) {
  gl_FragColor = vec4(nor2.x, nor2.y, nor2.z, 1.0);
}
`;

const id_program = compileProgram(code_vertex, code_fragment);
const parametric_plane = createParametric(plane, 20, 20);
const parametric_sphere = createParametric(sphere, 20, 20);
var frame = 0

function renderMesh(parametric) {
  gl.useProgram(id_program);
  // Position
  gl.bindBuffer(gl.ARRAY_BUFFER, parametric.id_vertex);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 3, gl.FLOAT, gl.FALSE, 12, 0);
  // Normal
  gl.bindBuffer(gl.ARRAY_BUFFER, parametric.id_normal);
  gl.enableVertexAttribArray(1);
  gl.vertexAttribPointer(1, 3, gl.FLOAT, gl.FALSE, 12, 0);
  // Draw
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, parametric.id_index);
  gl.drawElements(gl.TRIANGLES, 3 * parametric.triangle_count, gl.UNSIGNED_SHORT, 0);
}

function render() {
  //gl.clearColor(Math.random(), Math.random(), Math.random(), 1.0);
  gl.clearColor(0, 0, 0, 1.0);
  gl.clearDepth(1.0);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LESS);
  var view = matLookAt([10 * Math.cos(frame),0,5 * Math.sin(frame)],[0,0,0],[0,1,0])
  var projection = matProjection(90, 0.001, 100.0);
  // Draw a plane
  {
    var model = matTranslate(0, -6, 0);
    model = matMultiply(model, matScale(50, 1, 50));
    mat = matMultiply(model, view);
    mat = matMultiply(mat, projection);
    const uniform_mvp = gl.getUniformLocation(id_program, "mvp");
    gl.uniformMatrix4fv(uniform_mvp, gl.TRUE, matFlatten(mat));
    renderMesh(parametric_plane);
  }
  // Draw some spheres
  for (var y = -5; y < 5; ++y) {
    for (var x = -5; x < 5; ++x) {
      const model = matTranslate(x, y, 0);
      mat = matMultiply(model, view);
      mat = matMultiply(mat, projection);
      const uniform_mvp = gl.getUniformLocation(id_program, "mvp");
      gl.uniformMatrix4fv(uniform_mvp, gl.TRUE, matFlatten(mat));
      renderMesh(parametric_sphere);
    }
    frame = frame + 0.001;
  }
}

setInterval(render, 1000 / 60);