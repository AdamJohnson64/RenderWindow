// Linear algebra and matrix utilities for 3D graphics

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
  // TODO: Implement full inversion
  for (let i = 0; i < 16; ++i) inv[i] = (i % 5 === 0) ? 1 : 0;
  return inv;
}

function matLookAt(eye, center, up) {
  // Standard right-handed lookAt matrix
  const f = vector3Normalize(vector3Sub(center, eye)); // forward
  const s = vector3Normalize(vector3Cross(f, up));     // right (side)
  const u = vector3Cross(s, f);                        // up

  return new Float32Array([
    s[0],  u[0],  -f[0],  0,
    s[1],  u[1],  -f[1],  0,
    s[2],  u[2],  -f[2],  0,
    -vector3Dot(s, eye), -vector3Dot(u, eye), vector3Dot(f, eye), 1
  ]);
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
  // Perspective projection, aspect ratio = 1
  const f = 1 / Math.tan((fov / 2) * (Math.PI / 180));
  const m = matCreate();
  m[0] = f;
  m[5] = f;
  m[10] = (far + near) / (near - far);
  m[11] = -1;
  m[14] = (2 * far * near) / (near - far);
  m[15] = 0;
  return m;
}

function matPerspective(fov, aspect, near, far) {
  // Standard perspective projection with aspect ratio
  const f = 1 / Math.tan((fov / 2) * (Math.PI / 180));
  const m = new Float32Array(16);
  m[0] = f / aspect;
  m[1] = 0;
  m[2] = 0;
  m[3] = 0;

  m[4] = 0;
  m[5] = f;
  m[6] = 0;
  m[7] = 0;

  m[8] = 0;
  m[9] = 0;
  m[10] = (far + near) / (near - far);
  m[11] = -1;

  m[12] = 0;
  m[13] = 0;
  m[14] = (2 * far * near) / (near - far);
  m[15] = 0;
  return m;
}

function matProjection2(fov, near, far) {
  // Alternate projection (left-handed)
  const scale = 1 / (Math.tan((fov / 2) * (Math.PI / 180)));
  const m = matCreate();
  m[0] = scale;
  m[5] = scale;
  m[10] = -far / (far - near);
  m[11] = -1;
  m[14] = -far * near / (far - near);
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

// Vector utilities
function vector3String(v) {
  return `[${v[0].toFixed(2)}, ${v[1].toFixed(2)}, ${v[2].toFixed(2)}]`;
}

function vector3Add(a, b) {
  return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
}

function vector3Sub(a, b) {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function vector3Mul(a, s) {
  return [a[0] * s, a[1] * s, a[2] * s];
}

function vector3Dot(a, b) {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function vector3Cross(a, b) {
  return [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0]
  ];
}

function vector3Negate(a) {
  return [-a[0], -a[1], -a[2]];
}

function vector3Normalize(a) {
  const invMag = 1.0 / Math.sqrt(vector3Dot(a, a));
  return vector3Mul(a, invMag);
}