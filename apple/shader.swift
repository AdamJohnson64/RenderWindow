import simd

class Shader {

    struct Vertex {
        var position: simd_float3
        var normal: simd_float3
    }

    struct UniformsFrame {
        var viewProjection: simd_float4x4 = matrix_identity_float4x4
        var view: simd_float3 = simd_float3(0, 0, 0)
    }

    struct UniformsInstance {
        var model: simd_float4x4 = matrix_identity_float4x4
        var diffuse: simd_float3 = simd_float3(1, 0, 0)
    }

    static var source = """
#include <metal_stdlib>
using namespace metal;

struct VertexIn {
    float3 position [[attribute(0)]];
    float3 normal   [[attribute(1)]];
};

struct VertexOut {
    float4 position [[position]];
    float3 normal;
};

struct UniformsFrame {
    float4x4 viewProjectionMatrix;
    float3 view;
};

struct UniformsInstance {
    float4x4 modelMatrix;
    float3 diffuse;
};

float3 computeDiffuse(float3 normal, float3 lightDir, float3 diffuseColor) {
    float factor = dot(normal, lightDir);
    factor = clamp(factor, 0.0, 1.0);
    return diffuseColor * factor;
}

float3 computeSpecular(float3 normal, float3 lightDir, float3 viewDir, float shininess, float3 specularColor) {
    float3 reflectDir = reflect(-lightDir, normal);
    float factor = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    factor = clamp(factor, 0.0, 1.0);
    return specularColor * factor;
}

float3 visualizeNormal(float3 norm) {
    norm.x = (norm.x + 1) / 2;
    norm.y = (norm.y + 1) / 2;
    norm.z = (norm.z + 1) / 2;
    return norm;
}

vertex VertexOut vs_flat(
        VertexIn in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    VertexOut out;
    out.position = frame.viewProjectionMatrix * instance.modelMatrix * float4(in.position, 1.0);
    float3 light = normalize(float3(1,1,1));
    float3 normal = normalize(in.normal);
    out.normal = computeDiffuse(normal, light, instance.diffuse);
    return out;
}

fragment float4 fs_flat(
        VertexOut in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    return float4(in.normal, 1.0);
}

vertex VertexOut vs_normal(
        VertexIn in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    VertexOut out;
    out.position = frame.viewProjectionMatrix * instance.modelMatrix * float4(in.position, 1.0);
    out.normal = visualizeNormal(in.normal);
    return out;
}

fragment float4 fs_normal(
        VertexOut in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    return float4(in.normal, 1.0);
}

vertex VertexOut vs_shiny(
        VertexIn in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    VertexOut out;
    out.position = frame.viewProjectionMatrix * instance.modelMatrix * float4(in.position, 1.0);
    float3 normal = normalize(in.normal);
    float3 light = normalize(float3(1,1,1));
    float3 diffuse = instance.diffuse;
    float3 specular = float3(1, 1, 1);
    out.normal =
        computeDiffuse(normal, light, diffuse)
        + computeSpecular(normal, light, -frame.view, 10.00, specular);
    return out;
}

fragment float4 fs_shiny(
        VertexOut in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    return float4(in.normal, 1.0);
}
"""
}
