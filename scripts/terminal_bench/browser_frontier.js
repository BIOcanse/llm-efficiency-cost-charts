async (page) => {
  const checks = [];
  const check = (ok, message) => {if (!ok) throw new Error(message); checks.push(message);};
  const expected = {"4.0": [5,5,4], "3.0": [4,4,5], "2.1": [5,5,5], "2.0": [0,0,0], "1.0": [0,0,0]};
  const metrics = ["subscription", "api", "token"];
  for (const width of [1920, 1440]) {
    await page.setViewportSize({width, height: 1080});
    for (const language of ["zh-CN", "en"]) {
      await page.locator(`[data-language="${language}"]`).click();
      for (const [version, counts] of Object.entries(expected)) {
        await page.locator("#tb-version").selectOption(version);
        await page.waitForFunction(v => document.querySelector('[data-i18n="snapshotLabel"]').textContent === `Terminal-Bench ${v}` && !document.querySelector("#tb-snapshot").disabled, version);
        if (counts.every(value => !value)) {
          check(await page.locator("#tb-no-usage").isVisible(), `${width}/${language}/TB${version} missing-frontier notice`);
          continue;
        }
        const values = await page.evaluate(() => ["subscription", "api", "token"].map(metric => ({
          metric, ids: [...document.querySelectorAll(`#tb-frontier-table-${metric} [data-frontier-id]`)].map(element => element.dataset.frontierId),
          count: Number(document.querySelector(`#tb-chart-${metric} svg`).dataset.frontierCount),
          collision: Number(document.querySelector(`#tb-chart-${metric} svg`).dataset.labelCollisions),
          steps: document.querySelector(`#tb-chart-${metric} .interactive-pareto-line`).getAttribute("d"),
        })));
        const payload = await page.evaluate(async v => (await fetch(`data/terminal-bench/${v}/${document.querySelector("#tb-snapshot").value}.json`)).json(), version);
        check(values.every((item, i) => item.count === counts[i] && item.ids.length === counts[i] && JSON.stringify(item.ids) === JSON.stringify(payload.frontiers[item.metric])), `${width}/${language}/TB${version} list and line match saved frontier`);
        check(values.every(item => item.collision === 0 && item.steps.length > 0), `${width}/${language}/TB${version} step lines and labels`);
      }
    }
  }
  await page.locator("#tb-version").selectOption("4.0");
  await page.waitForFunction(() => document.querySelector('[data-i18n="snapshotLabel"]').textContent === "Terminal-Bench 4.0");
  const chart = page.locator("#tb-chart-subscription");
  await chart.locator("select").first().selectOption("Anthropic");
  check(await page.locator("#tb-frontier-table-subscription [data-frontier-id]").count() === 2, "Provider filter recalculates frontier");
  const before = await page.locator("#tb-frontier-table-subscription [data-frontier-id]").evaluateAll(nodes => nodes.map(node => node.dataset.frontierId));
  await chart.locator(".interactive-zoom-controls button").nth(1).click();
  check(JSON.stringify(await page.locator("#tb-frontier-table-subscription [data-frontier-id]").evaluateAll(nodes => nodes.map(node => node.dataset.frontierId))) === JSON.stringify(before), "Zoom does not recalculate membership");
  await page.locator("#tb-frontier-toggle-subscription").uncheck();
  check(await chart.locator(".interactive-pareto-line").count() === 0 && await page.locator("#tb-frontier-table-subscription [data-frontier-id]").count() === 2, "Overlay can hide without changing frontier list");
  await page.locator("#tb-frontier-toggle-subscription").check();
  await chart.locator("select").nth(1).selectOption("Codex");
  check(await chart.locator(".interactive-point").count() === 0 && await page.locator("#tb-frontier-table-subscription [data-frontier-id]").count() === 0, "Empty provider/agent combination clears stale points and list");
  await chart.locator("select").first().selectOption("");
  await chart.locator("select").nth(1).selectOption("all");
  await chart.locator(".interactive-zoom-controls button").last().click();
  await page.locator("#tb-frontier-table-subscription button").first().click();
  check(await page.locator("#tb-detail").isVisible(), "Frontier list opens the existing source detail");
  await page.keyboard.press("Escape");
  check((await page.locator("#tb-image-subscription").getAttribute("href")).endsWith("/en/07_subscription_frontier.png"), "Download selects supplemental figure");
  await page.evaluate(() => scrollTo(0, document.querySelector("#tb-chart-subscription").getBoundingClientRect().top + scrollY - 75));
  await page.screenshot({path: ".playwright-cli/tb-frontier-chart-en.png"});
  await page.evaluate(() => scrollTo(0, document.querySelector("#tb-frontier-table-subscription").getBoundingClientRect().top + scrollY - 240));
  await page.screenshot({path: ".playwright-cli/tb-frontier-list-en.png"});
  await page.locator('[data-language="zh-CN"]').click();
  await page.evaluate(() => scrollTo(0, document.querySelector("#tb-frontier-table-subscription").getBoundingClientRect().top + scrollY - 240));
  await page.screenshot({path: ".playwright-cli/tb-frontier-list-zh.png"});
  return {checks, checked: checks.length};
}
