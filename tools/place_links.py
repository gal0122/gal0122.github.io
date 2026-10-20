# 지도 링크를 실제 플레이스(네이버·카카오·구글)로, 모든 페이지 하단에 지도 바로가기
import re, os, glob
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galch', 'project')
NAVER = 'https://naver.me/FW6SmWrn'
KAKAO = 'https://place.map.kakao.com/628214691'
GOOGLE = 'https://maps.google.com/?cid=18044492256827464131'
OLD = {
 'https://map.naver.com/p/search/%EA%B0%88%EC%B0%BD%EB%A6%BC%ED%95%9C%EC%9D%98%EC%9B%90': NAVER,
 'https://map.kakao.com/?q=%EA%B0%88%EC%B0%BD%EB%A6%BC%ED%95%9C%EC%9D%98%EC%9B%90': KAKAO,
 'https://www.google.com/maps/search/?api=1&amp;query=%EA%B2%BD%EB%B6%81%20%EA%B2%BD%EC%82%B0%EC%8B%9C%20%ED%95%98%EC%96%91%EC%9D%8D%20%EB%8F%99%EC%84%9C2%EA%B8%B8%2043': GOOGLE,
}
INSTA = '<a href="https://www.instagram.com/gal__clinic/" target="_blank" rel="noopener" style="color: #ffffff; text-decoration: none">인스타그램</a>'
FOOT = ''.join(f'\n<a href="{u}" target="_blank" rel="noopener" data-place-link="true" style="color: #ffffff; text-decoration: none">{n}</a>'
               for n, u in [('네이버 지도', NAVER), ('카카오맵', KAKAO), ('구글 지도', GOOGLE)])
SKIP = {'HomeA.dc.html', 'HomeB.dc.html', 'HomeC.dc.html', 'ColorOptions.dc.html'}
n_foot = 0
for p in sorted(glob.glob(f'{G}/*.dc.html')):
    b = os.path.basename(p)
    if b in SKIP:
        continue
    t = open(p, encoding='utf-8').read()
    o = t
    for a, c in OLD.items():
        t = t.replace(a, c)
    t = re.sub(r'\n<a href="[^"]*" target="_blank" rel="noopener" data-place-link="true"[^>]*>[^<]*</a>', '', t)   # idempotent
    if INSTA in t:
        t = t.replace(INSTA, INSTA + FOOT)
        n_foot += 1
    if b == 'Schedule.dc.html':
        btn = None if 'data-place-btns' in t else re.search(r'<a href="' + re.escape(NAVER) + r'" target="_blank" rel="noopener" style="display: inline-flex;[^"]*">네이버지도에서 보기<svg.*?</svg></a>', t, re.S)
        if True:
            line = 'flex: 0 0 auto; display: inline-flex; align-items: center; gap: 8px; min-height: 48px; padding: 0 20px; text-decoration: none; font-weight: 500'
            arrow = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7"></path><path d="M8 7h9v9"></path></svg>'
            group = ('<div data-place-btns="true" class="eq-track" style="display: flex; gap: 8px; overflow-x: auto; max-width: 100%">\n'
                     f'<a href="{NAVER}" target="_blank" rel="noopener" style="{line}; background: #2f5241; color: #ffffff">네이버 지도{arrow}</a>\n'
                     f'<a href="{KAKAO}" target="_blank" rel="noopener" style="{line}; background: #ffffff; border: 1px solid #d7c9a7; color: #2f5241">카카오맵{arrow}</a>\n'
                     f'<a href="{GOOGLE}" target="_blank" rel="noopener" style="{line}; background: #ffffff; border: 1px solid #d7c9a7; color: #2f5241">구글 지도{arrow}</a>\n'
                     '</div>')
        if btn:
            t = t[:btn.start()] + group + t[btn.end():]
        elif 'data-place-btns' not in t:
            h2 = '<h2 style="margin: 0; font-size: 30px">오시는길</h2>\n'
            t = t.replace(h2, h2 + group + '\n', 1)
    if t != o:
        open(p, 'w', encoding='utf-8').write(t)
print('footers', n_foot)
