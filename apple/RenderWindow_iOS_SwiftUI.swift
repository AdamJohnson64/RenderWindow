import MetalKit
import UIKit

class UIViewControllerImpl: UIViewController {
    var mtkView: MTKView?
    var renderer: MTKViewDelegate?

    override func loadView() {
        if mtkView == nil {
            mtkView = MTKView(frame: .zero, device: MTLCreateSystemDefaultDevice())
        }
        if renderer == nil {
            renderer = MTKViewDelegateImpl(device: mtkView!.device!)
        }
        setupMTKView(view: mtkView!, delegate: renderer!)
        view = mtkView
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
