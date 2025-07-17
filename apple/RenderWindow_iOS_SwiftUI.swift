import MetalKit
import UIKit

class UIViewControllerImpl: UIViewController {
    var mtkview = MTKView()
    var renderer = MTKViewDelegateImpl()
    override func loadView() {
        setupMTKView(view: mtkview, delegate: renderer)
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
