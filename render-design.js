const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--font-render-hinting=none'],
  });

  const page = await browser.newPage();

  await page.setViewport({ width: 1080, height: 1080, deviceScaleFactor: 2 });

  const filePath = 'file://' + path.resolve(__dirname, 'easter-design.html');
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 30000 });

  await new Promise(r => setTimeout(r, 2000));

  await page.screenshot({
    path: path.resolve(__dirname, 'easter-social-media-design.png'),
    type: 'png',
    clip: { x: 0, y: 0, width: 1080, height: 1080 }
  });

  console.log('Screenshot saved to easter-social-media-design.png');

  await browser.close();
})();
