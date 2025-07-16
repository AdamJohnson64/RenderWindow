function compileShader(type, code, name) {
  const id_shader = gl.createShader(type);
  gl.shaderSource(id_shader, code);
  gl.compileShader(id_shader);
  if (!gl.getShaderParameter(id_shader, gl.COMPILE_STATUS)) {
    const error = name +" Shader Compiler Error: " + gl.getShaderInfoLog(id_shader)
    gl.deleteShader(id_shader);
    throw new Error(error);
  }
  return id_shader;
}

function compileProgram(code_vertex, code_fragment) {
  const id_program = gl.createProgram();
  const id_shader_vertex = compileShader(gl.VERTEX_SHADER, code_vertex, "Vertex");
  const id_shader_fragment = compileShader(gl.FRAGMENT_SHADER, code_fragment, "Fraggment");
  gl.attachShader(id_program, id_shader_vertex);
  gl.attachShader(id_program, id_shader_fragment);
  gl.linkProgram(id_program);
  return id_program;
}