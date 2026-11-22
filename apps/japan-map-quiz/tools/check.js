// 日本地図タップドリルの確認テスト（2026-11-22）
//   node apps/japan-map-quiz/tools/check.js     （Playwright の Chromium が必要）
// 1. 全コース・全ステージの全問題を、正解・不正解の両方で答えてみて、ページのエラーが出ないか
// 2. 4択の問題：選択肢が4つ・重ならない・正解がふくまれる
// 3. 禁則：問題文・選択肢・正誤・解説で、行の終わりに「（『【、行の頭に、。」）』】！？が来ないか（幅 320px と 375px）
// 4. ランダムのステージで「まちがえた問題だけもう一回」が同じ問題を出すか
// どれか1つでもだめなら、終了コード 1 で止まる
const path = require("path");
const { chromium } = require("playwright");
const URL = "file://" + path.resolve(__dirname, "..", "index.html");

(async () => {
  const browser = await chromium.launch();
  const fails = [];
  for (const width of [375, 320]) {
    const page = await browser.newPage({ viewport: { width, height: 760 } });
    page.on("pageerror", e => fails.push(`[${width}px] ページのエラー: ${e.message}`));
    page.on("console", m => { if (m.type() === "error" && !/Fetch API cannot load file:|ERR_FILE_NOT_FOUND|bgm\//.test(m.text())) fails.push(`[${width}px] console: ${m.text()}`); });
    await page.goto(URL);
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const bad = [], open = "「（『【", close = "、。」）』】！？";
      const scan = label => document.querySelectorAll(".fb .txt, .ask, .choices").forEach(el => {
        const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), cs = []; let n;
        while ((n = w.nextNode())) { if (n.parentElement.closest("rt")) continue;
          for (let i = 0; i < n.data.length; i++) { const ch = n.data[i]; if (ch === "⁠") continue;
            const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + 1); const rc = rg.getClientRects()[0];
            if (rc && rc.width > 0) cs.push([ch, Math.round(rc.top)]); } }
        for (let i = 1; i < cs.length; i++) if (cs[i][1] > cs[i - 1][1] + 3 && (open.includes(cs[i - 1][0]) || close.includes(cs[i][0])))
          bad.push(`禁則 ${label}: ${cs.slice(Math.max(0, i - 6), i).map(c => c[0]).join("")}⏎${cs.slice(i, i + 6).map(c => c[0]).join("")}`);
      });
      let answered = 0;
      for (const c of COURSES) for (const st of stagesOf(c)) {
        startQuiz(c, st, st.codes, {stage: true});
        for (let i = 0; i < quiz.qs.length; i++) for (const ok of [true, false]) {
          quiz.i = i; nextQ(); const q = quiz.q;
          if (kindOf(q) === "choice") {
            const names = q.choices.map(x => x[0]);
            if (names.length < 2 || new Set(names).size !== names.length || !names.includes(q.correct)) bad.push(`選択肢 ${c.id}:${q.key}: ${names.join("/")}`);
            answerChoice(q.order.findIndex(o => ok ? o[0] === q.correct : o[0] !== q.correct));
          } else {
            const wrong = PREFS.find(x => !q.answers.includes(x.code) && quiz.inArea.has(x.code));
            handleTap(ok || !wrong ? q.answers[0] : wrong.code);
          }
          scan(`${c.id}:${q.key}:${ok ? "正解" : "不正解"}`); answered++;
        }
      }
      // ランダムのステージのやり直し
      for (const [cid, sid] of [["general", "g10"], ["silhouette", "r10"]]) {
        const c = courseOf(cid), st = stagesOf(c).find(s => s.id === sid);
        startQuiz(c, st, st.codes, {stage: true});
        const prev = quiz.qs, miss = prev.slice(0, 3).map(q => q.key);
        startQuiz(c, st, st.codes, {keys: miss, prev});
        if (quiz.qs.length !== 3 || !quiz.qs.every(q => miss.includes(q.key))) bad.push(`やり直し ${cid}:${sid}: ${quiz.qs.length}問`);
      }
      home();
      return {answered, bad: [...new Set(bad)]};
    });
    console.log(`[${width}px] ${r.answered} 回答・問題 ${r.bad.length} 件`);
    r.bad.forEach(b => fails.push(`[${width}px] ${b}`));
    await page.close();
  }
  await browser.close();
  if (fails.length) { console.log(fails.slice(0, 80).join("\n")); process.exit(1); }
  console.log("OK");
})();
