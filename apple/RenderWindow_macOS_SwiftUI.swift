import MetalKit
import SwiftUI

struct NSViewReoresentableImpl: NSViewRepresentable {
    var mtkview : MTKView
    var renderer : MTKViewDelegate
    init() {
        mtkview = MTKView(frame: .zero, device: MTLCreateSystemDefaultDevice())
        renderer = MTKViewDelegateImpl(device: mtkview.device!)
        setupMTKView(view: mtkview, delegate: renderer)
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
