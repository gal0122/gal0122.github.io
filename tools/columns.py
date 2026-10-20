"""원장 칼럼: Markdown posts (galch/columns/*.md) -> HTML pieces for the list page and the post template.

Each post file:
---
title / slug / category / date / reviewed / description / summary
related: page.html | label; page.html#anchor | label
---
Markdown body. A final "## 자주 묻는 질문" section with "Q. …" / "A. …" lines becomes the FAQ accordion.
"""
import glob, html, os, re
import markdown

CATEGORIES = [('skin', '피부미용'), ('traffic', '교통사고'), ('pain', '근골격계 통증'), ('internal', '내과 질환'),
              ('diet', '다이어트'), ('kids-women', '소아·여성')]
CAT_KEY = {name: key for key, name in CATEGORIES}
CAT_NAME = dict(CATEGORIES)
# hero text of each category page (column-<key>.html)
CAT_INTRO = {
    'all': '피부미용과 교통사고, 척추·관절 통증, 내과 질환, 다이어트, 소아·여성 건강까지. 진료실에서 자주 받는 질문에 갈창림 대표원장이 직접 답합니다.',
    'skin': '기미·흑자 같은 색소와 점, 검버섯, 쥐젖 같은 피부 돌기, 아토피와 원형 탈모부터 레이저제모, 리프팅, 여드름, 모공, 스킨부스터까지. 피부 고민과 시술에 대해 궁금한 점을 갈창림 대표원장이 정리했습니다.',
    'traffic': '교통사고 뒤 며칠이 지나 나타나는 목·허리 통증과 두통, 어지럼, 잠을 설치는 증상처럼 사고 후 생기는 후유증을 다룹니다. 치료는 언제 시작하는 것이 좋은지, 자동차보험 진료는 어떻게 접수하는지 등 진료실에서 자주 받는 질문을 갈창림 대표원장이 정리했습니다.',
    'pain': '허리·목 디스크, 담 결림, 오십견, 무릎 통증, 발목 염좌처럼 척추와 관절, 근육에 생기는 통증을 갈창림 대표원장이 정리했습니다.',
    'internal': '소화불량, 역류성 식도염, 과민성 대장 증후군, 두통, 안면마비, 손발 저림, 불면증, 화병, 만성 피로, 비염, 수족냉증처럼 일상을 힘들게 하는 내과 질환을 다룹니다. 검사에서는 이상이 없다는데 계속 불편할 때 무엇을 살펴야 하는지, 먼저 병원 검사가 필요한 경우는 언제인지 갈창림 대표원장이 정리했습니다.',
    'diet': '한약 다이어트는 어떻게 진행되는지, 감량 뒤 요요 없이 유지하려면 무엇을 지켜야 하는지 등 체중 관리에 대해 자주 받는 질문을 갈창림 대표원장이 정리했습니다.',
    'kids-women': '아이 키 성장 치료를 언제 시작하면 좋은지, 성장을 방해하는 생활 습관은 무엇인지부터 생리통, 산후풍, 갱년기처럼 시기마다 달라지는 여성 건강까지 다룹니다. 보호자와 환자분들이 진료실에서 자주 묻는 질문을 갈창림 대표원장이 정리했습니다.',
}

FAQ_SUMMARY = ('<summary style="display: flex; justify-content: space-between; align-items: center; gap: 16px; '
               'padding: 20px 0; font-size: 17px; font-weight: 500">')
FAQ_ICON = ('<span class="faq-icon" aria-hidden="true" style="flex-shrink: 0; font-size: 24px; line-height: 1">+</span>'
            '</summary>')


