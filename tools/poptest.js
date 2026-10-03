const { chromium } = require('playwright');
const U = 'http://localhost:8765/index.html';
async function state(p) {
  return p.evaluate(() => {
    const o = document.getElementById('site-popups');
    const vis = o && !o.hidden ? [...o.querySelectorAll('.pop')].filter(x => x.style.display !== 'none').map(x => x.dataset.pop) : [];
    return { open: !!(o && !o.hidden), vis, lock: document.documentElement.style.overflow };
  });
}
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.clock.setFixedTime(new Date('2026-10-03T10:00:00+09:00'));
  await p.goto(U); await p.waitForTimeout(300);
  console.log('1 desktop first visit       ', JSON.stringify(await state(p)));
  await p.screenshot({ path: 'prev/pop-site-desk.png' });
  // close October popup WITH 24h checkbox
  await p.check('[data-pop="closed-2026-10"] .pop-check input');
  await p.click('[data-pop="closed-2026-10"] .pop-close');
  console.log('2 after closing Oct (24h)   ', JSON.stringify(await state(p)));
  // close event popup WITHOUT checkbox
  await p.click('[data-pop="event-end-2026"] .pop-close');
  console.log('3 after closing event       ', JSON.stringify(await state(p)));
  await p.reload(); await p.waitForTimeout(300);
  console.log('4 reload: Oct snoozed       ', JSON.stringify(await state(p)));
  await p.clock.setFixedTime(new Date('2026-10-04T10:30:00+09:00'));  // 24.5h later
  await p.reload(); await p.waitForTimeout(300);
  console.log('5 next day: both back       ', JSON.stringify(await state(p)));
  await p.clock.setFixedTime(new Date('2026-10-19T09:00:00+09:00'));
  await p.reload(); await p.waitForTimeout(300);
  console.log('6 Oct 19: Oct expired       ', JSON.stringify(await state(p)));
  await p.clock.setFixedTime(new Date('2027-01-01T09:00:00+09:00'));
  await p.reload(); await p.waitForTimeout(300);
  console.log('7 2027-01-01: none          ', JSON.stringify(await state(p)));
  // backdrop click closes all (no snooze)
  await p.clock.setFixedTime(new Date('2026-10-05T12:00:00+09:00'));
  await ctx.clearCookies(); await p.evaluate(() => localStorage.clear());
  await p.reload(); await p.waitForTimeout(300);
  await p.mouse.click(60, 850);
  console.log('8 backdrop click            ', JSON.stringify(await state(p)));
  // mobile: one at a time
  const m = await b.newPage({ viewport: { width: 375, height: 760 } });
  await m.clock.setFixedTime(new Date('2026-10-03T10:00:00+09:00'));
  await m.goto(U); await m.waitForTimeout(300);
  console.log('9 mobile first              ', JSON.stringify(await state(m)));
  await m.screenshot({ path: 'prev/pop-site-m1.png' });
  await m.click('[data-pop="event-end-2026"] .pop-close');
  console.log('10 mobile after close       ', JSON.stringify(await state(m)));
  await m.screenshot({ path: 'prev/pop-site-m2.png' });
  const a = await b.newPage(); await a.goto('http://localhost:8765/about.html');
  console.log('11 about page popups?       ', await a.evaluate(() => !!document.getElementById('site-popups')));
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
