import MetalKit
import SwiftUI

struct NSViewReoresentableImpl: NSViewRepresentable {
    var mtkview = MTKView()
    var renderer = MTKViewDelegateImpl()
    init() {
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