def load_posts(folder):
    posts = []
    for fp in sorted(glob.glob(os.path.join(folder, '*.md'))):
        raw = open(fp, encoding='utf-8').read()
        m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
        assert m, fp
        meta = {}
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        for k in ('title', 'slug', 'category', 'date', 'reviewed', 'description', 'summary'):
            assert meta.get(k), (fp, k)
        assert meta['category'] in CAT_KEY, (fp, meta['category'])
        body, faq = m.group(2), []
        fm = re.search(r'\n## 자주 묻는 질문\s*\n(.*)$', body, re.S)
        if fm:
            body = body[:fm.start()]
            for q, a in re.findall(r'Q\.\s*(.+?)\nA\.\s*(.+?)(?=\n\s*\nQ\.|\s*$)', fm.group(1).strip(), re.S):
                faq.append((q.strip(), ' '.join(a.split())))
        related = []
        for part in filter(None, (p.strip() for p in meta.get('related', '').split(';'))):
            href, label = (x.strip() for x in part.split('|', 1))
            related.append((href, label))
        meta.update(body_md=body.strip(), faq=faq, related=related, cat_key=CAT_KEY[meta['category']],
                    file=f"column-{meta['slug']}.html", src=os.path.basename(fp))
        assert meta['slug'] not in CAT_NAME, (fp, 'slug clashes with a category page')
        posts.append(meta)
    assert len({p['slug'] for p in posts}) == len(posts), 'duplicate slug'
    # newest first; posts of the same day by file name (2026-10-14b-… comes before 2026-10-14-…)
    posts.sort(key=lambda p: (p['date'], p['src']), reverse=True)
    return posts


def kdate(iso, sep='.'):
    y, mo, d = iso.split('-')
    return f'{y}{sep}{mo}{sep}{d}' if sep else f'{int(y)}년 {int(mo)}월 {int(d)}일'


def cat_file(key):
    """Page that lists one category ('all' = every column)."""
    return 'column.html' if key == 'all' else f'column-{key}.html'


def used_categories(posts):
    """Categories that have at least one post, in menu order (empty ones get no page, chip or menu link)."""
    have = {p['cat_key'] for p in posts}
    return [(k, n) for k, n in CATEGORIES if k in have]


def list_items(posts, link):
    out = []
    for p in posts:
        out.append(
            f'<article class="col-item" data-cat="{p["cat_key"]}">\n'
            f'<a href="{link(p)}">\n'
            f'<span class="col-tag">{html.escape(p["category"])}</span>\n'
            f'<h2>{html.escape(p["title"])}</h2>\n'
            f'<p>{html.escape(p["summary"])}</p>\n'
            f'<span class="col-date">{kdate(p["date"])} · 갈창림 대표원장</span>\n'
            f'</a>\n</article>\n')
    return ''.join(out)


def list_regions(posts, key, post_link, cat_link):
    """Regions of the list board for the whole column ('all') or one category page."""
    mine = posts if key == 'all' else [p for p in posts if p['cat_key'] == key]
    chips = []
    for k, n in [('all', '전체')] + used_categories(posts):
        cnt = len(posts) if k == 'all' else sum(p['cat_key'] == k for p in posts)
        cur = ' class="on" aria-current="page"' if k == key else ''
        chips.append(f'<a href="{cat_link(k)}"{cur}>{n}<span class="col-n">{cnt}</span></a>\n')
    name = '원장 칼럼' if key == 'all' else CAT_NAME[key]
    return {
        'lcrumb': '홈 &gt; 원장 칼럼' + ('' if key == 'all' else f' &gt; {name}'),
        'h1': '원장 칼럼' if key == 'all' else f'{name} 칼럼',
        'intro': CAT_INTRO[key],
        'chips': ''.join(chips),
        'list': list_items(mine, post_link),
    }


def others(p, posts, n=3):
    """Other columns to read next: same category first (closest in date, i.e. the neighbours in a series), then the newest."""
    import datetime
    day = lambda q: datetime.date.fromisoformat(q['date'])
    rest = [q for q in posts if q is not p]
    same = sorted((q for q in rest if q['cat_key'] == p['cat_key']), key=lambda q: (abs((day(q) - day(p)).days), q['date']))
    return (same + [q for q in rest if q['cat_key'] != p['cat_key']])[:n]


