import MetalKit
import SwiftUI

struct NSViewRepresentableImpl: NSViewRepresentable {
    var mtkView: MTKViewRenderWindow
    
    init() {
        mtkView = MTKViewRenderWindow(frame: .zero, device: MTLCreateSystemDefaultDevice())
    }
    func makeNSView(context: Context) -> NSView {
        return mtkView
    }
    func updateNSView(_ nsView: NSView, context: Context) {
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
