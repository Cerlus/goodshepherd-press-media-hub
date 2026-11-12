// Rasterise SVG files to PNG with Playwright's Chromium: node tools/raster.js '<json list of {svg, png, w, h}>'
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const br = await chromium.launch();
  for (const j of jobs) {
    const page = await br.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await page.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(j.svg, 'utf8')}</body></html>`);
    await page.waitForTimeout(250);
    await page.screenshot({ path: j.png, omitBackground: true });
    await page.close();
  }
  await br.close();
})();
