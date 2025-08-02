////////////////////////////////////////////////////////////////////////////////
// GL Transform Handling
////////////////////////////////////////////////////////////////////////////////

function getTransformEmpty() {
  return {
    model: undefined,
    view: undefined,
    projection: undefined,
    modelview: undefined,
    viewprojection: undefined,
    modelviewprojection: undefined,
    time : undefined,
  }
}

function getTransformModel(uniforms) {
  if (uniforms.model == undefined) {
    throw "Model matrix not set.";
  }
  return uniforms.model;
}

function getTransformView(uniforms) {
  if (uniforms.view == undefined) {
    throw "View matrix not set.";
  }
  return uniforms.view;
}

function getTransformProjection(uniforms) {
  if (uniforms.projection == undefined) {
    throw "Projection matrix not set.";
  }
  return uniforms.projection;
}

function getTransformModelView(uniforms) {
  if (uniforms.modelview != undefined) {
    return uniforms.modelview;
  }
  return uniforms.modelview =
    matMultiply(getTransformModel(uniforms), getTransformView(uniforms));    
}

function getTransformViewProjection(uniforms) {
  if (uniforms.viewprojection != undefined) {
    return uniforms.viewprojection;
  }
  return uniforms.viewprojection =
    matMultiply(getTransformView(uniforms), getTransformProjection(uniforms));
}

function getTransformModelViewProjection(uniforms) {
  if (uniforms.modelviewprojection != undefined) {
    return uniforms.viewprojection;
  }
  return uniforms.modelviewprojection =
    matMultiply(getTransformModel(uniforms), getTransformViewProjection(uniforms));
}

function setTransformModel(uniforms, model) {
  uniforms.model = model;
  uniforms.modelview = undefined;
  uniforms.modelviewprojection = undefined;
}

function setTransformView(uniforms, view) {
  uniforms.view = view;
  uniforms.modelview = undefined;
  uniforms.viewprojection = undefined;
  uniforms.modelviewprojection = undefined;
}

function setTransformProjection(uniforms, projection) {
  uniforms.projection = projection;
  uniforms.viewprojection = undefined;
  uniforms.modelviewprojection = undefined;
}

function glSetMatrix(program, name, matrix) {
    const uniform = gl.getUniformLocation(program, name);
    gl.uniformMatrix4fv(uniform, gl.TRUE, matrix);
    return matrix
}

function glSetUniforms(program, uniforms) {
  //console.log(uniforms);
  glSetMatrix(program, "model", getTransformModel(uniforms));
  glSetMatrix(program, "view", getTransformView(uniforms));
  glSetMatrix(program, "projection", getTransformProjection(uniforms));
  glSetMatrix(program, "modelview", getTransformModelView(uniforms));
  glSetMatrix(program, "viewprojection", getTransformViewProjection(uniforms));
  glSetMatrix(program, "modelviewprojection", getTransformModelViewProjection(uniforms));
  {
    const uniform = gl.getUniformLocation(program, "eye");
    const invview = matInvert(getTransformView(uniforms));
    gl.uniform3f(uniform, invview[12], invview[13], invview[14]);
  }
  {
    const uniform = gl.getUniformLocation(program, "time");
    gl.uniform1f(uniform, time);
  }
  {
    const uniform = gl.getUniformLocation(program, "Albedo");
    gl.uniform1i(uniform, 0);
  }
  {
    const uniform = gl.getUniformLocation(program, "Height");
    gl.uniform1i(uniform, 1);
  }
}