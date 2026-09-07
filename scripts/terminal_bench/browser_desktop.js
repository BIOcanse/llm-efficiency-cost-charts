async (page) => {
  const checks = [];
  const check = (condition, message) => { if (!condition) throw new Error(message); checks.push(message); };
  const layouts = [];
  await page.setViewportSize({width: 1440, height: 1000});
  for (const language of ["zh-CN", "en"]) {
    await page.locator(`[data-language="${language}"]`).click();
    for (const version of ["4.0", "3.0", "2.1"]) {
      await page.locator("#tb-version").selectOption(version);
      await page.waitForFunction(v => document.querySelector('[data-i18n="snapshotLabel"]').textContent === `Terminal-Bench ${v}` && !document.querySelector("#tb-snapshot").disabled, version);
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      const values = await page.locator("#terminal-panel .interactive-chart-svg").evaluateAll(nodes => nodes.map(node => ({...node.dataset})));
      check(values.length === 3 && values.every(item => Number(item.labelCollisions) === 0), `1440px ${language} TB${version} labels`);
      check((await page.locator("#tb-image-token").getAttribute("href")).includes(`/${version}/2026-09-05/${language}/`), `Selected ${language} TB${version} image URL`);
      layouts.push({language, version, values});
    }
  }
  await page.locator("#tb-version").selectOption("4.0");
  await page.waitForFunction(() => document.querySelector('[data-i18n="snapshotLabel"]').textContent === "Terminal-Bench 4.0");
  const table = await page.locator("#tb-rankings .tb-table").evaluate(element => {
    const luminance = rgb => rgb.map(value => value / 255).map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4).reduce((sum, value, i) => sum + value * [.2126, .7152, .0722][i], 0);
    const colors = [...element.querySelectorAll("tbody td")].map(node => getComputedStyle(node).color);
    const minimumContrast = Math.min(...colors.map(color => 1.05 / (luminance(color.match(/[\d.]+/g).slice(0, 3).map(Number)) + .05)));
    const model = element.querySelector(".tb-model strong").getBoundingClientRect();
    const effort = element.querySelector(".tb-effort").getBoundingClientRect();
    return {minimumContrast, modelEffortGap: effort.left - model.right, bodyWidth: document.body.scrollWidth, viewport: innerWidth};
  });
  check(table.minimumContrast >= 4.5, "Cost-table text contrast");
  check(table.modelEffortGap >= 0 && table.modelEffortGap <= 10, "Reasoning level stays next to model name");
  check(table.bodyWidth === table.viewport, "Desktop page has no horizontal overflow");
  await page.evaluate(() => scrollTo(0, document.querySelector("#tb-rankings").getBoundingClientRect().top + scrollY - 65));
  await page.screenshot({path: ".playwright-cli/tb-1440-ranking-en.png"});
  await page.locator('[data-language="zh-CN"]').click();
  await page.evaluate(() => scrollTo(0, document.querySelector("#tb-rankings").getBoundingClientRect().top + scrollY - 65));
  await page.screenshot({path: ".playwright-cli/tb-1440-ranking-zh.png"});
  await page.locator("#tb-version").selectOption("1.0");
  await page.waitForFunction(() => document.querySelector('[data-i18n="snapshotLabel"]').textContent === "Terminal-Bench 1.0");
  check(await page.locator(".tb-unverified").count() > 0, "Legacy verification flags remain visible");
  check((await page.locator("#tb-sources a").first().getAttribute("href")).includes("/blob/130be845"), "TB1 official-source link is pinned, not a fallback leaderboard");
  await page.locator("#tb-version").selectOption("2.1");
  await page.waitForFunction(() => document.querySelector('[data-i18n="snapshotLabel"]').textContent === "Terminal-Bench 2.1");
  await page.locator("#tb-metric").selectOption("api");
  await page.locator('#tb-table-body [data-result-id="fdb8393b-5b29-4645-b784-84f52cf31722"]').click();
  const detail = await page.locator("#tb-detail-content").textContent();
  check(detail.includes("metrics.n_trials = 447; associations = 445"), "Trial-count discrepancy is visible");
  await page.keyboard.press("Escape");
  return {checks, table, layouts};
}
