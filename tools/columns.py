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
    'all': '갈창림 대표원장이 진료실에서 자주 받는 질문에 직접 답한 글입니다. 피부미용, 교통사고, 척추·관절 통증, 내과 질환, 다이어트, 소아·여성 건강을 다룹니다.',
    'skin': '피부 고민과 시술에 대해 자주 받는 질문에 갈창림 대표원장이 직접 답한 글입니다. 기미·흑자 같은 색소, 점·검버섯·쥐젖 같은 피부 돌기, 아토피와 원형 탈모, 레이저제모·리프팅·여드름·모공·스킨부스터를 다룹니다.',
    'traffic': '교통사고 후유증과 자동차보험 진료에 대해 갈창림 대표원장이 직접 답한 글입니다. 며칠 지나 나타나는 목·허리 통증과 두통, 어지럼, 잠을 설치는 증상, 치료 시작 시기와 접수 방법을 다룹니다.',
    'pain': '척추·관절·근육 통증에 대해 갈창림 대표원장이 직접 답한 글입니다. 허리·목 디스크, 담 결림, 오십견, 어깨·무릎 통증, 발목 염좌 등을 다룹니다.',
    'internal': '검사에서는 이상이 없다는데 계속 불편한 내과 질환에 대해 갈창림 대표원장이 직접 답한 글입니다. 소화불량, 역류성 식도염, 과민성 대장 증후군, 두통, 안면마비, 손발 저림, 불면증, 화병, 만성 피로, 비염, 수족냉증과 먼저 병원 검사가 필요한 경우를 다룹니다.',
    'diet': '한약 다이어트와 체중 관리에 대해 갈창림 대표원장이 직접 답한 글입니다. 진행 방법과 감량 뒤 요요 없이 유지하는 방법을 다룹니다.',
    'kids-women': '아이 성장과 여성 건강에 대해 갈창림 대표원장이 직접 답한 글입니다. 성장 치료 시작 시기와 성장을 방해하는 습관, 생리통·산후풍·갱년기를 다룹니다.',
}

