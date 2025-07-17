import MetalKit
import SwiftUI

struct NSViewRepresentableImpl: NSViewRepresentable {
    var mtkView: MTKView
    var renderer: MTKViewDelegate

    init() {
        mtkView = MTKView(frame: .zero, device: MTLCreateSystemDefaultDevice())
        renderer = MTKViewDelegateImpl(device: mtkView.device!)
        setupMTKView(view: mtkView, delegate: renderer)
    }

    func makeNSView(context: Context) -> NSView {
        return mtkView
    }

    func updateNSView(_ nsView: NSView, context: Context) {
        // No-op
    }
}

@main
struct AppImpl: App {
    var body: some Scene {
        Window("RenderWindow", id: "RenderWindow") {
            NSViewRepresentableImpl()
        }
    }
}
