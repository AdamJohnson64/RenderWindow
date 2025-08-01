////////////////////////////////////////////////////////////////////////////////
// Parametric UV Shapes
////////////////////////////////////////////////////////////////////////////////

function planePos(u, v) {
  return [u - 0.5, 0, 0.5 - v];
}

function planeNor(u, v) {
  return [0, 1, 0];
}

function sphere(u, v) {
  const au = (2 * Math.PI) * u;
  const av = (1 * Math.PI) * v;
  const s = Math.sin(av);
  return [s * Math.cos(au), Math.cos(av), s * Math.sin(au)];
}

function torusPos(major, minor, u, v) {
  return function(u, v) {
    const au = (2 * Math.PI) * u;
    const av = (2 * Math.PI) * v;
    //x = (R + rcos(v))cos(u), y = (R + rcos(v))sin(u), and z = rsin(v). 
    return [
      (major + minor * Math.cos(av)) * Math.cos(au),
      minor * Math.sin(av),
      (major + minor * Math.cos(av)) * Math.sin(au),
    ];
  }
}

function torusNor(u, v) {
  return torusPos(0, 1)(u, v);
}

function unitUV(u, v) {
  return [u, v];
}

function getParametricPlane() {
  return { Pos : planePos, Nor : planeNor, UV0 : unitUV }
}

function getParametricSphere() {
  return { Pos : sphere, Nor : sphere, UV0 : unitUV }
}

function getParametricTorus(major, minor) {
  return { Pos : torusPos(major, minor), Nor : torusNor, UV0 : unitUV }
}