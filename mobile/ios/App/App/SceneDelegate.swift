import UIKit
import Capacitor

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = AppViewController()
        window?.makeKeyAndVisible()

        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}

/// Capacitor の画面に、アプリ用の小さな調整を足す
class AppViewController: CAPBridgeViewController {
    override func capacitorDidLoad() {
        super.capacitorDidLoad()
        guard let webView = webView else { return }
        // 中身はすべてアプリの中のファイルなので、ページ移動のたびの「危ないサイトの確認」はいらない（ここで待たされて画面が遅れることがある）
        webView.configuration.preferences.isFraudulentWebsiteWarningEnabled = false
        // iOS 26 のスクロール端のぼかし（上下に出る灰色の帯）を消す。地図の画面は不透明でマットに見せたい
        if #available(iOS 26.0, *) {
            webView.scrollView.topEdgeEffect.isHidden = true
            webView.scrollView.bottomEdgeEffect.isHidden = true
        }
    }
}
