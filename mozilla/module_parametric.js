////////////////////////////////////////////////////////////////////////////////
// Parametric UV Shapes
////////////////////////////////////////////////////////////////////////////////

function plane(u, v) {
  return [u - 0.5, 0, 0.5 - v];
}

function sphere(u, v) {
  const angle_u = (2 * Math.PI) * u;
  const angle_v = (1 * Math.PI) * v;
  const scale = Math.sin(angle_v);
  return [scale * Math.cos(angle_u), Math.cos(angle_v), scale * Math.sin(angle_u)];
}