# More intro paragraphs on category pages (reviewed by the doctor 2026-10-21).
CAT_INTRO_MORE = {
    'traffic': [
        '교통사고 직후에는 긴장한 탓에 아픈 곳을 잘 느끼지 못하다가, 며칠 뒤 목과 허리가 뻐근해지거나 두통·어지럼이 나타나는 경우가 많습니다. 엑스레이에서 이상이 없다는 말을 들었는데도 불편함이 이어진다면, 뭉친 근육과 인대, 틀어진 몸의 균형을 함께 살펴볼 필요가 있습니다.',
        '자동차보험으로 접수하면 보험사 접수번호만으로 한의원 진료를 받을 수 있고, 본인부담금은 발생하지 않습니다. 보험 종류와 보장 범위는 담당 보험사에 확인해 주세요. 정형외과와 같은 날 함께 다니셔도 됩니다. 평일은 오전 8시 30분부터 오후 6시 30분까지, 토·일요일도 오전 8시 30분부터 오후 2시까지 진료합니다. 치료 기간과 회복 정도는 사고의 정도와 몸 상태에 따라 개인차가 있습니다.',
    ],
    'internal': [
        '위내시경이나 혈액 검사에서 큰 이상이 없다는 결과를 받았는데도 소화가 안 되거나, 두통과 피로, 잠을 설치는 증상이 이어지는 분이 많습니다. 이런 증상은 생활 습관과 스트레스, 몸의 순환 상태가 함께 얽혀 있는 경우가 많아, 증상 하나만이 아니라 몸 전체를 함께 살펴봅니다.',
        '진료실에서는 증상이 언제부터, 어떤 상황에서 심해지는지 여쭙고 맥과 혀를 살피는 진찰로 상태를 확인한 뒤 침, 뜸, 한약 등 치료를 정합니다. 갑자기 심해진 통증이나 체중 감소, 마비처럼 먼저 병원 검사가 필요한 경우는 각 글에 따로 정리해 두었습니다. 회복 정도는 개인차가 있습니다.',
    ],
    'kids-women': [
        '아이 성장은 키만이 아니라 잠, 식사, 잦은 감기와 비염 같은 몸 상태와 함께 살펴봐야 합니다. 성장 치료를 언제 시작하면 좋을지, 성장판 검사가 필요한 경우는 언제인지, 집에서 챙길 수 있는 생활 습관을 정리했습니다.',
        "여성 건강은 생리통, 출산 후 산후풍, 갱년기처럼 시기마다 고민이 달라집니다. 진통제로 버티거나 '원래 그렇다'며 참기보다, 지금 몸 상태를 확인하고 시기에 맞게 관리하는 방법을 안내합니다. 치료 방법과 기간은 개인의 상태에 따라 다르며 개인차가 있습니다.",
    ],
}
P_INTRO = '<p style="margin: 0; max-width: 720px; font-size: 17px; color: #4d554f">'

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
        refs = []      # 참고 자료 (원장 검토를 거친 공공기관·학회 자료): 'name | url ; name | url'
        for part in filter(None, (p.strip() for p in meta.get('refs', '').split(' ; '))):
            name, url = (x.strip() for x in part.split('|', 1))
            refs.append((name, url))
        meta.update(body_md=body.strip(), faq=faq, related=related, refs=refs, cat_key=CAT_KEY[meta['category']],
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
        # the template wraps the intro in one <p>; extra paragraphs close it and open the next with the same style
        'intro': CAT_INTRO[key] + ''.join(f'</p>\n{P_INTRO}{html.escape(t)}' for t in CAT_INTRO_MORE.get(key, [])),
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
        rt = '관련 진료·칼럼 안내' if any(h.startswith('column-') for h, _ in p['related']) else '관련 진료 안내'
        related = f'<nav class="col-related" aria-label="{rt}">\n<h2>{rt}</h2>\n<ul>\n{links}</ul>\n</nav>'
    nxt = ''
    if len(posts) > 1:
        links = ''.join(f'<li><a href="{post_link(q)}"><span class="col-tag">{html.escape(q["category"])}</span>'
                        f'<span class="col-next-t">{html.escape(q["title"])}</span></a></li>\n' for q in others(p, posts))
        nxt = f'<nav class="col-next" aria-label="함께 읽으면 좋은 칼럼">\n<h2>함께 읽으면 좋은 칼럼</h2>\n<ul>\n{links}</ul>\n</nav>'
    local = ''
    if p.get('condition'):
        c = html.escape(p['condition'])
        local = (f'<section class="col-local" aria-label="경산·하양 진료 안내">\n<h2>경산·하양에서 {c} 진료를 찾으신다면</h2>\n'
                 f'<p>갈창림 한의원은 경상북도 경산시 하양읍 동서2길 43, 3층에 있습니다. 하양역에서 걸어서 약 10~15분 거리이며, '
                 f'건물 주차장과 이면도로에 주차할 수 있습니다.</p>\n'
                 f'<p>평일 08:30–18:30(점심 13:00–14:00), 토·일요일 08:30–14:00에 진료하며 공휴일은 휴진합니다. '
                 f'{c} 증상이 오래가거나 자주 반복된다면 지금 상태를 확인하고 알맞은 치료를 안내해 드립니다.</p>\n'
                 f'<p><a href="tel:053-851-0122">전화 053-851-0122</a> · <a href="https://talk.naver.com/W4F2TI" target="_blank" rel="noopener">네이버 톡톡 상담</a> · '
                 f'<a href="{page_link("schedule.html")}">진료시간 및 오시는길</a></p>\n<p>톡톡 상담은 진료시간 중 최대한 빠르게 답해 드립니다.</p>\n</section>')
    if p.get('refs'):
        items = ''.join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(n)}</a></li>\n' for n, u in p['refs'])
        body += f'\n<h2>참고 자료</h2>\n<ul class="col-refs">\n{items}</ul>'
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


def home_latest(posts, link, n=3):
    """Cards for the newest n columns on the home page (<!--col:homelatest--> region)."""
    newest = sorted(posts, key=lambda q: (q['date'], q['file']), reverse=True)[:n]
    out = []
    for p in newest:
        out.append(
            f'<a href="{link(p)}" class="svc" style="flex: 1 0 280px; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; '
            f'padding: 26px 24px; border-radius: 22px; background: #ffffff; border: 1px solid #e2dccd; text-decoration: none; color: #24302a">\n'
            f'<span style="align-self: flex-start; padding: 3px 10px; border-radius: 999px; background: #ede9dd; color: #2f5241; font-size: 13px; font-weight: 700">{html.escape(p["category"])}</span>\n'
            f'<strong style="font-size: 18px; line-height: 1.5; font-weight: 700; word-break: keep-all">{html.escape(p["title"])}</strong>\n'
            f'<span style="margin-top: auto; font-size: 14px; color: #5d655f">{kdate(p["date"])} · 갈창림 대표원장</span>\n'
            f'</a>\n')
    return ''.join(out)
