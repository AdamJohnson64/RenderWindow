function matCreate() {
  // Return a new identity matrix as a flat array
  return new Float32Array([
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
  ]);
}

function matDeterminant(m) {
  // m is a flat 16-element array
  // For readability, assign each element
  const m00 = m[0],  m01 = m[1],  m02 = m[2],  m03 = m[3];
  const m10 = m[4],  m11 = m[5],  m12 = m[6],  m13 = m[7];
  const m20 = m[8],  m21 = m[9],  m22 = m[10], m23 = m[11];
  const m30 = m[12], m31 = m[13], m32 = m[14], m33 = m[15];
  return (
    m03 * m12 * m21 * m30 - m02 * m13 * m21 * m30 - m03 * m11 * m22 * m30 + m01 * m13 * m22 * m30 +
    m02 * m11 * m23 * m30 - m01 * m12 * m23 * m30 - m03 * m12 * m20 * m31 + m02 * m13 * m20 * m31 +
    m03 * m10 * m22 * m31 - m00 * m13 * m22 * m31 - m02 * m10 * m23 * m31 + m00 * m12 * m23 * m31 +
    m03 * m11 * m20 * m32 - m01 * m13 * m20 * m32 - m03 * m10 * m21 * m32 + m00 * m13 * m21 * m32 +
    m01 * m10 * m23 * m32 - m00 * m11 * m23 * m32 - m02 * m11 * m20 * m33 + m01 * m12 * m20 * m33 +
    m02 * m10 * m21 * m33 - m00 * m12 * m21 * m33 - m01 * m10 * m22 * m33 + m00 * m11 * m22 * m33
  );
}

function matInvert(m) {
  // m is a flat 16-element array
  const inv = new Float32Array(16);
  const d = matDeterminant(m);
  if (d === 0) return null;
  // Compute the inverse using the analytic formula for 4x4 matrices
  // (code omitted for brevity, can use gl-matrix or similar for production)
  // For now, just return identity for placeholder
  // TODO: Implement full inversion
  for (let i = 0; i < 16; ++i) inv[i] = (i % 5 === 0) ? 1 : 0;
  return inv;
}

function matLookAt(eye, center, up) {
  // Standard WebGL right-handed lookAt (column-major)
  let z = vector3Normalize([
    eye[0] - center[0],
    eye[1] - center[1],
    eye[2] - center[2]
  ]);
  let x = vector3Normalize(vector3Cross(up, z));
  let y = vector3Cross(z, x);
  return new Float32Array([
    x[0], y[0], z[0], 0,
    x[1], y[1], z[1], 0,
    x[2], y[2], z[2], 0,
    -vector3Dot(x, eye), -vector3Dot(y, eye), -vector3Dot(z, eye), 1
  ]);
}

function matPerspective(fov, aspect, near, far) {
  // Standard WebGL perspective matrix (column-major)
  const f = 1.0 / Math.tan((fov * Math.PI) / 360.0);
  const nf = 1 / (near - far);
  const out = new Float32Array(16);
  out[0] = f / aspect;
  out[1] = 0;
  out[2] = 0;
  out[3] = 0;

  out[4] = 0;
  out[5] = f;
  out[6] = 0;
  out[7] = 0;

  out[8] = 0;
  out[9] = 0;
  out[10] = (far + near) * nf;
  out[11] = -1;

  out[12] = 0;
  out[13] = 0;
  out[14] = (2 * far * near) * nf;
  out[15] = 0;
  return out;
}

function matMultiply(a, b) {
  // a, b are flat 16-element arrays
  const r = new Float32Array(16);
  for (let i = 0; i < 4; ++i) {
    for (let j = 0; j < 4; ++j) {
      r[i * 4 + j] = 0;
      for (let k = 0; k < 4; ++k) {
        r[i * 4 + j] += a[i * 4 + k] * b[k * 4 + j];
      }
    }
  }
  return r;
}

function matProjection(fov, near, far) {
  const scale = 1 / (Math.tan((fov / 2) * (Math.PI / 180)));
  const m = matCreate();
  m[0] = scale;
  m[5] = scale;
  m[10] = (far + near) / (near - far);
  m[14] = (2 * far * near) / (near - far);
  m[11] = -1;
  m[15] = 0;
  return m;
}

function matProjection2(fov, near, far) {
  const scale = 1 / (Math.tan((fov / 2) * (Math.PI / 180)));
  const m = matCreate();
  m[0] = scale;
  m[5] = scale;
  m[10] = -far / (far - near);
  m[14] = -far * near / (far - near);
  m[11] = -1;
  m[15] = 0;
  return m;
}

function matRotateY(angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return new Float32Array([
    c, 0, s, 0,
    0, 1, 0, 0,
    -s, 0, c, 0,
    0, 0, 0, 1
  ]);
}

function matScale(x, y, z) {
  const m = matCreate();
  m[0] = x;
  m[5] = y;
  m[10] = z;
  return m;
}

function matTranslate(x, y, z) {
  const m = matCreate();
  m[12] = x;
  m[13] = y;
  m[14] = z;
  return m;
}

function matTranspose(m) {
  const r = new Float32Array(16);
  for (let i = 0; i < 4; ++i) {
    for (let j = 0; j < 4; ++j) {
      r[i * 4 + j] = m[j * 4 + i];
    }
  }
  return r;
}

function vector3String(v) {
  return "[" + v[0].toFixed(2) + ", " + v[1].toFixed(2) + ", " + v[2].toFixed(2) + "]";
}

function vector3Add(a, b) {
  return [a[0] + b[0],
          a[1] + b[1],
          a[2] + b[2]];
}

function vector3Cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1],
          a[2] * b[0] - a[0] * b[2],
          a[0] * b[1] - a[1] * b[0]];
}

function vector3Dot(a, b) {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function vector3Mul(a, s) {
  return [a[0] * s,
          a[1] * s,
          a[2] * s];
}

function vector3Negate(a) {
  return [-a[0], -a[1], -a[2]];
}

function vector3Normalize(a) {
  const inv_mag = 1.0 / Math.sqrt(vector3Dot(a, a));
  return vector3Mul(a, inv_mag);
}

function vector3Sub(a, b) {
  return [a[0] - b[0],
          a[1] - b[1],
          a[2] - b[2]];
}