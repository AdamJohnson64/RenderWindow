////////////////////////////////////////////////////////////////////////////////
// GL Parametric Mesh Construction
////////////////////////////////////////////////////////////////////////////////

function glCreateParametricVector3(func, in_u, in_v) {
  const steps_u = in_u + 1;
  const steps_v = in_v + 1;
  const vec = new Float32Array(3 * steps_u * steps_v);
  for (let v = 0; v < steps_v; ++v) {
    for (let u = 0; u < steps_u; ++u) {
      const base = 3 * (u + v * steps_u);
      const point = func(u / in_u, v / in_v);
      vec[base + 0] = point[0];
      vec[base + 1] = point[1];
      vec[base + 2] = point[2];
    }
  }
  const id = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, id);
  gl.bufferData(gl.ARRAY_BUFFER, vec, gl.STATIC_DRAW);
  return id;
}

function glCreateParametricIndices(func, in_u, in_v) {
  const steps_u = in_u + 1;
  const steps_v = in_v + 1;
  const vec = new Int16Array(2 * 3 * in_u * in_v);
  for (let v = 0; v < in_v; ++v) {
    for (let u = 0; u < in_u; ++u) {
      const base = 2 * 3 * (u + v * in_u);
      vec[base + 0] = (u + 0) + (v + 0) * steps_u;
      vec[base + 1] = (u + 1) + (v + 0) * steps_u;
      vec[base + 2] = (u + 0) + (v + 1) * steps_u;
      vec[base + 3] = (u + 1) + (v + 0) * steps_u;
      vec[base + 4] = (u + 0) + (v + 1) * steps_u;
      vec[base + 5] = (u + 1) + (v + 1) * steps_u;
    }
  }
  const id = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, id);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, vec, gl.STATIC_DRAW);
  return id;
}

function computeNormal(func, u, v) {
  const du = vector3Sub(func(u - 0.01, v), func(u + 0.01, v));
  const dv = vector3Sub(func(u, v - 0.01), func(u, v + 0.01));
  const t = vector3Normalize(vector3Cross(du, dv));
  if (t[0] > 0.99 && t[1] > 0.99 && t[2] < 0.99) throw new Error("Oops");
  return t;
};

function glCreateParametric(func, u, v) {
  const norm = function(u2, v2) {
    return computeNormal(func, u2, v2);
  }
  return {
    id_vertex: glCreateParametricVector3(func, u, v),
    id_normal: glCreateParametricVector3(norm, u, v),
    id_index: glCreateParametricIndices(func, u, v),
    triangle_count: 2 * u * v,
  };
}
