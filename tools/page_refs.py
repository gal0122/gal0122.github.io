# 진료 페이지 맨 아래 '참고 자료' (원장 검토 2026-10-20) — 작성·검토 정보 바로 위. 다시 실행해도 한 번만 들어감
import re, os, html
from refs_data import R, PAGES
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galch', 'project')
for b, keys in PAGES.items():
    p = f'{G}/{b}.dc.html'
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'<section data-refs="true".*?</section>\n\n?', '', t, flags=re.S)
    lis = ''.join(f'<li><a href="{html.escape(R[k][1])}" target="_blank" rel="noopener" style="color: #2f5241">{R[k][0]}</a></li>\n' for k in keys)
    sec = ('<section data-refs="true" aria-label="참고 자료">\n'
           '<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 0">\n'
           '<div style="padding-top: 20px; border-top: 1px solid #e2dccd; display: flex; flex-direction: column; gap: 8px; font-size: 14px; color: #5d655f">\n'
           '<strong style="font-size: 15px; color: #24302a">참고 자료</strong>\n'
           f'<ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 4px">\n{lis}</ul>\n'
           '</div>\n</div>\n</section>\n\n')
    a = '<section aria-label="작성 및 검토 정보">'
    assert t.count(a) == 1, b
    t = t.replace(a, sec + a)
    open(p, 'w', encoding='utf-8').write(t)
    print(b, len(keys))
