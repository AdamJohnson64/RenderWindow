import MetalKit

class Material {
    var library: MTLLibrary? = nil
    var pipeline: MTLRenderPipelineState? = nil
    init(device: MTLDevice, name: String) {
        // Load Metal shaders
        do { library = try device.makeLibrary(source: Shader.source, options: nil) }
        catch { fatalError("Failed to create shader library: \(error)") }
        // Create a pipeline descriptor for this shader
        let descriptor = Material.getRenderPipelineDescriptor(library: library!, name: name)
        do { pipeline = try device.makeRenderPipelineState(descriptor: descriptor) }
        catch { fatalError("Failed to create pipeline state: \(error)") }
    }
    static func getRenderPipelineDescriptor(library: MTLLibrary, name: String) -> MTLRenderPipelineDescriptor {
        let desc = MTLRenderPipelineDescriptor()
        desc.vertexFunction = library.makeFunction(name: "vs_" + name)
        desc.fragmentFunction = library.makeFunction(name: "fs_" + name)
        desc.vertexDescriptor = getVertexDescriptor()
        desc.colorAttachments[0].pixelFormat = .bgra8Unorm
        desc.depthAttachmentPixelFormat = .depth32Float
        return desc
    }
    static func getVertexDescriptor() -> MTLVertexDescriptor {
        let desc = MTLVertexDescriptor()
        desc.attributes[0].format = .float3
        desc.attributes[0].offset = 0
        desc.attributes[0].bufferIndex = 0
        desc.attributes[1].format = .float3
        desc.attributes[1].offset = MemoryLayout<simd_float3>.stride
        desc.attributes[1].bufferIndex = 0
        desc.layouts[0].stride = MemoryLayout<Shader.Vertex>.stride
        desc.layouts[0].stepRate = 1
        desc.layouts[0].stepFunction = .perVertex
        return desc
    }
}
