# SAKKI-MAN 作業メモ（Claude 向け）

中学受験・社会の暗記ヒーロー「サッ記マン」のアプリと動画案。キャラ設定は [docs/character.md](docs/character.md)。

## 公開URL（スマホで確認する場所）

メインは Vercel（ユーザーがスマホで見るのはこちら）:

- 入口: https://sakki-man.vercel.app/
- 日本地図タップクイズ: https://sakki-man.vercel.app/japan-map-quiz/

予備に GitHub Pages（https://hnhn-g1t.github.io/SAKKI-MAN/）。

main に push すると、Vercel（`vercel.json`）と GitHub Actions（`.github/workflows/pages.yml`）の両方が `tools/build_site.py` でビルドして公開する（1〜2分）。

## 作業ルール

- 質問されたら、まず質問に答える。制作・変更は、必要なら進めてよいか確認してから着手する。
- 確率・集計など数値が絡むものは、必ずコードを実行して結果を出す（暗算・推定で答えない）。
- 変更したら README.md「最近の変更」の先頭に `日付 Claude：内容` を1行足す。
- 検証が通ったら main に push まで済ませる（スマホで見られないと終わっていない）。

## 日本地図タップクイズ（apps/japan-map-quiz）

詳しい仕様・座標系・はまりどころは [apps/japan-map-quiz/HANDOFF.md](apps/japan-map-quiz/HANDOFF.md)。

- `index.html` はビルドの出力。直接編集しない。`src/template.html` を直す
- ビルド（Windows は `py -3`、それ以外は `python3`）:

  ```
  py -3 apps/japan-map-quiz/tools/build.py
  ```

- ビルドした `index.html` も必ずコミットする。忘れると Actions の「ビルド忘れチェック」で公開が止まる
- 検証: ビルド → ブラウザで index.html を開き、HANDOFF.md「動作確認」の観点（県48要素・375px幅・沖縄の切り替え・目ボタン・コンソールエラーなし）を見る

## アプリを増やすとき

`apps/<名前>/` に置き、`tools/build_site.py` の `APPS` と `site/index.html` のリンクに1行ずつ足す。
