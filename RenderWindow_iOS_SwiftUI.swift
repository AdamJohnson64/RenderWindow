import MetalKit
import UIKit

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

class UIViewControllerImpl: UIViewController {
    var mtkview = MTKView()
    var renderer = MTKViewDelegateImpl()
    override func loadView() {
        mtkview.delegate = renderer
        mtkview.device = MTLCreateSystemDefaultDevice()
        mtkview.isPaused = false
        mtkview.preferredFramesPerSecond = 1
        view = mtkview
    }
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}

@main
class SceneDelegate: UIResponder, UIWindowSceneDelegate, UIApplicationDelegate {
    var window: UIWindow?
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = UIViewControllerImpl()
        window?.makeKeyAndVisible()
    }
}
