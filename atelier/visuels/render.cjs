// Rend les visuels en PNG : node atelier/visuels/render.cjs  (nécessite playwright)
const { chromium } = require('playwright');
const path = require('path');
const jobs = [
  ['post.html', 1080, 1350, 'zellijist-atelier-post-1080x1350.png'],
  ['story.html', 1080, 1920, 'zellijist-atelier-story-1080x1920.png'],
].filter(j => !process.argv[2] || j[0].startsWith(process.argv[2]));
(async () => {
  const browser = await chromium.launch();
  for (const [file, w, h, out] of jobs) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto('file://' + path.join(__dirname, file));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.locator('#frame').screenshot({ path: path.join(__dirname, out) });
    console.log('ok', out);
  }
  await browser.close();
})();
