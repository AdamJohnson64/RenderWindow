///////////////////////////////////////////////////////////////////////////////
//Default Shaders

const glShaderVertex = `#version 300 es
precision highp float;

layout(location = 0) in vec3 inPos;
layout(location = 1) in vec3 inNor;
layout(location = 2) in vec2 inST0;
out vec3 outPos;
out vec3 outNor;
out vec2 outST0;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 modelview;
uniform mat4 viewprojection;
uniform mat4 modelviewprojection;
uniform vec3 eye;
uniform float time;

void main(void) {
  gl_Position = modelviewprojection * vec4(inPos, 1.0);
  outPos = (model * vec4(inPos, 1.0)).xyz;
  outNor = normalize(mat3(model) * inNor);
  outST0 = inST0;
}`;

const glShaderFragmentLit = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;
out vec4 outCol;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 modelview;
uniform mat4 viewprojection;
uniform mat4 modelviewprojection;
uniform vec3 eye;
uniform float time;

uniform sampler2D Albedo;
uniform sampler2D Height;

void main(void) {
  float dotL = clamp(dot(outNor, vec3(0.0, 1.0, 0.0)), 0.0, 1.0);
  float illumination = clamp(dotL, 0.25, 1.0);
  outCol = vec4(texture(Albedo, outST0).rgb * illumination, 1.0);
}`;

const glShaderFragment = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;
out vec4 outCol;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 modelview;
uniform mat4 viewprojection;
uniform mat4 modelviewprojection;
uniform vec3 eye;
uniform float time;

uniform sampler2D Albedo;
uniform sampler2D Height;

void main(void) {
  // Reconstruct TBN using screen-space derivatives
  vec3 dpdx = dFdx(outPos);
  vec3 dpdy = dFdy(outPos);
  vec2 dstdx = dFdx(outST0);
  vec2 dstdy = dFdy(outST0);
  vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  mat3 TBN = mat3(tangent, bitangent, normalize(outNor));

  // View direction in tangent space
  vec3 viewDir = normalize(eye - outPos);
  vec3 viewDirTS = normalize(transpose(TBN) * viewDir);

  // Relief mapping parameters
  float heightScale = 0.1;
  int numSteps = 32;
  float layerDepth = 1.0 / float(numSteps);
  float currentLayerDepth = 0.0;
  vec2 P = viewDirTS.xy * heightScale;
  vec2 deltaTexCoord = -P / float(numSteps);
  vec2 currentTexCoord = outST0;
  float currentDepthMapValue = texture(Height, currentTexCoord).r;

  // Linear search for intersection
  int steps = numSteps;
  while(currentLayerDepth < currentDepthMapValue && steps > 0) {
    currentTexCoord += deltaTexCoord;
    currentDepthMapValue = texture(Height, currentTexCoord).r;
    currentLayerDepth += layerDepth;
    steps--;
  }

  // Clamp to texture bounds
  currentTexCoord = clamp(currentTexCoord, vec2(0.0), vec2(1.0));

  // Lighting (simple diffuse)
  vec3 lightDir = normalize(vec3(0.0, 1.0, 0.0));
  float dotL = clamp(dot(outNor, lightDir), 0.0, 1.0);
  float illumination = clamp(dotL, 0.25, 1.0);

  // Ambient
  float ambient = 0.3;
  illumination = max(illumination, ambient);

  outCol = vec4(texture(Albedo, currentTexCoord).rgb * illumination, 1.0);
}`;

const glShaderFragmentRelaxedCone = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;
out vec4 outCol;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 modelview;
uniform mat4 viewprojection;
uniform mat4 modelviewprojection;
uniform vec3 eye;
uniform float time;

uniform sampler2D Albedo;
uniform sampler2D Height;

void main(void) {
  // Reconstruct TBN using screen-space derivatives
  vec3 dpdx = dFdx(outPos);
  vec3 dpdy = dFdy(outPos);
  vec2 dstdx = dFdx(outST0);
  vec2 dstdy = dFdy(outST0);
  vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  mat3 TBN = mat3(tangent, bitangent, normalize(outNor));

  // View direction in tangent space
  vec3 viewDir = normalize(eye - outPos);
  vec3 viewDirTS = normalize(transpose(TBN) * viewDir);

  // Relaxed cone relief mapping parameters
  float heightScale = 0.1;
  int numSteps = 64;
  float minStep = 0.01;
  float maxStep = 1.0 / float(numSteps);
  float currentLayerDepth = 0.0;
  float currentDepthMapValue = 0.0;
  vec2 P = viewDirTS.xy * heightScale;
  vec2 deltaTexCoord = -P;
  vec2 currentTexCoord = outST0;

  // Initial sample
  currentDepthMapValue = texture(Height, currentTexCoord).r;

  // Relaxed cone search
  float coneStep = maxStep;
  for (int i = 0; i < numSteps; ++i) {
    float height = texture(Height, currentTexCoord).r;
    if (currentLayerDepth >= height) {
      break;
    }
    // Relaxed cone: step size increases with distance from viewer
    coneStep = mix(maxStep, minStep, currentLayerDepth);
    currentTexCoord += deltaTexCoord * coneStep * 2.0; // take a larger step
    currentLayerDepth += coneStep;
  }

  // Clamp to texture bounds
  currentTexCoord = clamp(currentTexCoord, vec2(0.0), vec2(1.0));

  // Lighting (simple diffuse)
  vec3 lightDir = normalize(vec3(0.0, 1.0, 0.0));
  float dotL = clamp(dot(outNor, lightDir), 0.0, 1.0);
  float illumination = clamp(dotL, 0.25, 1.0);

  // Ambient
  float ambient = 0.3;
  illumination = max(illumination, ambient);

  outCol = vec4(texture(Albedo, currentTexCoord).rgb * illumination, 1.0);
}`;

///////////////////////////////////////////////////////////////////////////////
//Debug Shaders

const glShaderFragmentBitangent = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out vec4 FragColor;

void main(void) {
  vec3 dpdx = dFdx(outPos);
  vec3 dpdy = dFdy(outPos);
  vec2 dstdx = dFdx(outST0);
  vec2 dstdy = dFdy(outST0);
  vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  FragColor = vec4((bitangent + 1.0) / 2.0, 1.0);
}`;

const glShaderFragmentNormal = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out vec4 FragColor;

void main(void) {
  FragColor = vec4((outNor + 1.0) / 2.0, 1.0);
}`;

const glShaderFragmentTangent = `#version 300 es
precision highp float;

in vec3 outPos;
in vec3 outNor;
in vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out vec4 FragColor;

void main(void) {
  vec3 dpdx = dFdx(outPos);
  vec3 dpdy = dFdy(outPos);
  vec2 dstdx = dFdx(outST0);
  vec2 dstdy = dFdy(outST0);
  vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  FragColor = vec4((tangent + 1.0) / 2.0, 1.0);
}`;

function glCompileShader(type, code, name) {
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

function glCompileProgram(code_vertex, code_fragment) {
  const id_program = gl.createProgram();
  const id_shader_vertex = glCompileShader(gl.VERTEX_SHADER, code_vertex, "Vertex");
  const id_shader_fragment = glCompileShader(gl.FRAGMENT_SHADER, code_fragment, "Fragment");
  gl.attachShader(id_program, id_shader_vertex);
  gl.attachShader(id_program, id_shader_fragment);
  gl.linkProgram(id_program);
  return id_program;
}