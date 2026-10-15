"""내과 질환 아트보드 4장 (척추 질환 페이지와 같은 양식).
Header/footer come from PainSpine.dc.html; run after the menus already contain 내과 질환.
Cards may link to 원장 칼럼 posts with <a data-col="slug" href="column-slug.html">; build_site.py drops
those links until the post is published."""
import os

S = os.path.dirname(os.path.abspath(__file__))
G = f'{S}/galch/project/'
REVIEWED = '2026년 10월 15일'

BLOB = {'digestive': '98469f8aea4e8f4709a2c1030f09339b', 'headache': 'd510667e5acca8254235c649460c5f90',
        'sleep': '41236daa076c2d94f1778e0e42d10457', 'nose': 'bab882a43d90bfdf0de24c740f8f53dd',
        'cold': '3a6d25e247cbd9749163e1df296445c8'}
TABS = [('InternalDigestive', '소화기 질환'), ('InternalNeuro', '두통·신경 질환'),
        ('InternalSleep', '불면·스트레스'), ('InternalRhinitis', '비염·수족냉증')]

EYEBROW = 'margin: 0; font-size: 14px; font-weight: 700; color: #7a6b42; letter-spacing: 0.04em'
CHECK_SVG = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink: 0; margin-top: 4px">'
             '<path d="M20 6L9 17l-5-5"></path></svg>')
PREV_BTN = ('<button type="button" aria-label="{a}" onClick="{{{{ prev }}}}" style="width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; padding: 0; border: 1px solid #2f5241; background: #ffffff; color: #24302a; cursor: pointer">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg></button>')
NEXT_BTN = ('<button type="button" aria-label="{a}" onClick="{{{{ next }}}}" style="width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; padding: 0; border: 1px solid #2f5241; background: #2f5241; color: #ffffff; cursor: pointer">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"></path></svg></button>')


def hero(board, h1, sub):
    tabs = []
    for b, name in TABS:
        if b == board:
            tabs.append(f'<a href="{b}.dc.html" aria-current="page" style="flex: 0 0 auto; padding: 14px 0; border-bottom: 3px solid #2f5241; font-weight: 700; text-decoration: none">{name}</a>')
        else:
            tabs.append(f'<a href="{b}.dc.html" style="flex: 0 0 auto; padding: 14px 0; border-bottom: 3px solid transparent; color: #5d655f; text-decoration: none">{name}</a>')
    return f'''<section style="background: #f1ede3; border-bottom: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 0; display: flex; flex-direction: column; gap: 12px">
<p style="margin: 0; font-size: 14px; color: #5d655f">홈 &gt; 내과 질환 &gt; {h1}</p>
<h1 style="margin: 0; font-size: 40px; line-height: 1.3">{h1}</h1>
<p style="margin: 0; font-size: 18px; color: #4d554f">{sub}</p>
<nav aria-label="내과 질환 하위 메뉴" class="eq-track" style="display: flex; gap: 0 32px; margin-top: 24px; font-size: 15px; overflow-x: auto; white-space: nowrap">
{chr(10).join(tabs)}
</nav>
</div>
</section>
'''


def figure(blob, alt, caption, minw=900, maxw=None):
    mw = f' max-width: {maxw}px;' if maxw else ''
    return f'''<figure style="margin: 0; display: flex; flex-direction: column; gap: 12px">
<div class="eq-track" style="overflow-x: auto"><img src="/_blob/{BLOB[blob]}" alt="{alt}" style="display: block; width: 100%;{mw} min-width: {minw}px; height: auto"></div>
<figcaption style="font-size: 14px; color: #5d655f">{caption}</figcaption>
</figure>'''


def intro(eyebrow, h2, paras, point, fig):
    ps = '\n'.join(f'<p style="margin: 0; font-size: 17px; color: #4d554f">{p}</p>' for p in paras)
    return f'''<section style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 16px; max-width: 820px">
<p style="{EYEBROW}">{eyebrow}</p>
<h2 style="margin: 0; font-size: 32px; line-height: 1.4">{h2}</h2>
{ps}
<p style="margin: 8px 0 0; padding-left: 16px; border-left: 3px solid #2f5241; font-size: 17px; font-weight: 500">{point}</p>
</div>
{fig}
</section>
'''


