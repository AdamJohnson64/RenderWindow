import MetalKit
import SwiftUI

class MTKViewDelegateImpl: NSObject, MTKViewDelegate {
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
    }
    func draw(in view: MTKView) {
        view.clearColor = MTLClearColor(red:Double.random(in:0..<1), green:Double.random(in:0..<1), blue:Double.random(in:0..<1), alpha:1.0)
        let queue = view.device?.makeCommandQueue()
        let command = queue?.makeCommandBuffer()
        let pass = view.currentRenderPassDescriptor
        let encoder = command?.makeRenderCommandEncoder(descriptor:pass!)
        encoder?.endEncoding()
        command?.present(view.currentDrawable!)
        command?.commit()
    }
}

struct NSViewReoresentableImpl: NSViewRepresentable {
    var mtkview = MTKView()
    var renderer = MTKViewDelegateImpl()
    init() {
        mtkview.delegate = renderer
        mtkview.device = MTLCreateSystemDefaultDevice()
        mtkview.isPaused = false
        mtkview.preferredFramesPerSecond = 1
    }
    func makeNSView(context: Context) -> NSView {
        return mtkview
    }
    func updateNSView(_ nsView: NSView, context: Context) {
    }
}

@main
struct AppImpl: App {
    var body: some Scene {
        Window("RenderWindow", id:"RenderWindow") {
            NSViewReoresentableImpl()
        }
    }
}
