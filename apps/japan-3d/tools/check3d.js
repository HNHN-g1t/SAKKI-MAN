// 3D日本地図の確認テスト: node apps/japan-3d/tools/check3d.js [URL] [スクショの置き場]
//   読みこみ・コンソールエラーなし・地形の高さ（富士山＞六甲山）・強調スライダー・タップ移動・絶景ビューの出入り
//   URL を省くと http://localhost:8765/apps/japan-3d/（リポジトリの直下で python3 -m http.server 8765）
const { chromium } = require("playwright");
const URL_ = process.argv[2] || "http://localhost:8765/apps/japan-3d/";
const OUT = process.argv[3] || "";
(async () => {
  // ヘッドレスでも WebGL が動くよう、ソフトウェア描画（SwiftShader）を使う
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const page = await browser.newPage({ viewport: { width: 375, height: 740 }, deviceScaleFactor: 1, hasTouch: true });
  const errors = [];
  // SwiftShader がスクショのたびに出す「GPU stall due to ReadPixels」は除く
  page.on("console", (m) => { if ((m.type() === "error" || m.type() === "warning") && !m.text().includes("GL Driver Message")) errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  const ok = (c, msg) => { console.log((c ? "OK  " : "NG  ") + msg); if (!c) process.exitCode = 1; };
  const shot = async (n) => { if (OUT) await page.screenshot({ path: `${OUT}/${n}.png` }); };
  const wait = (ms) => page.waitForTimeout(ms);
  await page.goto(URL_);
  await page.waitForFunction(() => window.__j3d && window.__j3d.ready, null, { timeout: 90000 });
  await wait(1500);
  await shot("01-japan");
  const h = await page.evaluate(() => {
    const j = window.__j3d, f = j.SPOTS.find((s) => s.id === "fuji"), r = j.SPOTS.find((s) => s.id === "rokko");
    return { fuji: j.groundY(f.x, f.z), rokko: j.groundY(r.x, r.z), sea: j.groundY(600, 900) };
  });
  ok(h.fuji > h.rokko * 3 && h.rokko > 0 && h.sea === 0, `高さ 富士山 ${h.fuji.toFixed(2)} > 六甲山 ${h.rokko.toFixed(2)}、海 ${h.sea}`);
  await page.evaluate(() => window.__j3d.setExag(8));
  const h8 = await page.evaluate(() => { const j = window.__j3d, f = j.SPOTS.find((s) => s.id === "fuji"); return j.groundY(f.x, f.z); });
  ok(Math.abs(h8 / h.fuji - 2) < 0.01, `強調 ×8 で高さ2倍（${(h8 / h.fuji).toFixed(3)}）`);
  await page.evaluate(() => window.__j3d.setExag(4));

  // 中部にズームして斜めから
  await page.evaluate(() => { const f = window.__j3d.SPOTS.find((s) => s.id === "fuji"); window.__j3d.setCam({ tx: f.x - 30, tz: f.z - 10, D: 160, pitch: 0.6, yaw: 0.3 }); });
  await wait(1200);
  await shot("02-chubu");
  // ドラッグ → 指をはなしたあとも慣性ですべる
  await page.mouse.move(200, 400); await page.mouse.down();
  for (let k = 1; k <= 6; k++) { await page.mouse.move(200 + k * 25, 400); await wait(16); }
  await page.mouse.up();
  const c1 = await page.evaluate(() => window.__j3d.cam.tx);
  await wait(250);
  const c2 = await page.evaluate(() => window.__j3d.cam.tx);
  ok(c2 < c1 - 0.2, `ドラッグのあと慣性ですべる（${c1.toFixed(1)} → ${c2.toFixed(1)}）`);
  // 2本指で上へドラッグ → 傾きが変わる（CDP でタッチを送る）
  const cdp = await page.context().newCDPSession(page);
  const touch = (type, pts) => cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts.map(([x, y], id) => ({ x, y, id })) });
  const p0 = await page.evaluate(() => window.__j3d.cam.pitch);
  await touch("touchStart", [[150, 450], [230, 450]]);
  for (let k = 1; k <= 6; k++) { await touch("touchMove", [[150, 450 - k * 15], [230, 450 - k * 15]]); await wait(16); }
  await touch("touchEnd", []);
  const p1 = await page.evaluate(() => window.__j3d.cam.pitch);
  ok(Math.abs(p1 - p0) > 0.2, `2本指ドラッグで傾く（${p0.toFixed(2)} → ${p1.toFixed(2)}）`);
  await page.evaluate(() => { const f = window.__j3d.SPOTS.find((s) => s.id === "fuji"); window.__j3d.setCam({ tx: f.x - 30, tz: f.z - 10, D: 160, pitch: 0.6, yaw: 0.3 }); });
  await wait(800);
  // 画面の真ん中をタップ → 地形の上を移動
  const before = await page.evaluate(() => ({ x: window.__j3d.player.x, z: window.__j3d.player.z }));
  await page.touchscreen.tap(187, 420);
  await wait(300);
  ok(await page.evaluate(() => !!window.__j3d.player.moving), "タップで移動を始める");
  await page.waitForFunction(() => !window.__j3d.player.moving, null, { timeout: 15000 });
  const after = await page.evaluate(() => ({ x: window.__j3d.player.x, z: window.__j3d.player.z }));
  ok(Math.hypot(after.x - before.x, after.z - before.z) > 1, "タップした地点に着く");
  await shot("03-moved");

  // 富士山へ移動 → カード → 絶景ビュー
  await page.evaluate(() => window.__j3d.goTo("fuji"));
  await page.waitForFunction(() => !window.__j3d.player.moving, null, { timeout: 15000 });
  await wait(600);
  const card = await page.evaluate(() => document.getElementById("card").classList.contains("show") && document.getElementById("cardName").textContent);
  ok(card && card.includes("富士山"), `富士山に到着してカード（${card}）`);
  await shot("04-fuji-card");
  await page.click("#btnPano");
  await page.waitForFunction(() => window.__j3d.mode === "pano", null, { timeout: 15000 });
  ok(true, "絶景ビューに入る");
  await page.evaluate(() => { window.__j3d.pano.yaw = 2.6; window.__j3d.pano.auto = false; });   // 南西（駿河湾）の方
  await wait(1000);
  await shot("05-pano-fuji");
  const labels = await page.evaluate(() => [...document.querySelectorAll(".lb.guide")].filter((e) => e.style.display === "block").map((e) => e.textContent));
  if (errors.length) console.log(errors.join("\n"));
  ok(labels.length > 0, `うっすらラベル: ${labels.join(" / ")}`);
  await page.click("#btnPanoBack");
  await page.waitForFunction(() => window.__j3d.mode === "bird", null, { timeout: 15000 });
  ok(true, "鳥瞰にもどる");

  // 槍ヶ岳から南東（富士山の方）
  await page.evaluate(() => window.__j3d.warp("yari"));
  await wait(500);
  await page.evaluate(() => window.__j3d.enterPano());
  await page.waitForFunction(() => window.__j3d.mode === "pano", null, { timeout: 15000 });
  await page.evaluate(() => { window.__j3d.pano.yaw = -2.2; window.__j3d.pano.auto = false; });
  await wait(1000);
  await shot("06-pano-yari");
  const yl = await page.evaluate(() => [...document.querySelectorAll(".lb.guide")].filter((e) => e.style.display === "block").map((e) => e.textContent));
  ok(yl.some((t) => t.startsWith("富士山")), `槍ヶ岳から富士山のラベル: ${yl.join(" / ")}`);
  await page.click("#btnPanoBack");
  await page.waitForFunction(() => window.__j3d.mode === "bird", null, { timeout: 15000 });
  // 六甲山から南（大阪湾）
  await page.evaluate(() => window.__j3d.warp("rokko"));
  await page.evaluate(() => window.__j3d.enterPano());
  await page.waitForFunction(() => window.__j3d.mode === "pano", null, { timeout: 15000 });
  await page.evaluate(() => { window.__j3d.pano.yaw = 3.0; window.__j3d.pano.auto = false; });
  await wait(1000);
  await shot("07-pano-rokko");
  ok(errors.length === 0, "コンソールのエラー・警告なし" + (errors.length ? "\n  " + errors.join("\n  ") : ""));
  await browser.close();
})();