def card(num, title, desc, symptoms, col=None, basis='300px'):
    link = (f'\n<p style="margin: 0; font-size: 15px; font-weight: 500"><a data-col="{col}" href="column-{col}.html">원장 칼럼에서 자세히 보기 →</a></p>'
            if col else '')
    return f'''<article style="flex: 1 0 {basis}; scroll-snap-align: start; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; padding: 28px 24px; background: #ffffff; border: 1px solid #e2dccd">
<p style="{EYEBROW}">{num:02d}</p>
<h4 style="margin: 0; font-size: 21px">{title}</h4>
<p style="margin: 0; color: #4d554f; font-size: 15px">{desc}</p>
<p style="margin: auto 0 0; padding-top: 12px; border-top: 1px solid #e2dccd; font-size: 15px"><strong>이런 증상</strong> · {symptoms}</p>{link}
</article>'''


def conditions(h2, groups):
    out, n = [], 0
    for g in groups:
        name, cards, fig = g.get('h3'), g['cards'], g.get('fig', '')
        items = []
        for c in cards:
            n += 1
            items.append(card(n, *c))
        h3 = f'<h3 style="margin: 0; font-size: 22px">{name}</h3>\n' if name else ''
        label = name or h2
        out.append(f'''<div style="display: flex; flex-direction: column; gap: 20px">
{h3}{fig + chr(10) if fig else ''}<div class="eq-track" role="region" aria-label="{label}" tabindex="0" style="display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 12px">
{chr(10).join(items)}
</div>
</div>''')
    return f'''<section style="background: #f1ede3; border-top: 1px solid #e2dccd; border-bottom: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 48px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">CONDITIONS</p>
<h2 style="margin: 0; font-size: 30px">{h2}</h2>
</div>
{chr(10).join(out)}
</div>
</section>
'''


def compare(eyebrow, h2, desc, cols, rows, note, label, border=False, minw=760):
    w = '45%' if len(cols) == 1 else '22%' if len(cols) == 2 else '19%'
    th = '\n'.join(f'<th scope="col" style="padding: 16px 20px; font-size: 17px">{c}</th>' for c in cols)
    trs = '\n'.join('<tr style="border-bottom: 1px solid #e2dccd"><th scope="row" style="padding: 16px 20px; font-weight: 500">'
                    + r[0] + '</th>' + ''.join(f'<td style="padding: 16px 20px; color: #4d554f">{v}</td>' for v in r[1:]) + '</tr>'
                    for r in rows)
    sec = '<section style="border-top: 1px solid #e2dccd">' if border else '<section>'
    return f'''{sec}
<div style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 32px">
<div style="display: flex; flex-direction: column; gap: 8px; max-width: 820px">
<p style="{EYEBROW}">{eyebrow}</p>
<h2 style="margin: 0; font-size: 30px">{h2}</h2>
<p style="margin: 0; color: #4d554f">{desc}</p>
</div>
<div class="eq-track" role="region" aria-label="{label}" tabindex="0" style="overflow-x: auto; padding-bottom: 12px">
<table style="width: 100%; min-width: {minw}px; border-collapse: collapse; font-size: 16px; text-align: left">
<thead>
<tr style="border-top: 2px solid #2f5241; border-bottom: 1px solid #2f5241">
<th scope="col" style="width: {w}; padding: 16px 20px; font-size: 15px"></th>
{th}
</tr>
</thead>
<tbody>
{trs}
</tbody>
</table>
</div>
<p style="margin: 0; font-size: 14px; color: #5d655f">{note}</p>
</div>
</section>
'''


def check(desc, items):
    lis = '\n'.join(f'<li style="display: flex; gap: 12px; align-items: flex-start; padding: 16px 0; border-bottom: 1px solid #e2dccd">{CHECK_SVG}{i}</li>' for i in items)
    return f'''<section style="border-top: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 48px; align-items: start">
<div style="display: flex; flex-direction: column; gap: 16px">
<p style="{EYEBROW}">CHECK</p>
<h2 style="margin: 0; font-size: 30px; line-height: 1.4">이런 증상이 있다면<br>진료를 받아 보세요</h2>
<p style="margin: 0; color: #4d554f">{desc}</p>
<a href="tel:053-851-0122" style="align-self: flex-start; display: inline-flex; align-items: center; min-height: 48px; padding: 0 24px; margin-top: 8px; background: #2f5241; color: #ffffff; text-decoration: none; font-weight: 500">상담 예약하기</a>
</div>
<ul style="list-style: none; margin: 0; padding: 0; border-top: 1px solid #2f5241; font-size: 17px">
{lis}
</ul>
</div>
</section>
'''


