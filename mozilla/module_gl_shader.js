const glShaderVertex = `#version 300 es
layout(location = 0) in vec3 inPos;
layout(location = 1) in vec3 inNor;
layout(location = 2) in vec2 inST0;
out highp vec3 outPos;
out highp vec3 outNor;
out highp vec2 outST0;

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
  outNor = inNor;
  outST0 = inST0;
}`;

const glShaderFragment = `#version 300 es
in highp vec3 outPos;
in highp vec3 outNor;
in highp vec2 outST0;
out highp vec4 outCol;

uniform highp mat4 model;
uniform highp mat4 view;
uniform highp mat4 projection;
uniform highp mat4 modelview;
uniform highp mat4 viewprojection;
uniform highp mat4 modelviewprojection;
uniform highp vec3 eye;
uniform highp float time;

uniform sampler2D Albedo;
uniform sampler2D Height;

void main(void) {
  // Calculate TBN matrix
  highp vec3 dpdx = dFdx(outPos);
  highp vec3 dpdy = dFdy(outPos);
  highp vec2 dstdx = dFdx(outST0);
  highp vec2 dstdy = dFdy(outST0);
  highp vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  highp vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  highp mat3 TBN = mat3(tangent, bitangent, normalize(outNor));
  
  // Calculate view direction in tangent space
  highp vec3 viewDir = normalize(eye - outPos);
  highp vec3 tangentViewDir = normalize(TBN * viewDir);
  
  // Relief mapping parameters
  highp float heightScale = 0.1;
  highp float maxSteps = 32.0;
  
  // Simple parallax mapping (more reliable than complex POM)
  highp float height = texture(Height, outST0).r;
  highp vec2 texCoord = outST0 - tangentViewDir.xy * height * heightScale;
  
  // Check if we're outside the texture bounds and clamp
  if(texCoord.x > 1.0 || texCoord.y > 1.0 || texCoord.x < 0.0 || texCoord.y < 0.0) {
    // Fallback to original coordinates if out of bounds
    texCoord = outST0;
  }
  
  // Lighting calculation with proper normal
  highp vec3 lightDir = normalize(vec3(0.0, 1.0, 0.0));
  highp float dotL = clamp(dot(outNor, lightDir), 0.0, 1.0);
  highp float illumination = clamp(dotL, 0.25, 1.0);
  
  // Add ambient lighting
  highp float ambient = 0.3;
  illumination = max(illumination, ambient);
  
  outCol = vec4(texture(Albedo, texCoord).rgb * illumination, 1.0);
}`;

const glShaderFragment2 = `#version 300 es
in highp vec3 outPos;
in highp vec3 outNor;
in highp vec2 outST0;
out highp vec4 outCol;

uniform highp mat4 model;
uniform highp mat4 view;
uniform highp mat4 projection;
uniform highp mat4 modelview;
uniform highp mat4 viewprojection;
uniform highp mat4 modelviewprojection;
uniform highp vec3 eye;
uniform highp float time;

uniform sampler2D Albedo;
uniform sampler2D Height;

void main(void) {
  highp float dotL = clamp(dot(outNor, vec3(0.0, 1.0, 0.0)), 0.0, 1.0);
  highp float illumination = clamp(dotL, 0.25, 1.0);
  outCol = vec4(texture(Albedo, outST0).rgb * illumination, 1.0);
}`;

const glShaderFragmentBitangent = `#version 300 es
in highp vec3 outPos;
in highp vec3 outNor;
in highp vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out highp vec4 FragColor;

void main(void) {
  highp vec3 dpdx = dFdx(outPos);
  highp vec3 dpdy = dFdy(outPos);
  highp vec2 dstdx = dFdx(outST0);
  highp vec2 dstdy = dFdy(outST0);
  highp vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  highp vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
  FragColor = vec4((bitangent + 1.0) / 2.0, 1.0);
}`;

const glShaderFragmentNormal = `#version 300 es
in highp vec3 outPos;
in highp vec3 outNor;
in highp vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out highp vec4 FragColor;

void main(void) {
  FragColor = vec4((outNor + 1.0) / 2.0, 1.0);
}`;

const glShaderFragmentTangent = `#version 300 es
in highp vec3 outPos;
in highp vec3 outNor;
in highp vec2 outST0;

uniform sampler2D Albedo;
uniform sampler2D Height;

out highp vec4 FragColor;

void main(void) {
  highp vec3 dpdx = dFdx(outPos);
  highp vec3 dpdy = dFdy(outPos);
  highp vec2 dstdx = dFdx(outST0);
  highp vec2 dstdy = dFdy(outST0);
  highp vec3 tangent = normalize(dpdx * dstdy.y - dpdy * dstdx.y);
  highp vec3 bitangent = normalize(-dpdx * dstdy.x + dpdy * dstdx.x);
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