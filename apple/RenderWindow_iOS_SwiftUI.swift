import MetalKit
import UIKit

class UIViewControllerImpl: UIViewController {
    var mtkView: MTKViewRenderWindow?

    override func loadView() {
        if (mtkView == nil) {
            mtkView = MTKViewRenderWindow(frame: .zero, device: MTLCreateSystemDefaultDevice())
            view = mtkView
        }
    }
}

@main
class UIApplicationImpl: UIApplication, UIApplicationDelegate {
    var window: UIWindow?
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        window = UIWindow()
        window?.rootViewController = UIViewControllerImpl()
        window?.makeKeyAndVisible()
        return true
    }
}
