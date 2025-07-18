import MetalKit
import simd

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
    }}

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

class MTKViewDelegateImpl : NSObject, MTKViewDelegate {
    var device: MTLDevice
    var stateDepth: MTLDepthStencilState
    var instances: [Instance] = []
    var aspect: Float = 1
    var frame: Float = 0
    init(device: MTLDevice) {
        self.device = device;
        // Prepare the depth stencil state
        let desc = MTLDepthStencilDescriptor()
        desc.depthCompareFunction = .less
        desc.isDepthWriteEnabled = true
        self.stateDepth = device.makeDepthStencilState(descriptor: desc)!
        // Create the scene
        let materialFlat = Material(device: device, name: "flat")
        let materialNormal = Material(device: device, name: "normal")
        let materialShiny = Material(device: device, name: "shiny")
        let meshPlane = Mesh(device: device, shape: plane, u: 1, v: 1)
        let meshSphere = Mesh(device: device, shape: sphere, u: 50, v: 50)
        // Add in a coordinate reference
        var uniformsInstance = Shader.UniformsInstance()
        // Add in a plane
        uniformsInstance.diffuse = simd_float3(0, 1, 0)
        uniformsInstance.model = simd_float4x4_translate(0, -6, 0) * simd_float4x4_scale(100, 1, 100)
        instances.append(Instance(device: device, material: materialFlat, mesh: meshPlane, uniforms: uniformsInstance))
        // Add in axis guides
        uniformsInstance.diffuse = simd_float3(1, 0, 0)
        uniformsInstance.model = simd_float4x4_translate(10, 0, 0)
        instances.append(Instance(device: device, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        uniformsInstance.model = simd_float4x4_translate(0, 10, 0)
        instances.append(Instance(device: device, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        uniformsInstance.model = simd_float4x4_translate(0, 0, 10)
        instances.append(Instance(device: device, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        // Add in a bunch of spheres
        for z in -5...5 {
            for y in -5...5 {
                for x in -5...5 {
                    uniformsInstance.diffuse = simd_float3((Float(x) + 5.0) / 10.0, (Float(y) + 5.0) / 10.0, (Float(z) + 5.0) / 10.0)
                    uniformsInstance.model = simd_float4x4_translate(Float(x), Float(y), Float(z))
                    let instance = Instance(device: device, material: materialShiny, mesh: meshSphere, uniforms: uniformsInstance)
                    instances.append(instance);
                }
            }
        }
    }
    // MTKViewDelegate Implementation
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        aspect = Float(size.height) / Float(size.width)
    }
    func draw(in view: MTKView) {
        view.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        let queue = (view.device!.makeCommandQueue())!
        let command = (queue.makeCommandBuffer())!
        let pass = view.currentRenderPassDescriptor
        let encoder = (command.makeRenderCommandEncoder(descriptor:pass!))!
        // =======================================
        // Beginning of frame
        // Setup the view*projection matrix
        var uniformsFrame = Shader.UniformsFrame()
        // Build the uniforms for the frame
        let matrixAspect = simd_float4x4_scale(aspect, 1, 1);
        let matrixView = simd_float4x4_lookAt(eye:[25 * cos(frame), 10 * (1 - cos(frame * 0.2)), 10 * sin(frame)], center:[0,0,0], up:[0,1,0])
        let matrixProjection = simd_float4x4_perspective(fovyRadians:(60.0 / 360.0) * (.pi * 2), aspect:1, near:0.001, far:100.0);
        uniformsFrame.viewProjection = matrixAspect * matrixProjection * matrixView;
        // Build the view direction
        let cameraForward = SIMD3<Float>(0, 0, -1)
        let rotation = simd_float3x3(
            SIMD3<Float>(matrixView.columns.0.x, matrixView.columns.0.y, matrixView.columns.0.z),
            SIMD3<Float>(matrixView.columns.1.x, matrixView.columns.1.y, matrixView.columns.1.z),
            SIMD3<Float>(matrixView.columns.2.x, matrixView.columns.2.y, matrixView.columns.2.z)
        )
        uniformsFrame.view = simd_normalize(rotation.transpose * cameraForward)
        // Add the light position (point light)
        uniformsFrame.light = [25 * cos(frame * 0.73), 10 * (1 - cos(frame * 0.16)), 10 * sin(frame * 0.73)]
        // =======================================
        let uniformsSize = MemoryLayout<Shader.UniformsFrame>.size
        let uniformsBuffer = withUnsafeBytes(of: uniformsFrame) { ptr in
            return device.makeBuffer(bytes: ptr.baseAddress!, length: uniformsSize, options: [])! }
        // Start encoding the render command buffer
        encoder.setDepthStencilState(stateDepth)
        // Bind the per-frame constants
        encoder.setVertexBuffer(uniformsBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformsBuffer, offset: 0, index: 1)
        // Render instances
        for i in instances {
            i.render(encoder: encoder);
        }
        frame = frame + 0.01
        // End of frame
        // ========================================
        encoder.endEncoding()
        command.present(view.currentDrawable!)
        command.commit()
    }
}

class MTKViewDelegateTest: NSObject, MTKViewDelegate {
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
    }
    func draw(in view: MTKView) {
        view.clearColor = MTLClearColor(red: Double.random(in: 0..<1), green: Double.random(in: 0..<1), blue: Double.random(in: 0..<1), alpha: 1)
        let queue = view.device?.makeCommandQueue()
        let command = queue?.makeCommandBuffer()
        let pass = view.currentRenderPassDescriptor
        let encoder = command?.makeRenderCommandEncoder(descriptor:pass!)
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
