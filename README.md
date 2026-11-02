# SAKKI-MAN

中学受験の **社会** に特化した記憶アプリ ＆ ショート動画のアイデア置き場。

## アプリ（スマホで開く）

- [日本地図タップクイズ](https://sakki-man.vercel.app/japan-map-quiz/) … 出された県を地図でタップ（[仕様](apps/japan-map-quiz/HANDOFF.md)）

## ドキュメント

| ファイル | 中身 |
|---|---|
| [docs/character.md](docs/character.md) | キャラクター「サッ記マン」の設定 |
| [docs/app-ideas.md](docs/app-ideas.md) | 記憶アプリの機能案 |
| [docs/short-video-ideas.md](docs/short-video-ideas.md) | ショート動画のシリーズ案・台本の型 |
| [docs/open-questions.md](docs/open-questions.md) | まだ決めていないこと |

## 前提

- 対象：小4〜小6の中学受験生（と保護者）
- 範囲：地理・歴史・公民・時事
- 方針：動画で「おっ」と思わせて、アプリで「定着」させる

## 最近の変更

- 2026-11-02 Claude：地図クイズの4択で、問いを選択肢のすぐ上に移動（上のバーは進み具合だけ）
- 2026-11-02 Claude：地図クイズの左上にタイトルへ戻るボタン、音ボタンの左にデバッグ（自動で全問正解）ボタンを追加
- 2026-11-02 Claude：地図クイズに 4年生〜中学受験の4モード、地理コース（県名タップ→県庁所在地4択→政令指定都市）、県名マスター判定、県ごとに色がつくコレクションを追加
- 2026-11-02 12:04 JST Codex：正解直後の終了・再開始で前のクイズのタイマーが残る問題と、問題切替時の県名ヒント表示・判定を修正。

- 2026-11-02 Claude：Vercel と連携。https://sakki-man.vercel.app/ で公開（main に push で自動反映）
- 2026-11-02 Claude：日本地図タップクイズ（v4）を apps/ に追加。main に push すると GitHub Pages へ自動公開
- 2026-11-02 Claude：キャラクター「サッ記マン」の設定を追加。動画の台本の型をボソボソタイム入りに
- 2026-11-02 Claude：リポジトリ作成。アプリ案・ショート動画案・未決事項の初版
