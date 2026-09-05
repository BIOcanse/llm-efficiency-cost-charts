async (page) => {
  // Serve this static fixture through browser request interception: no daemon,
  // listening port, user profile, or published preview is needed.
  await page.unroute("http://127.0.0.1:8765/**");
  await page.route("http://127.0.0.1:8765/**", async (route) => {
    const path = decodeURIComponent(route.request().url().replace("http://127.0.0.1:8765", "").split("?")[0]);
    if (path.includes("..") || path.includes("\\")) return route.abort();
    const resource = path === "/" ? "/index.html" : path;
    const type = resource.endsWith(".js") ? "text/javascript" : resource.endsWith(".css") ? "text/css" : resource.endsWith(".json") ? "application/json" : resource.endsWith(".html") ? "text/html" : undefined;
    await route.fulfill({path: `site${resource}`, contentType: type});
  });
  await page.setViewportSize({width: 1920, height: 1080});
  await page.goto("http://127.0.0.1:8765/?lang=zh-CN");
  await page.locator("#tb-table-body tr").first().waitFor();
  await page.screenshot({path: ".playwright-cli/tb-default.png", fullPage: false});
  return await page.evaluate(() => ({title: document.title, scenario: document.documentElement.dataset.scenario, error: document.querySelector("#tb-error").textContent, status: document.querySelector("#status").textContent, counts: ["token", "api", "subscription"].map(key => document.getElementById(`${key}-count`).textContent), labels: [...document.querySelectorAll("#terminal-panel .interactive-chart-svg")].map(element => ({...element.dataset}))}));
}
