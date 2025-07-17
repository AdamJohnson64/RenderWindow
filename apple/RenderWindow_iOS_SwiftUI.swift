import MetalKit
import UIKit

class UIViewControllerImpl: UIViewController {
    var mtkview : MTKView?
    var renderer : MTKViewDelegate?
    override func loadView() {
        if (mtkview == nil) {
            mtkview = MTKView(frame: .zero, device: MTLCreateSystemDefaultDevice());
        }
        if (renderer == nil) {
            renderer = MTKViewDelegateImpl(device: mtkview!.device!)
        }
        setupMTKView(view: mtkview!, delegate: renderer!)
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
