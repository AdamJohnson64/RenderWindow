import MetalKit

class Instance {
    var device: MTLDevice
    var material: Material
    var mesh: Mesh
    var matrixBuffer: MTLBuffer
    init(device: MTLDevice, material: Material, mesh: Mesh, uniforms: Shader.UniformsInstance) {
        self.device = device
        self.material = material
        self.mesh = mesh
        let uniformsSize = MemoryLayout<Shader.UniformsInstance>.size
        matrixBuffer = withUnsafeBytes(of: uniforms) { ptr in
            return device.makeBuffer(bytes: ptr.baseAddress!, length: uniformsSize, options: [])!
        }
    }
    func render(encoder: MTLRenderCommandEncoder) {
        encoder.setRenderPipelineState(material.pipeline!)
        // Bind the per-instance constants
        encoder.setVertexBuffer(matrixBuffer, offset: 0, index: 2)
        encoder.setFragmentBuffer(matrixBuffer, offset: 0, index: 2)
        mesh.render(cmd: encoder)
    }
}
