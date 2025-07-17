import MetalKit
import simd

struct Mesh {
    var vertex: MTLBuffer
    var index: MTLBuffer
    var index_count: Int
    init(device: MTLDevice, shape: (simd_float2) -> simd_float3, u: Int, v: Int ) {
        vertex = Mesh.generateBufferVertices(device:device, function: shape, u:u, v:v)
        index = Mesh.generateBufferIndices(device:device, u:u, v:v)
        index_count = 6 * u * v;
    }
    static func generateBufferVertices(device: MTLDevice, function: (simd_float2) -> simd_float3, u: Int, v: Int) -> MTLBuffer {
        let data = generateParametricPositions(function:function, u:u, v:v)
        let buffer = device.makeBuffer(
            bytes: data,
            length: MemoryLayout<Vertex>.stride * data.count,
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
            indexCount: index_count,
            indexType: .uint16,
            indexBuffer: index,
            indexBufferOffset: 0)
    }}

struct Vertex {
    var position: simd_float3
    var normal: simd_float3
}

class Material {
    var library: MTLLibrary? = nil
    var pipeline: MTLRenderPipelineState? = nil
    init(device: MTLDevice) {
        // Load Metal shaders
        do { library = try device.makeLibrary(source: Material.getShaderSource(), options: nil) }
        catch { fatalError("Failed to create shader library: \(error)") }
        // Create a pipeline descriptor for this shader
        let descriptor = Material.getRenderPipelineDescriptor(library: library!)
        do { pipeline = try device.makeRenderPipelineState(descriptor: descriptor) }
        catch { fatalError("Failed to create pipeline state: \(error)") }
    }
    static func getShaderSource() -> String {
return """
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
};

struct UniformsInstance {
    float4x4 modelMatrix;
};

vertex VertexOut vertex_main(
        VertexIn in [[stage_in]],
        constant UniformsFrame& frame [[buffer(1)]],
        constant UniformsInstance& instance [[buffer(2)]]
        ) {
    VertexOut out;
    out.position = frame.viewProjectionMatrix * instance.modelMatrix * float4(in.position, 1.0);
    float4 norm = float4(in.normal, 0.0);
    norm.x = (norm.x + 1) / 2;
    norm.y = (norm.y + 1) / 2;
    norm.z = (norm.z + 1) / 2;
    out.normal = float3(norm.x, norm.y, norm.z);
    return out;
}

fragment float4 fragment_main(VertexOut in [[stage_in]]) {
    return float4(in.normal, 1.0);
}
"""
    }
    static func getRenderPipelineDescriptor(library: MTLLibrary) -> MTLRenderPipelineDescriptor {
        let desc = MTLRenderPipelineDescriptor()
        desc.vertexFunction = library.makeFunction(name: "vertex_main")
        desc.fragmentFunction = library.makeFunction(name: "fragment_main")
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
        desc.layouts[0].stride = MemoryLayout<Vertex>.stride
        desc.layouts[0].stepRate = 1
        desc.layouts[0].stepFunction = .perVertex
        return desc
    }
}

class Instance {
    var device: MTLDevice
    var material: Material
    var mesh: Mesh
    var matrixBuffer: MTLBuffer
    init(device: MTLDevice, material: Material, mesh: Mesh, m: simd_float4x4) {
        self.device = device
        self.material = material
        self.mesh = mesh
        let matrixSize = MemoryLayout<simd_float4x4>.size
        matrixBuffer = withUnsafeBytes(of: m) { ptr in
            return device.makeBuffer(bytes: ptr.baseAddress!, length: matrixSize, options: [])!
        }
    }
    func render(encoder: MTLRenderCommandEncoder) {
        encoder.setRenderPipelineState(material.pipeline!)
        encoder.setVertexBuffer(matrixBuffer, offset: 0, index: 2)
        mesh.render(cmd: encoder)
    }
}

class Sample {
    var device: MTLDevice
    var state_depth: MTLDepthStencilState
    var instances: [Instance] = []
    var frame: Float = 0
    init(device: MTLDevice) {
        self.device = device;
        // Prepare the depth stencil state
        let desc_depth = MTLDepthStencilDescriptor()
        desc_depth.depthCompareFunction = .less
        desc_depth.isDepthWriteEnabled = true
        self.state_depth = device.makeDepthStencilState(descriptor: desc_depth)!
        // Create the scene
        let material = Material(device: device)
        let mesh_plane = Mesh(device: device, shape: plane, u: 20, v: 20)
        let mesh_sphere = Mesh(device: device, shape: sphere, u: 20, v: 20)
        // Add in a plane
        let mat_translate = simd_float4x4_translate(0, -5, 0)
        let mat_scale = simd_float4x4_scale(100, 1, 100)
        let mat = mat_translate * mat_scale;
        let instance = Instance(device: device, material: material, mesh: mesh_plane, m: mat)
        instances.append(instance)
        // Add in a bunch of spheres
        for y in -5...5 {
            for x in -5...5 {
                let instance = Instance(device: device, material: material, mesh: mesh_sphere, m: simd_float4x4_translate(Float(x), Float(y), 0))
                instances.append(instance);
            }
        }
    }
    func render(encoder: MTLRenderCommandEncoder) {
        // Setup the view*projection matrix
        let matrix_view = simd_float4x4_lookAt(eye:[10 * cos(frame),0,5 * sin(frame)], center:[0,0,0], up:[0,1,0])
        let matrix_projection = simd_float4x4_perspective(fovyRadians:(90.0 / 360.0) * (.pi * 2), aspect:1, near:0.001, far:100.0);
        let matrix = matrix_projection * matrix_view
        let matrixSize = MemoryLayout<simd_float4x4>.size
        let matrixBuffer = withUnsafeBytes(of: matrix) { ptr in
            return device.makeBuffer(bytes: ptr.baseAddress!, length: matrixSize, options: [])! }
        // Start encoding the render command buffer
        encoder.setDepthStencilState(state_depth)
        encoder.setVertexBuffer(matrixBuffer, offset: 0, index: 1)
        // Render instances
        for i in instances {
            i.render(encoder: encoder);
        }
        frame = frame + 0.01
    }
}

class MTKViewDelegateImpl: NSObject, MTKViewDelegate {
    var sample: Sample? = nil
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
    }
    func draw(in view: MTKView) {
        if (sample == nil) {
            sample = Sample(device: view.device!)
        }
        view.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        let queue = view.device?.makeCommandQueue()
        let command = queue?.makeCommandBuffer()
        let pass = view.currentRenderPassDescriptor
        let encoder = command?.makeRenderCommandEncoder(descriptor:pass!)
        sample!.render(encoder: encoder!)
        encoder?.endEncoding()
        command?.present(view.currentDrawable!)
        command?.commit()
    }
}

func setupMTKView(view: MTKView, delegate: MTKViewDelegate) {
    view.delegate = delegate
    view.device = MTLCreateSystemDefaultDevice()
    view.isPaused = false
    view.preferredFramesPerSecond = 60
    view.depthStencilPixelFormat = .depth32Float;
}
