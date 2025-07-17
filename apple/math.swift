import Foundation
import simd

func simd_float4x4_lookAt(eye: simd_float3, center: simd_float3, up: simd_float3) -> simd_float4x4 {
    let f = simd_normalize(center - eye)
    let s = simd_normalize(simd_cross(f, up))
    let u = simd_cross(s, f)
    let col0 = simd_float4(s.x, u.x, -f.x, 0.0)
    let col1 = simd_float4(s.y, u.y, -f.y, 0.0)
    let col2 = simd_float4(s.z, u.z, -f.z, 0.0)
    let col3 = simd_float4(-simd_dot(s, eye), -simd_dot(u, eye), simd_dot(f, eye), 1.0)
    return simd_float4x4(col0, col1, col2, col3)
}

func simd_float4x4_perspective(fovyRadians: Float, aspect: Float, near: Float, far: Float) -> simd_float4x4 {
    let f = 1.0 / tan(fovyRadians / 2.0)
    let nf = 1.0 / (near - far)
    var m = simd_float4x4()
    m.columns = (
        simd_float4(f / aspect, 0, 0, 0),
        simd_float4(0, f, 0, 0),
        simd_float4(0, 0, (far + near) * nf, -1),
        simd_float4(0, 0, (2 * far * near) * nf, 0)
    )
    return m
}

func simd_float4x4_scale(_ s: simd_float3) -> simd_float4x4 {
    var m = matrix_identity_float4x4
    m.columns.0.x = s.x
    m.columns.1.y = s.y
    m.columns.2.z = s.z
    return m
}

func simd_float4x4_scale(_ x: Float, _ y: Float, _ z: Float) -> simd_float4x4 {
    var m = matrix_identity_float4x4
    m.columns.0.x = x
    m.columns.1.y = y
    m.columns.2.z = z
    return m
}

func simd_float4x4_translate(_ t: simd_float3) -> simd_float4x4 {
    var m = matrix_identity_float4x4
    m.columns.3 = simd_float4(t, 1.0)
    return m
}

func simd_float4x4_translate(_ x: Float, _ y: Float, _ z: Float) -> simd_float4x4 {
    var m = matrix_identity_float4x4
    m.columns.3 = SIMD4<Float>(x, y, z, 1.0)
    return m
}
