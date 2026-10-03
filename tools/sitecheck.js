const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const pages = fs.readdirSync('/home/claude/site').filter(f => f.endsWith('.html'));
  const files = new Set(fs.readdirSync('/home/claude/site'));
  let bad = 0;
  for (const f of pages) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const fails = [], errs = [];
    p.on('requestfailed', r => { if (!r.url().includes('naver.com')) fails.push(r.url()); });
    p.on('response', r => { if (r.status() >= 400) fails.push(r.status() + ' ' + r.url()); });
    p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/' + f, { waitUntil: 'load' });
    await p.waitForTimeout(300);
    const info = await p.evaluate(async () => {
      await document.fonts.ready;
      const font = document.fonts.check('16px Pretendard');
      const brokenImg = [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src').slice(0, 40));
      const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => !/^(https?:|tel:|mailto:|#)/.test(h));
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
      const badAnchors = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !ids.includes(h.slice(1)));
      return { font, brokenImg, links, badAnchors, mapBoxes: document.querySelectorAll('[data-naver-map]').length };
    });
    const deadLinks = [...new Set(info.links.map(h => h.split('#')[0]))].filter(h => !files.has(h));
    const ok = !fails.length && !errs.length && info.font && !info.brokenImg.length && !deadLinks.length && !info.badAnchors.length;
    if (!ok) bad++;
    console.log((ok ? 'OK ' : 'BAD') + ' ' + f + (info.mapBoxes ? ' map=' + info.mapBoxes : '') + (ok ? '' : ' ' + JSON.stringify({ fails, errs, font: info.font, brokenImg: info.brokenImg, deadLinks, badAnchors: info.badAnchors })));
    await p.close();
  }
  console.log('bad pages:', bad);
  await b.close();
})();
