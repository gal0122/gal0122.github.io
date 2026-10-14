const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 664 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await p.route(/googletagmanager|oapi\.map\.naver/, r => r.abort());
  await p.goto('http://localhost:8794/' + (process.argv[2] || 'price.html'));
  await p.evaluate(() => { const o = document.getElementById('site-popups'); if (o) o.remove(); });
  await p.click('.m-menu summary');
  await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const nav = document.querySelector('nav[aria-label="전체 메뉴"]');
    nav.scrollTop = nav.scrollHeight;
    const nr = nav.getBoundingClientRect(), qn = document.querySelector('.qn').getBoundingClientRect();
    const links = [...nav.querySelectorAll('a')]; const last = links[links.length - 1].getBoundingClientRect();
    return { navBottom: nr.bottom, qnTop: qn.top, lastText: links[links.length - 1].textContent.trim(), lastBottom: last.bottom, vh: innerHeight };
  });
  console.log(JSON.stringify(r));
  await p.screenshot({ path: 'prev/menu-' + (process.argv[3] || 'before') + '.png' });
  await b.close();
})();