def treatment(h2, desc, label, cards):
    arts = '\n'.join(f'''<article style="flex: 1 0 340px; scroll-snap-align: start; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; padding: 28px; border: 1px solid #e2dccd">
<p style="{EYEBROW}">{i + 1:02d} · {tag}</p>
<h3 style="margin: 0; font-size: 26px">{name}</h3>
<p style="margin: 0; font-weight: 500">{lead}</p>
<p style="margin: 0; color: #4d554f">{body}</p>
<p style="margin: auto 0 0; padding-top: 12px; border-top: 1px solid #e2dccd; font-size: 15px"><strong>이런 분께</strong> · {who}</p>
</article>''' for i, (tag, name, lead, body, who) in enumerate(cards))
    return f'''<section style="border-top: 1px solid #e2dccd">
<div data-eq-slider="true" style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 32px">
<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 16px">
<div style="display: flex; flex-direction: column; gap: 8px; max-width: 820px">
<p style="{EYEBROW}">TREATMENT</p>
<h2 style="margin: 0; font-size: 30px">{h2}</h2>
<p style="margin: 0; color: #4d554f">{desc}</p>
</div>
<div style="display: flex; gap: 8px; flex-shrink: 0">
{PREV_BTN.format(a='이전 치료 보기')}
{NEXT_BTN.format(a='다음 치료 보기')}
</div>
</div>
<div data-eq-track="true" class="eq-track" role="region" aria-label="{label}" tabindex="0" style="display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; padding-bottom: 12px">
{arts}
</div>
</div>
</section>
'''


def flow(desc, label, steps, note='※ 그날의 몸 상태에 따라 일부 치료는 달라질 수 있습니다.'):
    lis = '\n'.join(f'<li style="flex: 0 0 260px; scroll-snap-align: start; box-sizing: border-box; display: flex; flex-direction: column; gap: 8px; padding: 24px; background: #ffffff"><span style="font-size: 14px; font-weight: 700">STEP {i + 1}</span><strong style="font-size: 17px">{a}</strong><span style="color: #4d554f; font-size: 15px">{b}</span></li>'
                    for i, (a, b) in enumerate(steps))
    return f'''<section style="background: #f1ede3; border-top: 1px solid #e2dccd; border-bottom: 1px solid #e2dccd">
<div data-eq-slider="true" style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 16px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">FLOW</p>
<h2 style="margin: 0; font-size: 30px">내원하시면 이렇게 진행됩니다</h2>
<p style="margin: 0; color: #4d554f">{desc}</p>
</div>
<div style="display: flex; gap: 8px; flex-shrink: 0">
{PREV_BTN.format(a='이전 단계 보기')}
{NEXT_BTN.format(a='다음 단계 보기')}
</div>
</div>
<ol data-eq-track="true" class="eq-track" aria-label="{label}" tabindex="0" style="list-style: none; margin: 0; padding: 0 0 16px; display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth">
{lis}
</ol>
<p style="margin: 0; font-size: 14px; color: #5d655f">{note}</p>
</div>
</section>
'''


def caution(h2, desc, items, after=''):
    lis = '\n'.join(f'<li>{i}</li>' for i in items)
    tail = f'\n<p style="margin: 0; color: #4d554f">{after}</p>' if after else ''
    return f'''<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 20px; padding: 40px; border: 2px solid #2f5241">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">CAUTION</p>
<h2 style="margin: 0; font-size: 26px">{h2}</h2>
<p style="margin: 0; color: #4d554f">{desc}</p>
</div>
<ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 8px; font-size: 16px">
{lis}
</ul>{tail}
</div>
</div>
</section>
'''


def care(h2, items, note='※ 치료에 대한 반응과 회복 속도는 개인차가 있습니다.'):
    lis = '\n'.join(f'<li style="display: flex; gap: 16px; padding: 16px 0; border-bottom: 1px solid #e2dccd"><strong style="flex-shrink: 0; width: 28px">{i + 1:02d}</strong><span style="color: #4d554f">{v}</span></li>'
                    for i, v in enumerate(items))
    return f'''<section style="border-top: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">CARE</p>
<h2 style="margin: 0; font-size: 30px">{h2}</h2>
</div>
<ol style="margin: 0; padding: 0; list-style: none; border-top: 1px solid #2f5241; font-size: 16px">
{lis}
</ol>
<p style="margin: 0; font-size: 14px; color: #5d655f">{note}</p>
</div>
</section>
'''


