import MetalKit

class MTKViewRenderWindow : MTKView {
    var stateDepth: MTLDepthStencilState?
    var instances: [Instance] = []
    var aspect: Float = 1
    var tick: Float = 0
    override init(frame frameRect: CGRect, device: (any MTLDevice)?) {
        super.init(frame: frameRect, device: device)
        _setup()
    }
    required init(coder: NSCoder) {
        super.init(coder: coder)
        _setup()
    }
    func _setup() {
        isPaused = false
        preferredFramesPerSecond = 60
        depthStencilPixelFormat = .depth32Float
        // Prepare the depth stencil state
        let desc = MTLDepthStencilDescriptor()
        desc.depthCompareFunction = .less
        desc.isDepthWriteEnabled = true
        self.stateDepth = device!.makeDepthStencilState(descriptor: desc)!
        // Create the scene
        let materialFlat = Material(device: device!, name: "flat")
        let materialNormal = Material(device: device!, name: "normal")
        let materialShiny = Material(device: device!, name: "shiny")
        let meshPlane = Mesh(device: device!, shape: plane, u: 1, v: 1)
        let meshSphere = Mesh(device: device!, shape: sphere, u: 50, v: 50)
        // Add in a coordinate reference
        var uniformsInstance = Shader.UniformsInstance()
        // Add in a plane
        uniformsInstance.diffuse = simd_float3(0, 1, 0)
        uniformsInstance.model = simd_float4x4_translate(0, -6, 0) * simd_float4x4_scale(100, 1, 100)
        instances.append(Instance(device: device!, material: materialFlat, mesh: meshPlane, uniforms: uniformsInstance))
        // Add in axis guides
        uniformsInstance.diffuse = simd_float3(1, 0, 0)
        uniformsInstance.model = simd_float4x4_translate(10, 0, 0)
        instances.append(Instance(device: device!, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        uniformsInstance.model = simd_float4x4_translate(0, 10, 0)
        instances.append(Instance(device: device!, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        uniformsInstance.model = simd_float4x4_translate(0, 0, 10)
        instances.append(Instance(device: device!, material: materialNormal, mesh: meshSphere, uniforms: uniformsInstance))
        // Add in a bunch of spheres
        for z in -5...5 {
            for y in -5...5 {
                for x in -5...5 {
                    uniformsInstance.diffuse = simd_float3((Float(x) + 5.0) / 10.0, (Float(y) + 5.0) / 10.0, (Float(z) + 5.0) / 10.0)
                    uniformsInstance.model = simd_float4x4_translate(Float(x), Float(y), Float(z))
                    let instance = Instance(device: device!, material: materialShiny, mesh: meshSphere, uniforms: uniformsInstance)
                    instances.append(instance);
                }
            }
        }
    }
    override func draw() {
        super.draw()
        aspect = Float(frame.height) / Float(frame.width)
        clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        let queue = (device!.makeCommandQueue())!
        let command = (queue.makeCommandBuffer())!
        let pass = currentRenderPassDescriptor
        let encoder = (command.makeRenderCommandEncoder(descriptor:pass!))!
        // =======================================
        // Beginning of frame
        // Setup the view*projection matrix
        var uniformsFrame = Shader.UniformsFrame()
        // Build the uniforms for the frame
        let matrixAspect = simd_float4x4_scale(aspect, 1, 1);
        let matrixView = simd_float4x4_lookAt(eye:[25 * cos(tick), 10 * (1 - cos(tick * 0.2)), 10 * sin(tick)], center:[0,0,0], up:[0,1,0])
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
        uniformsFrame.light = [25 * cos(tick * 0.73), 10 * (1 - cos(tick * 0.16)), 10 * sin(tick * 0.73)]
        // =======================================
        let uniformsSize = MemoryLayout<Shader.UniformsFrame>.size
        let uniformsBuffer = withUnsafeBytes(of: uniformsFrame) { ptr in
            return device!.makeBuffer(bytes: ptr.baseAddress!, length: uniformsSize, options: [])! }
        // Start encoding the render command buffer
        encoder.setDepthStencilState(stateDepth)
        // Bind the per-frame constants
        encoder.setVertexBuffer(uniformsBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformsBuffer, offset: 0, index: 1)
        // Render instances
        for i in instances {
            i.render(encoder: encoder);
        }
        tick = tick + 0.01
        // End of frame
        // ========================================
        encoder.endEncoding()
        command.present(currentDrawable!)
        command.commit()
    }
}
