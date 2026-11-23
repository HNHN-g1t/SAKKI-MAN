# サッ記マン iOS アプリ（Capacitor）

Web 版（タイトル画面＋日本地図タップドリル）を、そのままアプリの中に入れて iOS アプリにしたもの。
画像・音・フォントもアプリの中に入るので、電波がなくても動く。

- アプリ名：サッ記マン　／　バンドルID：`com.hnhn.Sakkiman`（変えるときは下の「1回目だけ」）
- iPhone 専用・縦向きだけ・iOS 16 以上（iPhone SE 第1世代など iOS 15 までの機種は対象外）
- 中身は `mobile/www/`（`build_www.py` が作る。リポジトリには入れない）→ `npx cap sync ios` で `ios/App/App/public/` にうつる

## Mac で動かす

いるもの：Xcode（App Store から）、Node.js（https://nodejs.org の LTS）、python3（Xcode を入れると使える）

```
git pull
cd mobile
npm install          # 1回目と、Capacitor を上げたときだけ
npm run sync         # Web をビルドして iOS プロジェクトへうつす（中身を変えたら毎回）
npm run open         # Xcode が開く
```

### 1回目だけ（Xcode）

1. 左の一覧で「App」→ TARGETS の「App」→「Signing & Capabilities」
2. 「Team」に自分の開発者アカウント（Apple Developer Program のチーム）を選ぶ
3. バンドルID を自分のもの（例：`jp.自分のドメイン.sakkiman`）に変えるなら、ここの「Bundle Identifier」と `mobile/capacitor.config.json` の `appId` の両方を同じに変える

### 自分の iPhone で動かす

1. iPhone を Mac にケーブルでつなぐ（初めてなら iPhone の「設定 > プライバシーとセキュリティ > デベロッパモード」をオン）
2. Xcode 上の実行先で自分の iPhone を選んで ▶（Run）

### App Store に出す

1. 実行先を「Any iOS Device (arm64)」にして、メニュー「Product > Archive」
2. できた Archive を「Distribute App > App Store Connect > Upload」
3. App Store Connect（https://appstoreconnect.apple.com）でアプリを作り、スクリーンショット・説明文・プライバシーポリシーの URL・年齢区分などを入れて審査に出す
4. 2回目からは、Xcode の「General」の Version（例 1.0.1）か Build の数字を上げてから Archive

## 中身を更新するとき

Web 版（`apps/japan-map-quiz/src/template.html` など）を直して push したら、Mac で `git pull` → `cd mobile` → `npm run sync` → Xcode でビルド。

## フォント

`mobile/fonts/` は Google Fonts の BIZ UDPGothic と Dela Gothic One（どちらも SIL Open Font License 1.1）。
取り直すときは `python3 mobile/fetch_fonts.py`。アプリでは Google Fonts を読みに行かず、これを使う（`build_www.py` が差しかえる）。
