import simd

class Shader {

    struct Vertex {
        var position: simd_float3
        var normal: simd_float3
    }

    struct UniformsFrame {
        var viewProjection: simd_float4x4 = matrix_identity_float4x4
        var view: simd_float3 = simd_float3(0, 0, 0)
        var light: simd_float3 = simd_float3(0, 0, 0)
    }

    struct UniformsInstance {
        var model: simd_float4x4 = matrix_identity_float4x4
        var diffuse: simd_float3 = simd_float3(1, 0, 0)
    }

    static var source = """
#include <metal_stdlib>
using namespace metal;

// Vertex input and output structures
struct VertexIn {
    float3 position [[attribute(0)]];
    float3 normal   [[attribute(1)]];
};

struct VertexOut {
    float4 position [[position]];
    float3 normal;
    float3 world;
    float3 color;
};

// Uniforms for the frame and per-instance
struct UniformsFrame {
    float4x4 viewProjectionMatrix;
    float3 view;
    float3 light;
};

struct UniformsInstance {
    float4x4 modelMatrix;
    float3 diffuse;
};

// --- Helper Functions ---

// Compute attenuation based on distance
float computeAttenuation(float3 lightPos, float3 worldPos, float maxDist) {
    float dist = length(lightPos - worldPos);
    return clamp((maxDist - dist) / maxDist, 0.0, 1.0);
}

// Compute diffuse lighting
float3 computeDiffuse(float3 normal, float3 lightDir, float3 diffuseColor) {
    float factor = max(dot(normal, lightDir), 0.0);
    return diffuseColor * factor;
}

// Compute specular lighting
float3 computeSpecular(float3 normal, float3 lightDir, float3 viewDir, float shininess, float3 specularColor) {
    float3 reflectDir = reflect(-lightDir, normal);
    float factor = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    return specularColor * factor;
}

// Visualize normal as color
float3 visualizeNormal(float3 norm) {
    return (norm + 1.0) * 0.5;
}

// --- Vertex Shader Helper ---

VertexOut calculateDefaults(VertexIn in, constant UniformsFrame& frame, constant UniformsInstance& instance) {
    VertexOut out;
    float4 worldPos = instance.modelMatrix * float4(in.position, 1.0);
    out.position = frame.viewProjectionMatrix * worldPos;
    out.normal = in.normal;
    out.world = worldPos.xyz;
    out.color = instance.diffuse;
    return out;
}

// --- Shaders ---

vertex VertexOut vs_flat(VertexIn in [[stage_in]],
                        constant UniformsFrame& frame [[buffer(1)]],
                        constant UniformsInstance& instance [[buffer(2)]]) {
    return calculateDefaults(in, frame, instance);
}

fragment float4 fs_flat(VertexOut in [[stage_in]],
                        constant UniformsFrame& frame [[buffer(1)]],
                        constant UniformsInstance& instance [[buffer(2)]]) {
    float3 normal = normalize(in.normal);
    float3 lightDir = normalize(frame.light - in.world);
    float attenuation = computeAttenuation(frame.light, in.world, 50.0);
    float3 color = computeDiffuse(normal, lightDir, in.color) * attenuation;
    return float4(color, 1.0);
}

vertex VertexOut vs_normal(VertexIn in [[stage_in]],
                           constant UniformsFrame& frame [[buffer(1)]],
                           constant UniformsInstance& instance [[buffer(2)]]) {
    return calculateDefaults(in, frame, instance);
}

fragment float4 fs_normal(VertexOut in [[stage_in]],
                          constant UniformsFrame& frame [[buffer(1)]],
                          constant UniformsInstance& instance [[buffer(2)]]) {
    float attenuation = computeAttenuation(frame.light, in.world, 50.0);
    float3 color = visualizeNormal(normalize(in.normal));
    return float4(color * attenuation, 1.0);
}

vertex VertexOut vs_shiny(VertexIn in [[stage_in]],
                          constant UniformsFrame& frame [[buffer(1)]],
                          constant UniformsInstance& instance [[buffer(2)]]) {
    return calculateDefaults(in, frame, instance);
}

fragment float4 fs_shiny(VertexOut in [[stage_in]],
                         constant UniformsFrame& frame [[buffer(1)]],
                         constant UniformsInstance& instance [[buffer(2)]]) {
    float3 normal = normalize(in.normal);
    float3 lightDir = normalize(frame.light - in.world);
    float3 viewDir = normalize(-frame.view);
    float attenuation = computeAttenuation(frame.light, in.world, 50.0);
    float3 diffuse = computeDiffuse(normal, lightDir, in.color);
    float3 specular = computeSpecular(normal, lightDir, viewDir, 10.0, float3(1, 1, 1));
    float3 color = (diffuse + specular) * attenuation;
    return float4(color, 1.0);
}
"""
}
