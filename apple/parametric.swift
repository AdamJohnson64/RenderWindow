import Foundation
import simd

func generateNormal(function: (simd_float2) -> simd_float3, uv: simd_float2) -> simd_float3 {
    let du = function(simd_float2(uv.x - 0.01, uv.y))
    - function(simd_float2(uv.x + 0.001, uv.y));
    let dv = function(simd_float2(uv.x, uv.y - 0.01))
    - function(simd_float2(uv.x, uv.y + 0.01))
    return simd_normalize(simd_cross(du, dv))
}

func generateParametricPositions(function: (simd_float2) -> simd_float3, u: Int, v: Int) -> [Vertex] {
    var vertices = Array(
        repeating: Vertex(
            position: simd_float3(repeating: 0),
            normal: simd_float3(repeating: 0)),
        count: 0);
    for iv in 0...v {
        for iu in 0...u {
            let uv = simd_float2(Float(iu) / Float(u), Float(iv) / Float(v))
            let normal = generateNormal(function: function, uv: uv)
            vertices.append(Vertex(
                position: function(uv),
                normal: simd_float3(normal)))
                    //Float.random(in:0..<1), Float.random(in:0..<1), Float.random(in:0..<1))))
        }
    }
    return vertices
}

func generateParametricIndices(u: Int, v: Int) -> [UInt16] {
    var indices = Array(repeating: UInt16(0), count: 0);
    for iv in 0...(v-1) {
        for iu in 0...(u-1) {
            indices.append(UInt16((iu + 0) + (iv + 0) * (u + 1)));
            indices.append(UInt16((iu + 1) + (iv + 0) * (u + 1)));
            indices.append(UInt16((iu + 0) + (iv + 1) * (u + 1)));
            indices.append(UInt16((iu + 0) + (iv + 1) * (u + 1)));
            indices.append(UInt16((iu + 1) + (iv + 0) * (u + 1)));
            indices.append(UInt16((iu + 1) + (iv + 1) * (u + 1)));
        }
    }
    return indices;
}

func plane(uv: simd_float2) -> simd_float3 {
    return simd_float3(uv.x - 0.5, 0, 0.5 - uv.y)
}

func sphere(uv: simd_float2) -> simd_float3 {
    let angle_u = (2 * .pi) * uv.x;
    let angle_v = (1 * .pi) * uv.y;
    let scale = sin(angle_v);
    return [cos(angle_u) * scale,
            cos(angle_v),
            sin(angle_u) * scale];
}