def faq(items):
    ds = '\n'.join(f'''<details style="border-bottom: 1px solid #e2dccd">
<summary style="display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; font-size: 17px; font-weight: 500">Q. {q}<span class="faq-icon" aria-hidden="true" style="flex-shrink: 0; font-size: 24px; line-height: 1">+</span></summary>
<p style="margin: 0 0 20px; color: #4d554f">{a}</p>
</details>''' for q, a in items)
    return f'''<section style="border-top: 1px solid #e2dccd">
<div class="faq" style="max-width: 1240px; margin: 0 auto; padding: 88px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">FAQ</p>
<h2 style="margin: 0; font-size: 30px">자주 묻는 질문</h2>
</div>
<div style="border-top: 1px solid #2f5241">
{ds}
</div>
</div>
</section>
'''


def time_section(h2):
    src = open(G + 'PainSpine.dc.html', encoding='utf-8').read()
    i = src.find('<p style="margin: 0; font-size: 14px; font-weight: 700; color: #7a6b42; letter-spacing: 0.04em">TIME</p>')
    a = src.rfind('<section', 0, i)
    b = src.find('</section>', i) + len('</section>')
    sec = src[a:b]
    return sec.replace('출근 전에도, 주말에도 치료받을 수 있습니다', h2) + '\n'


def next_section(cards):
    cs = '\n'.join(f'''<a href="{href}" style="flex: 1 0 300px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; padding: 28px 24px; background: #ffffff; border: 1px solid #e2dccd; text-decoration: none">
<strong style="font-size: 20px">{name}</strong>
<span style="color: #4d554f; font-size: 15px">{desc}</span>
<span style="margin-top: auto; padding-top: 8px; font-size: 14px; color: #5d655f">자세히 보기 →</span>
</a>''' for href, name, desc in cards)
    return f'''<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 72px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{EYEBROW}">NEXT</p>
<h2 style="margin: 0; font-size: 28px">함께 보면 좋은 내용</h2>
</div>
<div class="eq-track" role="region" aria-label="관련 페이지" tabindex="0" style="display: flex; gap: 16px; overflow-x: auto; padding-bottom: 12px">
{cs}
</div>
</div>
</section>
'''


def reviewed():
    src = open(G + 'PainSpine.dc.html', encoding='utf-8').read()
    a = src.find('<section aria-label="작성 및 검토 정보">')
    b = src.find('</section>', a) + len('</section>')
    import re
    return re.sub(r'최종 검토 \d{4}년 \d{1,2}월 \d{1,2}일', f'최종 검토 {REVIEWED}', src[a:b]) + '\n'


def cta(h2, p):
    return f'''<section style="background: #f1ede3; border-top: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 72px 24px; display: flex; flex-direction: column; align-items: center; gap: 16px; text-align: center">
<h2 style="margin: 0; font-size: 28px">{h2}</h2>
<p style="margin: 0; color: #4d554f">{p}</p>
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 8px">
<a href="https://talk.naver.com/W4F2TI" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; min-height: 48px; padding: 0 24px; border: 1px solid #2f5241; background: #ffffff; text-decoration: none; font-weight: 500">네이버상담</a>
<a href="tel:053-851-0122" style="display: inline-flex; align-items: center; min-height: 48px; padding: 0 24px; background: #2f5241; color: #ffffff; text-decoration: none; font-weight: 500">전화 상담</a>
</div>
</div>
</section>
'''


def write_board(board, title, main):
    src = open(G + 'PainSpine.dc.html', encoding='utf-8').read()
    head, rest = src.split('<main>\n', 1)
    tail = rest.split('</main>', 1)[1]
    head = head.replace('<title>척추 질환</title>', f'<title>{title}</title>')
    open(G + board + '.dc.html', 'w', encoding='utf-8').write(head + '<main>\n\n' + main + '\n</main>' + tail)


from internal_content import PAGES   # noqa: E402

for board, title, build in PAGES:
    write_board(board, title, build(globals()))
    print('wrote', board)
