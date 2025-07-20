import MetalKit

struct Mesh {
    var vertex: MTLBuffer
    var index: MTLBuffer
    var indexCount: Int
    init(device: MTLDevice, shape: (simd_float2) -> simd_float3, u: Int, v: Int ) {
        vertex = Mesh.generateBufferVertices(device:device, function: shape, u:u, v:v)
        index = Mesh.generateBufferIndices(device:device, u:u, v:v)
        indexCount = 6 * u * v;
    }
    static func generateBufferVertices(device: MTLDevice, function: (simd_float2) -> simd_float3, u: Int, v: Int) -> MTLBuffer {
        let data = generateParametricPositions(function:function, u:u, v:v)
        let buffer = device.makeBuffer(
            bytes: data,
            length: MemoryLayout<Shader.Vertex>.stride * data.count,
            options: .storageModeShared)!
        return buffer
    }
    static func generateBufferIndices(device: MTLDevice, u: Int, v: Int) -> MTLBuffer {
        let data = generateParametricIndices(u: u, v: v)
        let buffer = device.makeBuffer(
            bytes: data,
            length: MemoryLayout<UInt16>.stride * data.count,
            options: .storageModeShared)!
        return buffer
    }
    func render(cmd: MTLRenderCommandEncoder) {
        // Bind the vertices
        cmd.setVertexBuffer(vertex, offset: 0, index: 0)
        // Draw the whole mesh
        cmd.drawIndexedPrimitives(
            type: .triangle,
            indexCount: indexCount,
            indexType: .uint16,
            indexBuffer: index,
            indexBufferOffset: 0)
    }
}
