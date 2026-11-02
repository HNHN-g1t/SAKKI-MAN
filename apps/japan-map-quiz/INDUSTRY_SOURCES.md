# 農林水産業・工業コース 問題データの出典一覧

`src/template.html` の `INDUSTRY` から作った一覧（最終確認日 2026-11-02）。データを直したら作り直す。

- 確認済み：答え・統計年・出典を国や県などの公式資料で確認した（出題する）
- 要確認：答えは確認済みだが、最新の年次などに確認が残る（出題する）
- 出題停止：根拠が足りないので出さない

確認は、公式資料の内容を検索で見る方法で行った（作業環境から官公庁のサイトを直接開けなかったため）。毎年の更新のときは、各URLの原本で数値を確かめ直すこと。


## 農業（米・野菜・花）

| ID | 問題 | 答え | 指標 | 統計年 | 出典 | 状態 |
|---|---|---|---|---|---|---|
| rice | 米の収穫量が全国一の都道府県は？ | 新潟県 | 水稲の収穫量（主食用） | 令和7年産 | [農林水産省「作物統計調査 令和7年産水陸稲の収穫量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kome/pdf/syukaku_suiriku_25.pdf) | 確認済み |
| potato | じゃがいもの収穫量が全国一の都道府県は？ | 北海道 | 春植えばれいしょの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産春植えばれいしょの作付面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_yasai/pdf/syukaku_barei_25.pdf) | 確認済み |
| onion | たまねぎの収穫量が全国一の都道府県は？ | 北海道 | たまねぎの収穫量 | 令和5年産（令和6・7年産の都道府県別は未確認） | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-01.pdf) | 要確認 |
| lettuce | レタスの収穫量が全国一の都道府県は？ | 長野県 | レタスの収穫量 | 令和5年産 | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-20.pdf) | 確認済み |
| pepper | ピーマンの収穫量が全国一の都道府県は？ | 茨城県 | ピーマンの収穫量 | 令和5年産 | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-08.pdf) | 確認済み |
| strawberry | いちごの収穫量が全国一の都道府県は？ | 栃木県 | いちごの収穫量 | 令和5年産 | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-09.pdf) | 確認済み |
| peanut | 落花生の収穫量が全国一の都道府県は？ | 千葉県 | らっかせいの収穫量 | 未確認（令和7年版の概要に掲載の年次） | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-12.pdf) | 要確認 |
| konjac | こんにゃくいもの収穫量が全国一の都道府県は？ | 群馬県 | こんにゃくいもの収穫量 | 令和6年産 | [農林水産省「こんにゃくをめぐる事情」（令和7年7月）](https://www.maff.go.jp/j/seisan/tokusan/attach/pdf/konnyaku-17.pdf) | 確認済み |
| sugarcane | さとうきびの収穫量が全国一の都道府県は？ | 沖縄県 | さとうきびの収穫量 | 令和5年産 | [農林水産省「都道府県の農林水産業の概要（令和7年版）」](https://www.maff.go.jp/j/kanbo/tiho/15sonota/todouhuken_gaiyou2025-47.pdf) | 確認済み |
| chrysanthemum | 菊（切り花）の出荷量が全国一の都道府県は？（令和6年産） | 愛知県 | きく（切り花）の出荷量 | 令和6年産 | [農林水産省「令和6年産花きの作付（収穫）面積及び出荷量」](https://www.maff.go.jp/j/tokei/kekka_gaiyou/sakumotu/sakkyou_kaki/sakutuke/r6/index.html) | 確認済み |

## くだもの

| ID | 問題 | 答え | 指標 | 統計年 | 出典 | 状態 |
|---|---|---|---|---|---|---|
| apple | りんごの収穫量が全国一の都道府県は？ | 青森県 | りんごの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産りんごの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_ringo_25.pdf) | 確認済み |
| mikan | みかんの収穫量が全国一の都道府県は？ | 和歌山県 | みかんの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産みかんの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_mikan_25.pdf) | 確認済み |
| grape | ぶどうの収穫量が全国一の都道府県は？ | 山梨県 | ぶどうの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産日本なし、ぶどうの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_ninasi_25.pdf) | 確認済み |
| peach | ももの収穫量が全国一の都道府県は？ | 山梨県 | ももの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産もも、すももの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_momo_25.pdf) | 確認済み |
| cherry | さくらんぼの収穫量が全国一の都道府県は？ | 山形県 | おうとう（さくらんぼ）の収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産びわ、おうとう、うめの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_biwa_25.pdf) | 確認済み |
| pear | 西洋なしの収穫量が全国一の都道府県は？ | 山形県 | 西洋なしの収穫量 | 令和6年産 | [農林水産省「作物統計調査 令和6年産西洋なし、かき、くりの結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_senasi_24.pdf) | 確認済み |
| ume | うめの収穫量が全国一の都道府県は？ | 和歌山県 | うめの収穫量 | 令和7年産 | [農林水産省「作物統計調査 令和7年産びわ、おうとう、うめの栽培面積、結果樹面積、収穫量及び出荷量」](https://www.maff.go.jp/j/tokei/kouhyou/sakumotu/sakkyou_kazyu/pdf/syukaku_biwa_25.pdf) | 確認済み |
| melon | メロンの収穫量が全国一の都道府県は？ | 茨城県 | メロンの収穫量 | 令和5年産 | [関東農政局茨城県拠点「茨城県のメロン生産」（令和7年10月）](https://www.maff.go.jp/kanto/chiikinet/ibaraki/ibarakitokei_bunnseki/attach/pdf/ibarakibunseki-3.pdf) | 確認済み |
| pineapple | パイナップルの収穫量が全国一の都道府県は？ | 沖縄県 | パインアップルの収穫量 | 令和5年産 | [農林水産省「令和5年産パインアップルの収穫面積、収穫量及び出荷量（沖縄県）」](https://www.maff.go.jp/j/tokei/kekka_gaiyou/sakumotu/sakkyou_kajyu/paineapp/r5/index.html) | 確認済み |

## 畜産・林業・水産業

| ID | 問題 | 答え | 指標 | 統計年 | 出典 | 状態 |
|---|---|---|---|---|---|---|
| dairy | 乳牛（乳用牛）の飼育頭数が全国一の都道府県は？ | 北海道 | 乳用牛の飼養頭数 | 令和7年2月1日現在 | [農林水産省「畜産統計」（鹿児島県「鹿児島県畜産の概要」の全国表で確認）](http://www.pref.kagoshima.jp/ag07/sangyo-rodo/nogyo/tikusan/basic/gaiyou.html) | 確認済み |
| pig | 豚の飼育頭数が全国一の都道府県は？ | 鹿児島県 | 豚の飼養頭数 | 令和7年2月1日現在 | [鹿児島県「豚に関する情報」（農林水産省「畜産統計」より）](https://www.pref.kagoshima.jp/ag07/sangyo-rodo/nogyo/tikusan/tokei/buta.html) | 確認済み |
| kiso | 木曽ひのき（天然の三大美林）がある都道府県は？ | 長野県 | 日本三大美林（天然林） | ― | [林野庁東北森林管理局「日本三大美林について」](https://www.rinya.maff.go.jp/tohoku/keikaku/sandaibirin.html) | 確認済み |
| akita | 秋田すぎ（天然の三大美林）がある都道府県は？ | 秋田県 | 日本三大美林（天然林） | ― | [林野庁東北森林管理局「日本三大美林について」](https://www.rinya.maff.go.jp/tohoku/keikaku/sandaibirin.html) | 確認済み |
| yoshino | 吉野すぎ（人工の三大美林）がある都道府県は？ | 奈良県 | 日本三大人工美林 | ― | [奈良県川上村「川上村のプロフィール」](https://www.vill.kawakami.nara.jp/life/docs/2017013100120/) | 確認済み |
| choshi | 水あげ量が全国トップクラスの漁港、銚子港がある都道府県は？ | 千葉県 | 主要漁港の水あげ量 | 2025年（令和7年） | [八戸市「水産統計」（全国主要漁港の水揚げ状況）](https://www.city.hachinohe.aomori.jp/soshikikarasagasu/suisanjimusho/1_1/3836.html) | 確認済み |
| yaizu | 冷凍のまぐろ・かつおの水あげが多い焼津港がある都道府県は？ | 静岡県 | 冷凍まぐろ類・かつおの上場水揚量（静岡県内の漁港の合計） | 令和6年 | [静岡県「みなみまぐろ(冷凍)…かつお(冷凍)の上場水揚量 日本一」（水産庁「水産物流通調査」より）](https://www.pref.shizuoka.jp/kensei/information/myshizuoka/1002255/1040934/1011248.html) | 確認済み |
| hachinohe | 八戸港（いか・さばの水あげが多い）がある都道府県は？ | 青森県 | 八戸港の魚種別水あげ量 | 2024年・2025年 | [八戸市「水産統計」](https://www.city.hachinohe.aomori.jp/soshikikarasagasu/suisanjimusho/1_1/3836.html) | 確認済み |
| sakaiminato | 日本海側の大きな漁港、境港がある都道府県は？ | 鳥取県 | ベニズワイガニの水あげ量 | ― | [鳥取県「蟹取県」紹介ページ](https://www.pref.tottori.lg.jp/178225.htm) | 確認済み |
| oyster | かきの養殖が全国一の都道府県は？ | 広島県 | かき類の養殖収獲量 | 2023年（令和5年） | [水産庁「カキ養殖をめぐる情勢について」（令和7年11月）](https://www.jfa.maff.go.jp/j/saibai/attach/pdf/kaki_youshoku-3.pdf) | 確認済み |
| nori | のりの養殖が全国一の都道府県は？ | 佐賀県 | のり類の養殖収獲量 | 未確認 | [水産庁「ノリ養殖をめぐる情勢について」（令和7年6月）](https://www.jfa.maff.go.jp/j/saibai/attach/pdf/norimeguji-6.pdf) | 出題停止 |

## 工業地帯・地場産業

| ID | 問題 | 答え | 指標 | 統計年 | 出典 | 状態 |
|---|---|---|---|---|---|---|
| output | 製造品出荷額が全国一の都道府県は？ | 愛知県 | 製造品出荷額等 | 2022年（2023年経済構造実態調査） | [愛知県「あいちの産業」（経済構造実態調査 製造業事業所調査より）](https://www.pref.aichi.jp/soshiki/ricchitsusho/miryoku-kouzou.html) | 確認済み |
| keiyo | 京葉工業地域の中心の都道府県は？ | 千葉県 | 工業地域の位置 | ― | [千葉県「京葉臨海コンビナート カーボンニュートラル推進協議会」資料](https://www.pref.chiba.lg.jp/sanshin/keiyo-rinkai/kyogikai/documents/04jimukyokusetumei.pdf) | 確認済み |
| tokai | 東海工業地域の中心の都道府県は？ | 静岡県 | 工業地域の位置 | ― | [静岡県「西部地域の産業」・富士市「産業史」](https://www.pref.shizuoka.jp/kensei/chiikikyoku/seibuchiiki/1058188/1035261.html) | 確認済み |
| kitakyu | 北九州工業地帯（地域）の中心の都道府県は？ | 福岡県 | 工業地帯の位置 | ― | [北九州市「八幡のあゆみ」](https://www.city.kitakyushu.lg.jp/yahatahigashi/file_0008.html) | 確認済み |
| kashima | 鹿島臨海工業地域がある都道府県は？ | 茨城県 | 工業地域の位置 | ― | [茨城県「鹿島港の概要」](https://www.pref.ibaraki.jp/doboku/kako/gaiyo.html) | 確認済み |
| mizushima | 水島（倉敷市）の石油化学コンビナートがある都道府県は？ | 岡山県 | 工業地帯の位置 | ― | [岡山県「水島臨海工業地帯の現状」（令和7年3月）](https://www.pref.okayama.jp/uploaded/life/906116_9310850_misc.pdf) | 確認済み |
| sabae | めがねフレームの産地、鯖江市がある都道府県は？ | 福井県 | めがねフレームの産地 | ― | [鯖江市「ものづくり」](https://www.city.sabae.fukui.jp/kanko/about/mono.html) | 確認済み |
| imabari | タオルの産地、今治市がある都道府県は？ | 愛媛県 | タオルの産地 | 2020年ごろ | [政府広報オンライン「Highlighting Japan」2020年9月号](https://www.gov-online.go.jp/eng/publicity/book/hlj/html/202009/202009_06_jp.html) | 確認済み |
| tsubame | 金属洋食器の産地、燕市がある都道府県は？ | 新潟県 | 金属洋食器の産地 | ― | [燕市「金属洋食器」地域未来投資促進法 基本計画](https://www.cas.go.jp/jp/seisaku/chiikimirai2/sangyo-keikaku/pdf/c-keikaku/niigataken-tsubameshi_kinzokuyoshokki_2-1.pdf) | 確認済み |

## 伝統工芸品

| ID | 問題 | 答え | 指標 | 統計年 | 出典 | 状態 |
|---|---|---|---|---|---|---|
| nanbu | 南部鉄器がつくられている都道府県は？ | 岩手県 | 伝統的工芸品の指定 | ― | [経済産業省「伝統的工芸品指定品目一覧［都道府県別］」（令和7年10月27日現在）](https://www.meti.go.jp/press/2025/10/20251027001/20251027001-b.pdf) | 確認済み |
| tendo | 天童将棋駒がつくられている都道府県は？ | 山形県 | 伝統的工芸品の指定 | ― | [経済産業省「伝統的工芸品指定品目一覧［都道府県別］」（令和7年10月27日現在）](https://www.meti.go.jp/press/2025/10/20251027001/20251027001-b.pdf) | 確認済み |
| aizu | 会津塗がつくられている都道府県は？ | 福島県 | 伝統的工芸品の指定 | ― | [経済産業省「伝統的工芸品指定品目一覧［都道府県別］」（令和7年10月27日現在）](https://www.meti.go.jp/press/2025/10/20251027001/20251027001-b.pdf) | 確認済み |
| mashiko | 益子焼がつくられている都道府県は？ | 栃木県 | 伝統的工芸品の指定 | ― | [栃木県「国指定の伝統的工芸品」](https://www.pref.tochigi.lg.jp/f02/work/shoukougyou/dentoukougei/national.html) | 確認済み |
| wajima | 輪島塗がつくられている都道府県は？ | 石川県 | 伝統的工芸品の指定 | ― | [石川県「こども向け県庁ガイド 伝統的工芸品」](https://www.pref.ishikawa.lg.jp/kensei/koho/kids/kodomo/dentou/main.html) | 確認済み |
| shigaraki | 信楽焼がつくられている都道府県は？ | 滋賀県 | 伝統的工芸品の指定 | ― | [滋賀県「滋賀県の伝統的工芸品について」](https://www.pref.shiga.lg.jp/ippan/shigotosangyou/kigyou/20017.html) | 確認済み |
| nishijin | 西陣織がつくられている都道府県は？ | 京都府 | 伝統的工芸品の指定 | ― | [経済産業省「伝統的工芸品指定品目一覧［都道府県別］」（令和7年10月27日現在）](https://www.meti.go.jp/press/2025/10/20251027001/20251027001-b.pdf) | 確認済み |
| bizen | 備前焼がつくられている都道府県は？ | 岡山県 | 伝統的工芸品の指定 | ― | [経済産業省「伝統的工芸品指定品目一覧［都道府県別］」（令和7年10月27日現在）](https://www.meti.go.jp/press/2025/10/20251027001/20251027001-b.pdf) | 確認済み |
| arita | 伊万里・有田焼がつくられている都道府県は？ | 佐賀県 | 伝統的工芸品の指定 | ― | [九州経済産業局「九州の伝統的工芸品」](https://www.kyushu.meti.go.jp/seisaku/dento/210330pamphlet.pdf) | 確認済み |
| hakata | 博多人形がつくられている都道府県は？ | 福岡県 | 伝統的工芸品の指定 | ― | [九州経済産業局「九州の伝統的工芸品」](https://www.kyushu.meti.go.jp/seisaku/dento/210330pamphlet.pdf) | 確認済み |
