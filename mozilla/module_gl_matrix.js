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

function getUniformTime(uniforms) {
  if (uniforms.time == undefined) {
    throw "Time not set.";
  }
  return uniforms.time;
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

function setUniformTime(uniforms, time) {
  uniforms.time = time;
}

function glSetMatrix(name, matrix) {
    const uniform = gl.getUniformLocation(glProgramDefault, name);
    gl.uniformMatrix4fv(uniform, gl.TRUE, matrix);
    return matrix
}

function glSetUniforms(uniforms) {
  //console.log(uniforms);
  glSetMatrix("model", getTransformModel(uniforms));
  glSetMatrix("view", getTransformView(uniforms));
  glSetMatrix("projection", getTransformProjection(uniforms));
  glSetMatrix("modelview", getTransformModelView(uniforms));
  glSetMatrix("viewprojection", getTransformViewProjection(uniforms));
  glSetMatrix("modelviewprojection", getTransformModelViewProjection(uniforms));
  const uniform = gl.getUniformLocation(glProgramDefault, "time");
  gl.uniform1f(uniform, getUniformTime(uniforms));
}