def regions(p, posts, page_link, post_link, cat_link):
    """HTML for each <!--col:NAME--> region of the post template.
    page_link maps 'traffic.html' to the right href; post_link(post) and cat_link(key) give column hrefs."""
    body = markdown.markdown(p['body_md'], extensions=['tables', 'sane_lists'])
    body = re.sub(r'href="([a-z0-9-]+\.html)(#[\w-]+)?"', lambda m: f'href="{page_link(m.group(1))}{m.group(2) or ""}"', body)
    faq = ''
    if p['faq']:
        items = ''.join(f'<details style="border-bottom: 1px solid #e2dccd">\n{FAQ_SUMMARY}Q. {html.escape(q)}{FAQ_ICON}\n'
                        f'<p style="margin: 0 0 20px; color: #4d554f">{html.escape(a)}</p>\n</details>\n' for q, a in p['faq'])
        faq = ('<div class="faq" style="display: flex; flex-direction: column; gap: 20px">\n'
               '<h2 style="margin: 0; font-size: 24px">자주 묻는 질문</h2>\n'
               f'<div style="border-top: 1px solid #2f5241">\n{items}</div>\n</div>')
    related = ''
    if p['related']:
        links = ''.join(f'<li><a href="{page_link(h.split("#")[0])}{("#" + h.split("#")[1]) if "#" in h else ""}">{html.escape(l)} →</a></li>\n'
                        for h, l in p['related'])
        related = f'<nav class="col-related" aria-label="관련 진료 안내">\n<h2>관련 진료 안내</h2>\n<ul>\n{links}</ul>\n</nav>'
    nxt = ''
    if len(posts) > 1:
        links = ''.join(f'<li><a href="{post_link(q)}"><span class="col-tag">{html.escape(q["category"])}</span>'
                        f'<span class="col-next-t">{html.escape(q["title"])}</span></a></li>\n' for q in others(p, posts))
        nxt = f'<nav class="col-next" aria-label="함께 읽으면 좋은 칼럼">\n<h2>함께 읽으면 좋은 칼럼</h2>\n<ul>\n{links}</ul>\n</nav>'
    local = ''
    if p.get('condition'):
        c = html.escape(p['condition'])
        local = (f'<section class="col-local" aria-label="경산·하양 진료 안내">\n<h2>경산·하양에서 {c} 진료를 찾으신다면</h2>\n'
                 f'<p>갈창림한의원은 경상북도 경산시 하양읍 동서2길 43, 3층에 있습니다. 하양역에서 걸어서 약 10~15분 거리이며, '
                 f'건물 주차장과 이면도로에 주차할 수 있습니다.</p>\n'
                 f'<p>평일 08:30–18:30(점심 13:00–14:00), 토·일요일 08:30–14:00에 진료하며 공휴일은 휴진합니다. '
                 f'{c} 증상이 오래가거나 자주 반복된다면 지금 상태를 확인하고 알맞은 치료를 안내해 드립니다.</p>\n'
                 f'<p><a href="tel:053-851-0122">전화 053-851-0122</a> · <a href="https://talk.naver.com/W4F2TI" target="_blank" rel="noopener">네이버 톡톡 상담</a> · '
                 f'<a href="{page_link("schedule.html")}">진료시간 및 오시는길</a></p>\n</section>')
    return {
        'crumb': f'홈 &gt; 원장 칼럼 &gt; {html.escape(p["category"])}',
        'cat': f'<a class="col-tag" href="{cat_link(p["cat_key"])}">{html.escape(p["category"])}</a>',
        'title': html.escape(p['title']),
        'meta': (f'<time datetime="{p["date"]}">작성 {kdate(p["date"], "")}</time>'
                 + (f' · <time datetime="{p["reviewed"]}">수정 {kdate(p["reviewed"], "")}</time>' if p['reviewed'] > p['date'] else '')
                 + ' · 글·검토 <a href="' + page_link('doctors.html') + '" style="color: #24302a; font-weight: 600; text-decoration: none">갈창림 대표원장</a> (한의사)'),
        'summary': html.escape(p['summary']),
        'body': body,
        'faq': faq,
        'related': related,
        'next': nxt,
        'local': local,
        'reviewed': f'최종 검토 {kdate(p["reviewed"], "")}',
    }


def plain(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment))).strip()


def search_index(posts):
    """Small JSON-able index for the column search box: every word of every post (title, summary, body, FAQ)."""
    out = []
    for p in posts:
        body = markdown.markdown(p['body_md'], extensions=['tables', 'sane_lists'])
        text = ' '.join([plain(body)] + [f'{q} {a}' for q, a in p['faq']])
        out.append({'u': p['file'], 't': p['title'], 'c': p['category'], 'k': p['cat_key'],
                    'd': kdate(p['date']), 's': p['summary'], 'x': re.sub(r'\s+', ' ', text)})
    return out


def fill(template, values):
    def rep(m):
        return values[m.group(1)] if m.group(1) in values else m.group(0)
    return re.sub(r'<!--col:(\w+)-->.*?<!--/col:\1-->', rep, template, flags=re.S)


def mark(values):
    """Same as regions() output, but kept inside markers so a board can be refilled later."""
    return {k: f'<!--col:{k}-->{v}<!--/col:{k}-->' for k, v in values.items()}
