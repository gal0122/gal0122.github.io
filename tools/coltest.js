const { chromium } = require('playwright');
const B = 'http://localhost:8794/';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route(/googletagmanager|map\.naver/, r => r.abort());
  await p.goto(B + 'column.html');
  const res = async () => p.evaluate(() => {
    const r = document.querySelector('.col-results');
    return { shown: !r.hidden, listHidden: document.querySelector('[data-column-list] > .col-list').hidden,
      count: r.querySelector('.col-count strong') ? r.querySelector('.col-count strong').textContent : null,
      head: r.querySelector('.col-count span') ? r.querySelector('.col-count span').textContent : null,
      titles: [...r.querySelectorAll('h2')].map(h => h.textContent.slice(0, 18)), marks: r.querySelectorAll('mark').length,
      snip: r.querySelector('.col-snip') ? r.querySelector('.col-snip').textContent.slice(0, 70) : null,
      empty: r.querySelector('.col-empty') ? 'EMPTY' : '', url: location.search };
  });
  for (const t of ['수염', '레이저 제모', '레이저제모', '본인부담금', '성장판', '추나 한약', '없는단어']) {
    await p.fill('.col-search input', t); await p.waitForTimeout(450);
    console.log(JSON.stringify(t), JSON.stringify(await res()));
  }
  await p.screenshot({ path: 'prev/search-empty-m.png' });
  await p.fill('.col-search input', '수염'); await p.waitForTimeout(400);
  await p.screenshot({ path: 'prev/search-m.png' });
  await p.click('.col-clear'); await p.waitForTimeout(300);
  console.log('after clear', JSON.stringify(await res()), await p.evaluate(() => document.querySelectorAll('[data-column-list] > .col-list .col-item:not([hidden])').length));
  // Enter key submit
  await p.fill('.col-search input', '면도'); await p.press('.col-search input', 'Enter'); await p.waitForTimeout(200);
  console.log('enter', JSON.stringify(await res()));
  // ?q= on load
  await p.goto(B + 'column.html?q=' + encodeURIComponent('엑스레이'));
  await p.waitForTimeout(400);
  console.log('?q', await p.inputValue('.col-search input'), JSON.stringify(await res()));
  // category page
  await p.goto(B + 'column-skin.html');
  console.log('skin chips', await p.$$eval('.col-chips a', as => as.map(a => (a.classList.contains('on') ? '*' : '') + a.textContent + '>' + a.getAttribute('href')).join(' | ')));
  console.log('skin list', await p.$$eval('[data-column-list] > .col-list h2', hs => hs.map(h => h.textContent.slice(0, 20))));
  console.log('skin h1', await p.textContent('h1'), '| crumb', await p.textContent('main p'));
  await p.fill('.col-search input', '교통사고'); await p.waitForTimeout(400);
  console.log('skin search', JSON.stringify(await res()));
  await p.screenshot({ path: 'prev/cat-skin-m.png' });
  // mobile menu links
  console.log('menu', await p.$$eval('.m-menu a[href^="column"]', as => as.map(a => a.textContent + '>' + a.getAttribute('href')).join(' | ')));
  // post page
  await p.goto(B + 'column-laser-hair-removal-sessions.html');
  console.log('post tag', await p.getAttribute('a.col-tag', 'href'), '| crumb', await p.textContent('main p'));
  console.log('next', await p.$$eval('.col-next a', as => as.map(a => a.getAttribute('href'))));
  const ld = await p.$eval('script[type="application/ld+json"]', s => JSON.parse(s.textContent));
  console.log('post bc', JSON.stringify(ld['@graph'].find(g => g['@type'] === 'BreadcrumbList').itemListElement.map(i => i.name + '>' + i.item)));
  await p.goto(B + 'column-skin.html');
  const ld2 = await p.$eval('script[type="application/ld+json"]', s => JSON.parse(s.textContent));
  console.log('cat types', ld2['@graph'].map(g => g['@type']).join(','), JSON.stringify(ld2['@graph'].find(g => g['@type'] === 'BreadcrumbList').itemListElement.map(i => i.name)));
  console.log('title', await p.title());
  console.log('errors', errs);
  await b.close();
})();
