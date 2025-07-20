import MetalKit

class MTKViewColorTest: MTKView {
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
    }
    func draw(in view: MTKView) {
        clearColor = MTLClearColor(red: Double.random(in: 0..<1), green: Double.random(in: 0..<1), blue: Double.random(in: 0..<1), alpha: 1)
        let queue = device?.makeCommandQueue()
        let command = queue?.makeCommandBuffer()
        let pass = currentRenderPassDescriptor
        let encoder = command?.makeRenderCommandEncoder(descriptor:pass!)
        encoder?.endEncoding()
        command?.present(view.currentDrawable!)
        command?.commit()
    }
}
