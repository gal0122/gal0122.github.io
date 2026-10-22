"""Explanatory pictures for 원장 칼럼 (original drawings, no patient photos).

Each spec makes one SVG in galch/columns/img-src; tools/render_svg.js turns them into WebP in galch/columns/img,
and add_figures() puts a <figure> into the column markdown before the given heading.
All text comes from the column itself."""
import os, re, html

W, H = 1200, 720
INK, SUB, GREEN, GOLD, LINE, CREAM, CARD = '#24302a', '#4d554f', '#2f5241', '#7a6b42', '#e2dccd', '#faf7f0', '#ffffff'
WARN = '#a8452f'
EPI, DER, FAT = '#f1e2cf', '#ecd3c3', '#f6ead9'


def esc(t):
    return html.escape(t, quote=False)


def tw(t, fs):
    """rough text width for Korean + latin."""
    w = 0
    for ch in t:
        w += fs * (0.98 if ord(ch) > 0x2E80 else 0.56 if ch != ' ' else 0.3)
    return w


def wrap(t, fs, maxw):
    words, lines, cur = t.split(' '), [], ''
    for w_ in words:
        cand = (cur + ' ' + w_).strip()
        if tw(cand, fs) <= maxw or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(x, y, t, fs=22, fill=SUB, weight=400, anchor='start', maxw=None, lh=1.45):
    lines = wrap(t, fs, maxw) if maxw else [t]
    out = ''
    for i, ln in enumerate(lines):
        out += (f'<text x="{x}" y="{y + i * fs * lh:.0f}" font-size="{fs}" font-weight="{weight}" fill="{fill}" '
                f'text-anchor="{anchor}">{esc(ln)}</text>')
    return out, y + len(lines) * fs * lh


def frame(title, subtitle, inner):
    t, _ = text(60, 78, title, 38, INK, 800)
    s, _ = text(60, 122, subtitle, 22, '#5d655f', 400, maxw=1080)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Pretendard, sans-serif">'
            f'<rect width="{W}" height="{H}" fill="{CREAM}"/>{t}{s}{inner}'
            '<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" fill="#b9ab86"/></marker></defs></svg>')


def card(x, y, w, h, head, body, num=None, accent=GREEN, fill=CARD):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="{LINE}" stroke-width="2"/>'
    hx = x + 28
    if num is not None:
        out += f'<circle cx="{x + 46}" cy="{y + 50}" r="20" fill="{accent}"/>'
        out += f'<text x="{x + 46}" y="{y + 58}" font-size="22" font-weight="800" fill="#fff" text-anchor="middle">{num}</text>'
        hx = x + 80
    t, yy = text(hx, y + 58, head, 25, accent, 800, maxw=w - (hx - x) - 20)
    out += t
    yy = max(yy, y + 100) + 6
    for b in body:
        t, yy = text(x + 28, yy, b, 20, SUB, 400, maxw=w - 56, lh=1.5)
        out += t
        yy += 6
    return out


def cards(items, y=170, h=300, gap=24, accent=GREEN, numbered=True):
    n = len(items)
    w = (W - 120 - gap * (n - 1)) / n
    out = ''
    for i, (head, body) in enumerate(items):
        x = 60 + i * (w + gap)
        out += card(x, y, w, h, head, body, (i + 1) if numbered else None, accent)
    return out


def flow(items, y=200, h=300, note=None, accent=GREEN):
    n = len(items)
    gap = 56
    w = (W - 120 - gap * (n - 1)) / n
    out = ''
    for i, (head, body) in enumerate(items):
        x = 60 + i * (w + gap)
        out += card(x, y, w, h, head, body, i + 1, accent)
        if i < n - 1:
            out += f'<path d="M{x + w + 10} {y + h / 2} h{gap - 20}" stroke="#b9ab86" stroke-width="4" marker-end="url(#ar)"/>'
    if note:
        out += callout(60, y + h + 36, note)
    return out


def callout(x, y, t, color=WARN, w=W - 120):
    lines = wrap(t, 21, w - 64)
    h = 30 + len(lines) * 31
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fbf0ec" stroke="{color}" stroke-width="2"/>'
    out += f'<text x="{x + 24}" y="{y + 40}" font-size="22" font-weight="800" fill="{color}">!</text>'
    t_, _ = text(x + 48, y + 40, t, 21, color, 600, maxw=w - 72, lh=1.45)
    return out + t_


def compare(left, right, y=170, h=420, note=None):
    out = ''
    w = (W - 120 - 32) / 2
    for i, (head, sub, body, accent) in enumerate([left, right]):
        x = 60 + i * (w + 32)
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
        out += f'<rect x="{x}" y="{y}" width="{w}" height="12" rx="6" fill="{accent}"/>'
        t, yy = text(x + 32, y + 66, head, 30, accent, 800, maxw=w - 64)
        out += t
        if sub:
            t, yy = text(x + 32, yy + 2, sub, 20, GOLD, 700, maxw=w - 64)
            out += t
        yy += 14
        for b in body:
            out += f'<circle cx="{x + 40}" cy="{yy - 7}" r="5" fill="{accent}"/>'
            t, yy = text(x + 58, yy, b, 21, SUB, 400, maxw=w - 96, lh=1.5)
            out += t
            yy += 10
    if note:
        out += callout(60, y + h + 26, note)
    return out


def timeline(points, y=330, note=None, hl=None):
    n = len(points)
    x0, x1 = 210, W - 210
    out = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#b9ab86" stroke-width="6" stroke-linecap="round"/>'
    for i, (head, body) in enumerate(points):
        x = x0 + (x1 - x0) * i / (n - 1)
        on = hl is not None and i == hl
        out += f'<circle cx="{x}" cy="{y}" r="{22 if on else 16}" fill="{GREEN if on else "#d7c9a7"}" stroke="#fff" stroke-width="4"/>'
        t, yy = text(x, y - 46, head, 25, GREEN if on else INK, 800, 'middle')
        out += t
        bw = (x1 - x0) / (n - 1) - 20 if n > 1 else 400
        yy = y + 58
        for b in body:
            t, yy = text(x, yy, b, 20, SUB, 400, 'middle', maxw=min(bw, 300), lh=1.5)
            out += t
    if note:
        out += callout(60, y + 220, note)
    return out


def skin(lesion, notes, x=60, y=170, w=640, h=470):
    """Skin cross-section on the left, notes on the right."""
    ep, de = 90, 230
    out = (f'<rect x="{x}" y="{y + 40}" width="{w}" height="{ep}" fill="{EPI}"/>'
           f'<rect x="{x}" y="{y + 40 + ep}" width="{w}" height="{de}" fill="{DER}"/>'
           f'<rect x="{x}" y="{y + 40 + ep + de}" width="{w}" height="{h - 40 - ep - de}" fill="{FAT}"/>'
           f'<line x1="{x}" y1="{y + 40 + ep}" x2="{x + w}" y2="{y + 40 + ep}" stroke="#c9a98f" stroke-width="3" stroke-dasharray="10 8"/>')
    for lab, yy in [('표피', y + 40 + 34), ('진피', y + 40 + ep + 40), ('피하지방', y + 40 + ep + de + 40)]:
        out += f'<text x="{x + w - 16}" y="{yy}" font-size="19" font-weight="700" fill="{GOLD}" text-anchor="end">{lab}</text>'
    cx, top = x + w * 0.42, y + 40
    out += LESIONS[lesion](cx, top, ep, de)
    nx = x + w + 48
    yy = y + 40
    for head, body in notes:
        t, yy = text(nx, yy + 10, head, 24, GREEN, 800, maxw=W - 60 - nx)
        out += t
        t, yy = text(nx, yy, body, 20, SUB, 400, maxw=W - 60 - nx, lh=1.5)
        out += t
        yy += 18
    return out


def _bump(cx, top, w, hgt, fill):
    return f'<path d="M{cx - w / 2} {top} q{w / 2} {-hgt * 2} {w} 0z" fill="{fill}"/>'


LESIONS = {
    'flat_epi': lambda cx, top, ep, de: f'<ellipse cx="{cx}" cy="{top + 34}" rx="120" ry="26" fill="#8a5a3c"/>',
    'dermal_dots': lambda cx, top, ep, de: ''.join(f'<circle cx="{cx + dx}" cy="{top + ep + dy}" r="{r}" fill="#6f7b8c"/>'
                                                   for dx, dy, r in [(-60, 70, 16), (0, 120, 14), (50, 80, 12), (-20, 170, 12), (80, 150, 10)]),
    'seb_k': lambda cx, top, ep, de: (_bump(cx, top + 2, 230, 40, '#6b4a33')
                                      + f'<path d="M{cx - 115} {top} h230 v{ep * 0.55} h-230z" fill="#7d573d"/>'),
    'mole_flat': lambda cx, top, ep, de: (f'<ellipse cx="{cx}" cy="{top + ep - 6}" rx="80" ry="22" fill="#4a3428"/>'
                                          + f'<ellipse cx="{cx}" cy="{top + ep + 30}" rx="60" ry="28" fill="#4a3428" opacity="0.75"/>'),
    'skin_tag': lambda cx, top, ep, de: (f'<path d="M{cx - 12} {top + 2} q-6 -22 -30 -34 q18 -26 54 -8 q8 22 -4 42z" fill="#d9b49a" stroke="#b98d70" stroke-width="3"/>'),
    'milia': lambda cx, top, ep, de: (f'<circle cx="{cx}" cy="{top + ep + 18}" r="22" fill="#ffffff" stroke="#cdbfa8" stroke-width="3"/>'
                                      + f'<path d="M{cx - 30} {top} q30 -16 60 0" fill="{EPI}"/>'),
    'seb_hyper': lambda cx, top, ep, de: (_bump(cx, top + 2, 160, 22, '#e9cf8c')
                                          + ''.join(f'<ellipse cx="{cx + dx}" cy="{top + ep + 50 + dy}" rx="30" ry="24" fill="#e2c26e" stroke="#c9a54a" stroke-width="2"/>'
                                                    for dx, dy in [(-50, 0), (50, 0), (-30, 50), (30, 50), (0, 20)])
                                          + f'<path d="M{cx} {top - 18} v{ep + 70}" stroke="#7a6b42" stroke-width="5"/>'),
    'cyst': lambda cx, top, ep, de: (f'<circle cx="{cx}" cy="{top + ep + 100}" r="90" fill="#fffaf0" stroke="#b9ab86" stroke-width="5"/>'
                                     + f'<path d="M{cx} {top - 4} v{ep + 14}" stroke="#3b3b3b" stroke-width="8"/>'
                                     + f'<circle cx="{cx}" cy="{top}" r="7" fill="#3b3b3b"/>'
                                     + f'<text x="{cx}" y="{top + ep + 108}" font-size="20" font-weight="700" fill="{GOLD}" text-anchor="middle">각질 주머니</text>'),
    'cherry': lambda cx, top, ep, de: (_bump(cx, top + 2, 120, 36, '#d1344b')
                                       + ''.join(f'<circle cx="{cx + dx}" cy="{top + ep + 20 + dy}" r="{r}" fill="#d1344b" opacity="0.8"/>'
                                                 for dx, dy, r in [(-30, 0, 16), (10, 10, 18), (40, -6, 12), (-8, 40, 12)])),
}


def top_view(kind, notes):
    """Skin seen from above (for spider angioma, porokeratosis, alopecia)."""
    x, y, w, h = 60, 170, 640, 470
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{EPI}"/>'
    cx, cy = x + w / 2, y + h / 2
    if kind == 'spider':
        import math
        for i in range(9):
            a = i * 2 * math.pi / 9 + 0.3
            x2, y2 = cx + 170 * math.cos(a), cy + 150 * math.sin(a)
            mx, my = cx + 90 * math.cos(a + 0.25), cy + 80 * math.sin(a + 0.25)
            out += f'<path d="M{cx} {cy} Q{mx} {my} {x2} {y2}" stroke="#d1344b" stroke-width="5" fill="none" stroke-linecap="round"/>'
        out += f'<circle cx="{cx}" cy="{cy}" r="20" fill="#c22a42"/>'
        out += f'<text x="{cx}" y="{cy + 220}" font-size="20" font-weight="700" fill="{GOLD}" text-anchor="middle">가운데 붉은 점 · 거미 다리처럼 뻗은 혈관</text>'
    elif kind == 'poro':
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="190" ry="140" fill="#e6c9ad"/>'
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="190" ry="140" fill="none" stroke="#8a5a3c" stroke-width="9"/>'
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="182" ry="132" fill="none" stroke="#f3e2cc" stroke-width="3"/>'
        out += f'<text x="{cx}" y="{cy + 200}" font-size="20" font-weight="700" fill="{GOLD}" text-anchor="middle">테두리가 실처럼 가늘게 솟은 고리 모양</text>'
    elif kind == 'alopecia':
        import random
        rnd = random.Random(3)
        for _ in range(520):
            px, py = x + 20 + rnd.random() * (w - 40), y + 20 + rnd.random() * (h - 40)
            if (px - cx) ** 2 / 150 ** 2 + (py - cy) ** 2 / 120 ** 2 < 1:
                continue
            out += f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{px + 4:.0f}" y2="{py - 16:.0f}" stroke="#3a2f2a" stroke-width="3" stroke-linecap="round"/>'
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="140" ry="110" fill="#f3dcc8" stroke="#d9b49a" stroke-width="2"/>'
        out += f'<text x="{cx}" y="{cy + 8}" font-size="22" font-weight="800" fill="{GOLD}" text-anchor="middle">동전 모양으로 빠진 자리</text>'
    nx, yy = x + w + 48, y + 30
    for head, body in notes:
        t, yy = text(nx, yy + 10, head, 24, GREEN, 800, maxw=W - 60 - nx)
        out += t
        t, yy = text(nx, yy, body, 20, SUB, 400, maxw=W - 60 - nx, lh=1.5)
        out += t
        yy += 18
    return out


def spine(bone, symptom):
    """normal vs herniated disc (neck version)."""
    out = ''
    for i, (lab, herniated) in enumerate([('정상 디스크', False), ('수핵이 밀려 나와 신경을 누름', True)]):
        gx = 140 + i * 540
        out += (f'<g transform="translate({gx},180)">'
                f'<rect x="0" y="0" width="360" height="110" rx="22" fill="#e8dfcf" stroke="#b9ab86" stroke-width="3"/>'
                f'<text x="180" y="64" font-size="24" font-weight="700" fill="#5d655f" text-anchor="middle">{bone}</text>'
                f'<rect x="18" y="122" width="324" height="62" rx="28" fill="#cfe0d4" stroke="{GREEN}" stroke-width="3"/>')
        if herniated:
            out += (f'<path d="M140 138 q110 -8 190 14 q36 4 46 0 q-10 18 -46 18 q-76 22 -190 0z" fill="{GREEN}"/>'
                    f'<path d="M408 30 q-18 120 0 280" stroke="#c9822f" stroke-width="10" fill="none" stroke-linecap="round"/>'
                    f'<text x="428" y="50" font-size="22" font-weight="700" fill="#c9822f">신경</text>'
                    f'<circle cx="398" cy="153" r="28" fill="none" stroke="#c0392b" stroke-width="4" stroke-dasharray="6 5"/>')
        else:
            out += f'<ellipse cx="180" cy="153" rx="64" ry="18" fill="{GREEN}"/><text x="180" y="160" font-size="19" font-weight="700" fill="#fff" text-anchor="middle">수핵</text>'
        out += (f'<rect x="0" y="196" width="360" height="110" rx="22" fill="#e8dfcf" stroke="#b9ab86" stroke-width="3"/>'
                f'<text x="180" y="260" font-size="24" font-weight="700" fill="#5d655f" text-anchor="middle">{bone}</text>'
                f'<text x="180" y="360" font-size="26" font-weight="800" fill="{INK if herniated else GREEN}" text-anchor="middle">{lab}</text></g>')
    out += callout(60, 580, symptom, GREEN)
    return out


def head_icon(cx, cy, kind):
    out = (f'<ellipse cx="{cx}" cy="{cy}" rx="90" ry="110" fill="#f0dcc7" stroke="#c9a98f" stroke-width="3"/>'
           f'<rect x="{cx - 40}" y="{cy + 100}" width="80" height="60" fill="#f0dcc7" stroke="#c9a98f" stroke-width="3"/>')
    if kind == 'band':
        out += f'<path d="M{cx - 96} {cy - 30} q96 -40 192 0" stroke="{WARN}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    else:
        out += ''.join(f'<path d="M{cx - 60 - r} {cy - 60} a{20 + r} {20 + r} 0 0 1 0 {40 + 2 * r}" stroke="{WARN}" stroke-width="5" fill="none" opacity="{1 - r / 40}"/>' for r in (0, 14, 28))
    return out


def svg(spec):
    return frame(spec['title'], spec['sub'], spec['body'])


# ---------------- column specs ----------------
def specs():
    S = []
    def add(md, before, name, alt, cap, title, sub, body):
        S.append(dict(md=md, before=before, name=name, alt=alt, cap=cap, title=title, sub=sub, body=body))

    add('2026-10-14-kids-growth-when-to-start.md', '## 초등학생 때 시작하기를 권하는 이유', 'growth-timing',
        '아이 키 성장 시기 그림: 초등학생 때 관리를 시작하고, 2차 성징 뒤 성장판이 닫히기까지의 흐름', '성장판이 닫히기 전, 2차 성징이 나타나기 전에 성장 상태를 확인하는 것이 좋습니다.',
        '키가 자랄 수 있는 시기', '사춘기가 시작되면 성장판이 닫히기까지 남은 시간이 짧아집니다.',
        timeline([('초등학생', ['2차 성징 전', '성장 상태 확인·관리 시작']), ('2차 성징', ['사춘기가 시작되면', '남은 시간이 짧아짐']), ('성장판 닫힘', ['이후에는 키가', '더 자라기 어려움'])], hl=0,
                 note='한의원의 성장 관리는 키를 직접 늘리는 것이 아니라 소화·수면·잦은 감기처럼 성장을 방해하는 요인을 살피는 것입니다.'))

    add('2026-10-14-traffic-delayed-pain.md', '## 검사에서 이상이 없다는데 왜 아플까요?', 'traffic-delayed',
        '교통사고 후 통증이 나타나는 시점 그림: 사고 직후에는 잘 느끼지 못하다가 며칠 뒤 목·허리 통증과 두통이 나타남', '사고 직후에는 긴장 때문에 통증을 잘 느끼지 못하는 경우가 많습니다.',
        '교통사고 통증은 며칠 뒤에 나타나기도 합니다', '통증이 시작되었다면 미루지 말고 진료를 받아 보시는 것이 좋습니다.',
        timeline([('사고 직후', ['놀라고 긴장해', '통증을 잘 못 느낌']), ('며칠 뒤', ['목·허리가 뻐근함', '두통·어지럼']), ('바로 진료', ['통증이 시작되면', '미루지 말고 진료'])], hl=2,
                 note='의식을 잃었거나 팔다리에 힘이 빠지면 먼저 큰 병원에서 확인하세요.'))

    add('2026-10-14b-sylfirm-x-guide.md', '## 고민별로 먼저 확인하는 것', 'sylfirm-cw-pw',
        '실펌X CW와 PW 비교 그림: CW는 고주파를 이어서, PW는 짧게 끊어서 보냄', '한 번의 시술에서 두 방식을 함께 쓰기도 합니다.',
        '실펌X, 열을 주는 두 가지 리듬', '바늘 깊이와 세기는 피부 두께, 피지 양, 예민한 정도에 따라 사람마다 다르게 정합니다.',
        compare(('CW · 연속파', '고주파를 끊지 않고 이어서', ['진피에 충분한 열 자극', '모공, 거친 피부결', '여드름 흉터, 탄력'], GREEN),
                ('PW · 펄스파', '고주파를 아주 짧게 끊어서', ['열이 한꺼번에 쌓이지 않게', '붉은 자국, 홍조처럼', '예민하게 다뤄야 하는 피부'], '#8a6d3b')))

    add('2026-10-15b-low-back-pain.md', '## 이런 경우는 디스크나 다른 원인을 먼저 확인합니다', 'low-back-first-days',
        '허리를 삐끗했을 때 처음 며칠 지내는 법 그림', '오래 누워 있기보다 아프지 않은 범위에서 조금씩 움직이는 것이 회복에 도움이 됩니다.',
        '허리를 삐끗했을 때, 처음 며칠', '허리 주변 근육과 인대가 갑자기 늘어나 생기는 통증입니다.',
        cards([('무리하지 않기', ['처음 하루이틀은', '허리를 숙여 물건을', '드는 동작을 피함']),
               ('조금씩 움직이기', ['오래 누워 있기보다', '아프지 않은 범위에서', '조금씩 움직임']),
               ('다른 원인 확인', ['다리 저림이나 힘 빠짐이', '함께 있으면 디스크 등', '다른 원인을 먼저 확인'])]))

    add('2026-10-16-lentigo.md', '## 흑자 치료는 이렇게 합니다', 'lentigo-depth',
        '흑자 피부 단면 그림: 표피에 경계가 또렷한 갈색 색소', '흑자는 표피에 있는 색소로, 진하기와 깊이에 맞춰 파장을 고릅니다.',
        '흑자는 표피에 있는 색소입니다', '햇빛을 많이 받은 얼굴과 손등에 경계가 또렷한 갈색 반점으로 생깁니다.',
        skin('flat_epi', [('경계가 또렷함', '주변 피부와 선이 분명한 갈색 반점'), ('겨울에도 그대로', '주근깨와 달리 계절에 따라 옅어지지 않음'), ('파장 선택', '532nm·755nm·1064nm 가운데 진하기와 깊이에 맞춰 고름')]))

    add('2026-10-17-abnom.md', '## ABNOM 치료는 이렇게 합니다', 'abnom-depth',
        'ABNOM 피부 단면 그림: 진피에 흩어진 회갈색 색소', 'ABNOM은 진피에 있는 색소라 기미 관리만으로는 잘 옅어지지 않습니다.',
        'ABNOM은 진피에 있는 색소입니다', '광대 양쪽에 회갈색·푸르스름한 작은 반점이 모여 생깁니다.',
        skin('dermal_dots', [('깊은 색소', '표피 아래 진피에 있어 회갈색으로 보임'), ('기미와 헷갈림', '비슷해 보이지만 색소 위치가 더 깊음'), ('긴 파장으로 여러 번', '깊이 닿는 1064nm로 간격을 두고 여러 번')]))

    add('2026-10-17-indigestion.md', '## 왜 생길까요?', 'indigestion-symptoms',
        '기능성 소화불량의 세 가지 증상 그림: 식후 더부룩함, 조기 포만감, 명치 통증', '검사에서 뚜렷한 이상이 없는데도 이런 증상이 반복되는 상태입니다.',
        '기능성 소화불량, 이런 증상이 반복됩니다', '위가 음식을 받아들이고 내려보내는 움직임이 둔해지고 예민해진 것과 관련이 있습니다.',
        cards([('식후 더부룩함', ['먹고 나면 오래', '배가 더부룩함']), ('조금만 먹어도 배부름', ['몇 숟가락만 먹어도', '배가 찬 느낌']), ('명치 통증', ['명치가 아프거나', '쓰린 느낌'])], h=300)
        + callout(60, 500, '40세 이후 새로 생긴 소화불량, 이유 없는 체중 감소, 검은 변, 삼키기 어려움이 있으면 내시경을 먼저 받으세요.'))

    add('2026-10-18-freckles.md', '## 주근깨 치료는 이렇게 합니다', 'freckles-season',
        '주근깨가 계절에 따라 달라지는 모습 비교 그림: 여름에 진해지고 겨울에 옅어짐', '체질에 자외선이 더해져 여름에 진해집니다.',
        '주근깨는 계절 따라 진하기가 달라집니다', '색소가 얕은 표피에 있어 532nm·755nm 레이저로 비교적 잘 옅어집니다.',
        compare(('여름', '자외선이 강할 때', ['색이 진해지고', '개수가 늘어 보임'], '#a0602f'),
                ('겨울', '자외선이 약할 때', ['색이 옅어짐', '치료 후 관리가 수월한 시기'], GREEN),
                h=330, note='체질적으로 생기는 색소라 햇빛을 받으면 다시 생길 수 있어 자외선 차단이 중요합니다.'))

    add('2026-10-18-neck-disc.md', '## 이런 증상이 나타납니다', 'neck-disc',
        '목디스크 그림: 정상 디스크와, 목뼈 사이 수핵이 밀려 나와 신경을 누르는 모습 비교', '목뼈 사이 디스크가 밀려 나와 신경을 누르면 목·어깨 통증과 팔·손 저림이 생길 수 있습니다.',
        '목디스크는 이렇게 생깁니다', '고개를 오래 숙이는 자세와 일자목·거북목이 큰 원인입니다.',
        spine('목뼈', '목과 어깨 통증, 팔과 손의 저림이 생길 수 있습니다. 손에 힘이 빠지거나 걸음이 불편해지면 먼저 검사가 필요합니다.'))

    add('2026-10-19-frozen-shoulder.md', '## 회전근개 손상과는 어떻게 다를까요?', 'frozen-shoulder-stages',
        '오십견의 세 단계 그림: 아픈 시기, 굳는 시기, 풀리는 시기', '오십견은 세 시기를 거치며 오래가는 경우가 많습니다.',
        '오십견은 세 단계를 거칩니다', '어깨 관절을 감싼 주머니에 염증이 생기고 굳어, 팔을 올리거나 뒤로 돌리기 어려워집니다.',
        timeline([('① 아픈 시기', ['통증이 심하고', '밤에 더 아픔']), ('② 굳는 시기', ['통증은 줄지만', '어깨가 굳어 움직임 제한']), ('③ 풀리는 시기', ['굳은 어깨가', '조금씩 풀림'])],
                 note='통증을 줄이면서 굳은 어깨의 움직임을 되찾는 것이 치료의 목표입니다.'))

    add('2026-10-19-moles.md', '## 이런 점은 바로 빼지 않고 먼저 확인합니다', 'mole-types',
        '점의 모양에 따른 제거 방법 비교 그림: 평평한 점은 아이스 점빼기, 솟거나 깊은 점은 유펄스 CO2', '평평한 점과 솟은 점은 뿌리의 깊이가 달라 제거 방법도 다릅니다.',
        '점의 모양에 따라 제거 방법이 다릅니다', '점은 색소 세포가 모여 생긴 양성 병변입니다.',
        compare(('평평한 점', '색이 짙고 납작함', ['피부를 깎지 않는', '아이스 점빼기'], '#4a3428'),
                ('솟은 점 · 깊은 점', '튀어나오거나 뿌리가 깊음', ['유펄스 CO2로', '필요한 깊이만큼 제거'], GREEN),
                h=320, note='모양이 비대칭이거나, 경계가 번지거나, 여러 색이 섞이거나, 6mm보다 크거나, 짧은 기간에 변한 점은 바로 빼지 않고 먼저 확인합니다.'))

    add('2026-10-20-headache.md', '## 왜 반복될까요?', 'headache-types',
        '긴장성 두통과 편두통 비교 그림', '자주 반복되는 두통의 대부분은 긴장성 두통과 편두통입니다.',
        '자주 오는 두통, 대부분은 두 가지입니다', '어떤 두통인지에 따라 관리 방법이 달라집니다.',
        head_icon(220, 300, 'band') + head_icon(820, 300, 'side')
        + text(220, 500, '긴장성 두통', 28, GREEN, 800, 'middle')[0] + text(220, 540, '머리를 조이듯 아픔', 21, SUB, 400, 'middle')[0]
        + text(220, 574, '목·어깨 긴장, 자세, 스트레스', 21, SUB, 400, 'middle')[0]
        + text(820, 500, '편두통', 28, WARN, 800, 'middle')[0] + text(820, 540, '한쪽이 욱신거림', 21, SUB, 400, 'middle')[0]
        + text(820, 574, '빛·소리에 예민, 메스꺼움', 21, SUB, 400, 'middle')[0]
        + callout(60, 616, '평생 처음 겪는 극심한 두통, 팔다리 마비·말 어눌함·얼굴 처짐이 함께 있으면 바로 응급실로 가세요.'))

    add('2026-10-20-seborrheic-keratosis.md', '## 흑자와는 어떻게 다를까요?', 'seb-keratosis',
        '검버섯(지루각화증) 피부 단면 그림: 표피가 두꺼워져 살짝 솟은 갈색 돌기', '검버섯은 피부에 붙여 놓은 듯 살짝 솟은 양성 돌기입니다.',
        '검버섯(지루각화증)은 이런 모양입니다', '나이가 들며 얼굴·목·몸에 갈색~검은색으로 생깁니다.',
        skin('seb_k', [('살짝 솟은 돌기', '피부에 붙여 놓은 듯 표피가 두꺼워짐'), ('피부암이 아님', '옮지도 않지만 저절로 없어지지 않음'), ('필요한 깊이만큼', '보기 싫거나 걸리면 레이저로 제거')]))

    add('2026-10-20c-traffic-insurance.md', '## 첫 방문 때 챙겨 주세요', 'traffic-insurance-flow',
        '교통사고 자동차보험 진료 순서 그림: 보험사 접수, 접수번호 받기, 내원, 자동차보험 진료', '접수한 보험 종류와 보장 범위는 담당 보험사에 확인해 주세요.',
        '자동차보험 진료, 이렇게 진행됩니다', '보험사에서 받은 접수번호만 있으면 자동차보험으로 진료받을 수 있습니다.',
        flow([('사고 접수', ['보험사에', '사고를 접수']), ('접수번호', ['보험사에서', '접수번호 받기']), ('내원', ['접수번호와', '신분증 챙기기']), ('진료', ['자동차보험으로', '진료 시작'])], h=280,
             note='상대방이 접수를 해 주지 않으면 내 차 보험의 자동차상해·자기신체사고·무보험차상해로 접수할 수 있는지 보험사에 확인하세요.'))

    add('2026-10-20d-traffic-ortho-and-km.md', '## 이렇게 함께 다니시면 좋습니다', 'ortho-and-km',
        '교통사고 후 정형외과와 한의원 역할 비교 그림', '두 곳은 살피는 부분과 치료 방법이 달라 함께 다니셔도 됩니다.',
        '정형외과와 한의원, 함께 다니셔도 됩니다', '같은 사고라면 같은 접수번호로 두 곳 모두 진료받을 수 있습니다.',
        compare(('정형외과', '영상 검사로 확인', ['엑스레이·CT·MRI', '뼈·관절·디스크·신경', '약물·주사·물리치료'], '#4f6a85'),
                ('한의원', '진찰로 확인', ['뭉친 근육, 틀어진 균형', '침·약침·추나·한약', '뜸·부항·물리치료요법'], GREEN),
                h=330, note='다른 곳에서 받는 치료와 복용 중인 약, 검사 결과지를 알려 주시면 진료에 도움이 됩니다.'))

    add('2026-10-21-skin-tags.md', '## 쥐젖 제거는 이렇게 합니다', 'skin-tag',
        '쥐젖(연성 섬유종) 그림: 피부에서 말랑하게 솟아 나온 작은 살 돌기', '쥐젖은 피부가 자주 접히고 쓸리는 곳에 생기는 말랑한 살 돌기입니다.',
        '쥐젖은 이런 모양입니다', '피부암이 아니고 옮지도 않지만 저절로 없어지지 않습니다.',
        skin('skin_tag', [('잘 생기는 곳', '목, 겨드랑이, 눈가처럼 접히고 쓸리는 곳'), ('영향을 주는 것', '마찰, 체중 증가, 나이, 임신'), ('제거', '걸리거나 보기 싫다면 유펄스 CO2로 제거')]))

    add('2026-10-22-milia.md', '## 비립종 제거는 이렇게 합니다', 'milia',
        '비립종 피부 단면 그림: 표피 바로 아래 입구 없이 갇힌 하얀 각질 주머니', '여드름처럼 입구가 열려 있지 않아 손으로 짜면 잘 나오지 않습니다.',
        '비립종은 입구가 없는 작은 주머니입니다', '피부 속에 각질이 갇혀 생긴 1~2mm 크기의 하얗고 단단한 좁쌀입니다.',
        skin('milia', [('입구가 없음', '짜면 잘 나오지 않고 상처·자국만 남기 쉬움'), ('잘 생기는 곳', '눈가와 볼'), ('제거', '아주 작은 통로를 낸 뒤 내용물을 빼냄')]))

    add('2026-10-22-rhinitis.md', '## 감기, 축농증과는 어떻게 다를까요?', 'rhinitis-flow',
        '비염이 생기는 흐름 그림: 알레르기 원인과 찬 공기가 예민한 코 점막을 자극해 재채기, 콧물, 코막힘이 생김', '코 점막이 예민해져 증상이 반복되는 질환입니다.',
        '비염은 이렇게 반복됩니다', '집먼지진드기·꽃가루 같은 알레르기 원인이나 찬 공기·온도 변화가 증상을 일으킵니다.',
        flow([('원인', ['집먼지진드기·꽃가루', '찬 공기·온도 변화']), ('예민한 코 점막', ['작은 자극에도', '쉽게 반응']), ('증상', ['재채기, 맑은 콧물', '코막힘, 코 가려움'])], h=280,
             note='누런 콧물과 얼굴 통증이 10일 넘게 계속되거나, 한쪽 코만 계속 막히면 이비인후과 진료를 먼저 받아 보세요.'))

    add('2026-10-23-neck-shoulder-stiffness.md', '## 이런 증상이 나타납니다', 'neck-stiffness',
        '담 결림이 생기는 원인과 확인할 점 그림', "흔히 '담 걸렸다'고 하는 결림은 근육과 인대가 놀라 굳은 상태입니다.",
        "'담 결림'은 이렇게 생깁니다", '대부분 근육이 풀리면서 좋아집니다.',
        flow([('원인', ['불편한 자세', '갑작스러운 움직임']), ('근육·인대가 굳음', ['목·어깨·등이', '결리고 잘 안 돌아감']), ('회복', ['근육이 풀리면서', '대부분 좋아짐'])], h=280,
             note='팔 저림이나 힘 빠짐이 함께 있으면 목디스크 등 다른 원인을 먼저 확인합니다.'))

    add('2026-10-23-sebaceous-hyperplasia.md', '## 여드름, 비립종과는 무엇이 다를까요?', 'sebaceous-hyperplasia',
        '피지선증식증 피부 단면 그림: 커진 피지선 위로 가운데가 살짝 패인 노르스름한 돌기', '피지를 만드는 피지선이 커져 생긴 양성 돌기입니다.',
        '피지선증식증은 피지선이 커진 것입니다', '이마와 볼, 코 주변에 2~5mm 크기로 생깁니다.',
        skin('seb_hyper', [('노르스름한 돌기', '가운데가 살짝 패인 모양'), ('짜도 없어지지 않음', '중년 이후 피지가 많은 피부에 흔함'), ('다시 생기기 쉬움', '레이저로 필요한 깊이만큼 치료')]))

    add('2026-10-24-epidermoid-cyst.md', '## 염증이 생기면 이렇게 됩니다', 'epidermoid-cyst',
        '표피낭종 피부 단면 그림: 진피 속 각질 주머니와 가운데 작은 검은 구멍', '주머니가 남아 있으면 다시 차오릅니다.',
        '표피낭종은 피부 속 각질 주머니입니다', '가운데 작은 검은 구멍이 보이고, 누르면 냄새나는 하얀 내용물이 나오기도 합니다.',
        skin('cyst', [('가운데 검은 구멍', '피부 표면과 이어진 작은 입구'), ('주머니가 핵심', '주머니가 남으면 다시 차오름'), ('치료', 'CO2 레이저나 니들로 작은 구멍을 내어 내용물과 주머니를 뺌')]))

    add('2026-10-24-facial-palsy.md', '## 이런 경우는 바로 응급실로 가세요', 'facial-palsy',
        '안면마비 증상과 응급 신호 비교 그림', '팔다리 힘 빠짐이나 말이 어눌해지는 증상이 함께 있으면 뇌졸중일 수 있습니다.',
        '안면마비, 먼저 이것을 구분하세요', '얼굴 근육을 움직이는 신경에 염증과 붓기가 생겨 갑자기 생깁니다.',
        compare(('안면마비(벨마비)', '얼굴 한쪽만', ['한쪽 눈이 잘 감기지 않음', '입이 한쪽으로 돌아감', '초기 치료가 중요'], GREEN),
                ('바로 응급실', '뇌졸중 의심 신호', ['팔다리 힘 빠짐', '말이 어눌해짐', '이마는 움직이는데 입 주변만 마비'], WARN), h=380))

    add('2026-10-25-ankle-sprain.md', '## 이런 경우는 골절부터 확인하세요', 'ankle-first-aid',
        '발목을 삐었을 때 처음 할 일 네 가지 그림: 쉬기, 차갑게, 압박, 올리기', '다친 직후에는 붓기를 줄이는 것이 중요합니다.',
        '발목을 삐었을 때, 다친 직후', '발목을 안쪽으로 접질리며 바깥쪽 인대가 늘어나거나 찢어진 상태입니다.',
        cards([('쉬기', ['다친 발목에', '무리를 주지 않기']), ('차갑게', ['차갑게 찜질해', '붓기 줄이기']), ('압박', ['붕대 등으로', '가볍게 압박']), ('올리기', ['다리를', '심장보다 높게'])], h=280)
        + callout(60, 490, '네 걸음도 걷기 어렵거나 복숭아뼈 끝을 눌렀을 때 아프면 골절부터 확인하세요.'))

    add('2026-10-25-steatocystoma.md', '## 다발성 피지낭종은 왜 생길까요?', 'cyst-compare',
        '표피낭종과 다발성 피지낭종 비교 그림', "흔히 '피지낭종'이라 부르는 혹은 대부분 표피낭종입니다.",
        '이름이 헷갈리는 두 가지 혹', '진짜 피지낭종은 피지선과 이어진 관에 생기는 주머니입니다.',
        compare(('표피낭종', '흔히 피지낭종이라 부르는 혹', ['치즈 같은 하얀 각질, 냄새', '가운데 구멍이 자주 보임', '하나 또는 몇 개', '얼굴, 귀 뒤, 목, 등'], '#8a6d3b'),
                ('다발성 피지낭종', '피지선과 이어진 관의 주머니', ['기름 같은 노란 액체', '가운데 구멍은 대개 없음', '여러 개, 많게는 수십 개', '가슴·겨드랑이·팔·목'], GREEN), h=400))

    add('2026-10-26-cherry-angioma.md', '## 거미혈관종이나 점과는 어떻게 다를까요?', 'cherry-angioma',
        '체리혈관종 피부 단면 그림: 작은 혈관이 늘어나 뭉친 선홍색 돌기', '체리혈관종은 작은 혈관이 늘어나 뭉쳐 생긴 점입니다.',
        '체리혈관종은 혈관이 뭉친 점입니다', '30대 이후 몸통과 팔에 하나둘 늘어나는 흔한 양성 병변입니다.',
        skin('cherry', [('선홍색 작은 점', '작은 혈관이 늘어나 뭉침'), ('건강에 해롭지 않음', '피부암이 아니지만 긁히면 피가 날 수 있음'), ('치료', '1064nm 롱펄스 레이저 등으로 치료')]))

    add('2026-10-26-menopause.md', '## 이런 경우는 먼저 확인이 필요합니다', 'menopause-symptoms',
        '갱년기 증후군의 주요 증상 그림', '폐경 전후로 여성호르몬이 줄면서 나타나는 증상입니다.',
        '갱년기, 이런 증상이 나타납니다', '증상의 종류와 정도는 사람마다 다릅니다.',
        cards([('열감·식은땀', ['얼굴이 화끈', '달아오르고 식은땀']), ('두근거림·불면', ['가슴이 두근거리고', '잠을 설침']), ('마음과 관절', ['예민함·우울감', '관절통'])], h=280)
        + callout(60, 490, '폐경 후 다시 출혈이 있거나 두근거림이 심하면 산부인과와 내과 검사를 먼저 받아 보세요.'))

    add('2026-10-27-insomnia.md', '## 잠들기 어려운 불면 (수면 개시 장애)', 'insomnia-types',
        '불면증 두 가지 유형 비교 그림: 잠들기 어려운 불면과 잠을 유지하기 어려운 불면', '두 가지로 나눠 보면 원인과 관리가 더 잘 보입니다.',
        '불면증은 두 가지로 나눠 봅니다', '유형에 따라 살펴볼 원인과 관리 방법이 다릅니다.',
        compare(('잠들기 어려운 불면', '수면 개시 장애', ['누워도 잠이 오지 않음', '긴장과 생각', '늦어진 생활 리듬', '자기 전 화면·카페인'], '#4f6a85'),
                ('잠을 유지하기 어려운 불면', '수면 유지 장애', ['자주 깨거나', '새벽에 일찍 깸', '다시 잠들기 어려움'], GREEN), h=420))

    add('2026-10-27-spider-angioma.md', '## 왜 생길까요?', 'spider-angioma',
        '거미혈관종 그림: 가운데 붉은 점에서 가는 혈관이 거미 다리처럼 뻗은 모양', '가운데를 누르면 색이 사라졌다가 다시 차오릅니다.',
        '거미혈관종은 이런 모양입니다', '얼굴·목·가슴·손등에 잘 생기며 어린이와 임신 중에 흔합니다.',
        top_view('spider', [('누르면 사라짐', '가운데를 누르면 색이 사라졌다가 다시 차오름'), ('대부분 문제없음', '어린이와 임신 중에 흔함'), ('어른에게 짧은 기간에 여러 개라면', '간 건강을 확인하는 검사를 받아 보세요')]))

    add('2026-10-28-porokeratosis.md', '## 여러 형태가 있습니다', 'porokeratosis',
        '한공각화증 그림: 테두리가 실처럼 가늘게 솟은 고리 모양 반점', '햇빛을 많이 받은 팔다리에 여러 개 생기는 형태가 가장 흔합니다.',
        '한공각화증은 고리 모양 반점입니다', '대부분 양성이지만 정확한 진단과 정기 확인이 중요합니다.',
        top_view('poro', [('고리 모양', '테두리가 실처럼 가늘게 솟음'), ('잘 생기는 곳', '햇빛을 많이 받은 팔다리, 얼굴'), ('정기 확인', '드물게 오래된 병변에서 피부암 사례가 보고되어 변화를 살핌')]))

    add('2026-10-28-shoulder-pain.md', '## 이런 증상이 있다면 회전근개를 의심해 보세요', 'shoulder-causes',
        '어깨 통증의 여러 원인 그림: 회전근개 손상, 충돌증후군, 석회성 건염', '팔을 들 때 아프다면 어깨를 움직이는 네 개의 힘줄을 살펴봐야 합니다.',
        '팔을 들 때 아픈 어깨, 원인이 여러 가지입니다', '원인에 따라 치료와 주의할 점이 달라집니다.',
        cards([('회전근개 손상', ['어깨를 움직이는', '네 개의 힘줄 손상']), ('충돌증후군', ['팔을 들 때 어깨뼈와', '힘줄이 부딪히며 아픔']), ('석회성 건염', ['힘줄에 석회가 쌓여', '갑자기 심한 통증이 생기기도 함'])], h=280)
        + callout(60, 490, '다친 뒤 갑자기 팔을 전혀 들 수 없다면 힘줄 파열 여부를 먼저 확인하세요.'))

    add('2026-10-29-flat-warts.md', '## 편평사마귀 치료는 이렇게 합니다', 'flat-warts-spread',
        '편평사마귀가 번지는 과정 그림', '긁거나 면도하면 그 자리를 따라 번질 수 있습니다.',
        '편평사마귀는 이렇게 번집니다', '사람유두종바이러스(HPV)가 피부에 감염되어 생깁니다.',
        flow([('감염', ['HPV가 피부에', '감염됨']), ('긁기·면도', ['작은 상처가', '생김']), ('번짐', ['그 자리를 따라', '새 돌기가 생김'])], h=280,
             note='치료 기간에는 시술 부위를 긁거나 면도로 자극하지 않는 것이 좋습니다.'))

    add('2026-10-29-reflux.md', '## 왜 생길까요?', 'reflux-symptoms',
        '역류성 식도염 증상과 원인 그림', '위산과 위 내용물이 식도로 거꾸로 올라와 생깁니다.',
        '역류성 식도염, 증상과 원인', '생활 습관 교정이 치료의 기본입니다.',
        compare(('이런 증상', '', ['가슴 쓰림', '신물이 올라옴', '목에 뭔가 걸린 느낌', '마른기침'], WARN),
                ('흔한 원인', '', ['과식, 늦은 밤 식사', '비만', '술·커피·기름진 음식'], GREEN), h=420))

    add('2026-10-30-carpal-tunnel.md', '## 이런 증상이 나타납니다', 'carpal-tunnel',
        '손목터널증후군 그림: 손목 안쪽 통로에서 신경이 눌려 엄지·검지·중지가 저림', '손목 안쪽의 좁은 통로에서 신경이 눌려 생깁니다.',
        '손목터널증후군은 이렇게 생깁니다', '손을 많이 쓰는 분, 임신 중이거나 갱년기 여성에게 흔합니다.',
        cards([('저린 손가락', ['엄지·검지·중지가', '주로 저림']), ('밤에 심해짐', ['밤이나 새벽에', '저림이 심해짐']), ('검사가 필요할 때', ['엄지 쪽 근육이 마르거나', '힘이 빠질 때'])], h=300))

    add('2026-10-31-dysmenorrhea.md', '## 이런 경우는 먼저 산부인과 진료를 받아 보세요', 'dysmenorrhea-types',
        '생리통 두 가지 비교 그림: 특별한 질환 없이 생기는 생리통과 원인 질환이 있는 생리통', '자궁이 수축할 때 나오는 물질이 많을수록 통증이 심해집니다.',
        '생리통은 두 가지로 나뉩니다', '특별한 질환 없이 생기는 경우가 많습니다.',
        compare(('특별한 질환 없이', '원발성 생리통', ['생리 직전이나 생리 중', '아랫배가 쥐어짜듯 아픔', '허리·허벅지까지 당김'], GREEN),
                ('먼저 산부인과 확인', '원인 질환이 있는 경우', ['통증이 해마다 심해짐', '생리 양이 갑자기 변함'], WARN), h=380))

    add('2026-11-01-atopic-dermatitis.md', '## 이런 경우는 먼저 진료가 필요합니다', 'atopy-cycle',
        '아토피 피부염의 가려움과 긁기 악순환 그림', '긁을수록 피부 장벽이 더 상합니다.',
        '가려움과 긁기의 악순환', '충분한 보습과 염증 관리로 이 고리를 끊는 것이 중요합니다.',
        flow([('가려움', ['심한 가려움']), ('긁기', ['참기 어려워 긁음']), ('장벽 손상', ['수분이 빠지고', '자극에 약해짐']), ('염증', ['붉은 습진', '→ 다시 가려움'])], h=260,
             note='충분한 보습으로 피부 장벽을 지키는 것이 생활 관리의 기본입니다.'))

    add('2026-11-02-elbow-pain.md', '## 운동을 하지 않아도 생깁니다', 'elbow-types',
        '테니스 엘보와 골프 엘보 비교 그림: 팔꿈치 바깥쪽과 안쪽 힘줄', '반복 사용으로 힘줄에 염증과 미세 손상이 생깁니다.',
        '테니스 엘보와 골프 엘보', '물건을 쥐거나 들 때 팔꿈치가 아픈 질환입니다.',
        compare(('테니스 엘보', '팔꿈치 바깥쪽', ['바깥쪽 힘줄의', '염증과 미세 손상'], '#8a6d3b'),
                ('골프 엘보', '팔꿈치 안쪽', ['안쪽 힘줄의', '염증과 미세 손상'], GREEN),
                h=300, note='이름과 달리 집안일, 컴퓨터 작업, 무거운 짐 들기처럼 손목을 많이 쓰는 일로도 흔히 생깁니다.'))

    add('2026-11-03-cold-hands-feet.md', '## 이런 증상이 나타납니다', 'cold-hands-causes',
        '수족냉증의 흔한 원인 그림', '다른 사람은 춥지 않은 온도에서도 손발이 유난히 찬 상태입니다.',
        '손발이 찬 이유', '여러 원인이 함께 있는 경우가 많습니다.',
        cards([('혈관 수축', ['혈관이 쉽게', '수축하는 경향']), ('적은 근육량', ['열을 만드는', '근육이 적음']), ('스트레스·다이어트', ['스트레스와', '무리한 다이어트'])], h=280)
        + callout(60, 490, '추위나 긴장에 손가락 색이 하얗게·파랗게 변하거나, 한쪽 다리만 차면 먼저 검사를 받아 보세요.'))

    add('2026-11-04-numbness.md', '## 이런 경우는 바로 응급실로 가세요', 'numbness-map',
        '저린 위치에 따라 생각해 볼 원인 그림', '손발 저림은 혈액순환보다 신경이 눌리거나 약해져 생기는 경우가 많습니다.',
        '저린 위치를 보면 원인이 보입니다', '어디가 어떻게 저린지가 중요한 단서입니다.',
        cards([('한쪽 팔·손가락', ['목·어깨 통증과 함께', '→ 목디스크']), ('엄지~약지, 밤에', ['손목 안쪽 신경 눌림', '→ 손목터널증후군']), ('한쪽 다리로 뻗침', ['엉덩이에서 다리로', '→ 허리디스크']), ('양쪽 발끝부터', ['장갑·양말처럼', '→ 말초신경병증'])], h=300)
        + callout(60, 510, '갑자기 한쪽 팔다리가 저리고 힘이 빠지면 뇌졸중일 수 있어 즉시 응급실로 가세요.'))

    add('2026-11-05-postpartum.md', '## 이런 증상이 나타납니다', 'postpartum-causes',
        '산후풍이 생기는 원인 그림', '출산 후 관절이 시리고 아프며 찬 바람이 드는 듯한 느낌이 이어지는 상태입니다.',
        '산후풍은 왜 생길까요?', '여러 원인이 겹쳐 손목·무릎·허리·발목이 시리고 아픕니다.',
        cards([('느슨해진 관절', ['임신 중 느슨해진', '관절과 인대']), ('떨어진 체력', ['출산으로', '떨어진 체력']), ('반복 동작', ['아기를 안고', '돌보는 반복 동작'])], h=300))

    add('2026-11-06-plantar-fasciitis.md', '## 아킬레스건 질환과는 다릅니다', 'plantar-fasciitis',
        '족저근막염 증상 그림: 아침 첫발과 오래 앉았다 일어날 때 발뒤꿈치 통증', '족저근막이 발뒤꿈치에 붙는 자리에 염증과 미세 손상이 생깁니다.',
        '족저근막염, 이럴 때 아픕니다', '오래 서 있거나 많이 걷는 분, 체중이 늘었거나 쿠션 없는 신발을 신는 분께 흔합니다.',
        cards([('아침 첫발', ['자고 일어나 첫발을', '디딜 때 찌르듯 아픔']), ('앉았다 일어날 때', ['오래 앉아 있다가', '걷기 시작할 때']), ('걷다 보면', ['몇 걸음 걸으면 나아지다가', '오래 걸으면 다시 아픔'])], h=320))

    add('2026-11-07-hwabyung.md', '## 이런 경우는 먼저 확인이 필요합니다', 'hwabyung-flow',
        '화병이 몸의 증상으로 나타나는 흐름 그림', '감정을 오래 참으면서 몸의 증상으로 나타나는 상태입니다.',
        '화병은 이렇게 나타납니다', '불안과 함께 오는 경우가 많습니다.',
        flow([('오래 참은 감정', ['억울함, 분노를', '오래 참음']), ('몸의 증상', ['가슴 답답함', '치밀어 오르는 열감']), ('함께 오는 것', ['두근거림', '불면'])], h=280,
             note='가슴 통증이 운동할 때 심해지거나 식은땀·숨 가쁨이 함께 있으면 바로 응급실로 가세요.'))

    add('2026-11-08-ibs.md', '## 이런 경우는 대장내시경을 먼저 받으세요', 'ibs-types',
        '과민성 대장 증후군 유형 그림: 설사형, 변비형, 혼합형', '배변 후 복통이 줄어드는 것이 특징입니다.',
        '과민성 대장 증후군, 세 가지 유형', '장이 예민해진 상태에 스트레스와 식습관이 더해져 증상이 오르내립니다.',
        cards([('설사형', ['묽은 변을 자주 봄', '갑자기 급하게', '화장실을 찾음']), ('변비형', ['변이 단단하고', '배변이 힘듦', '배가 빵빵함']), ('혼합형', ['설사와 변비가', '번갈아 나타남'])], h=300)
        + callout(60, 510, '변에 피가 섞이거나, 이유 없는 체중 감소가 있거나, 50세 이후 새로 생긴 배변 변화라면 대장내시경을 먼저 받으세요.'))

    add('2026-11-09-chronic-fatigue.md', '## 검사는 정상인데 계속 피곤하다면', 'fatigue-check',
        '만성 피로에서 먼저 확인할 원인 질환 그림', '원인이 되는 질환이 숨어 있을 수 있어 기본 검사를 먼저 받아 보는 것이 좋습니다.',
        '만성 피로, 먼저 원인 질환을 확인하세요', '충분히 쉬어도 몇 주 이상 피로가 이어진다면',
        cards([('혈액·호르몬', ['빈혈', '갑상선 기능 저하', '당뇨']), ('간·수면', ['간 질환', '수면무호흡']), ('마음', ['우울증'])], h=300, numbered=False)
        + callout(60, 500, '검사에서 이상이 없는데도 피곤하다면 생활 습관과 몸 상태를 함께 살펴 관리합니다.', GREEN))

    add('2026-11-10-alopecia-areata.md', '## 왜 생길까요?', 'alopecia-areata',
        '원형 탈모 그림: 두피에 동전 모양으로 머리카락이 빠진 자리', '면역 체계가 모낭을 잘못 공격해 생깁니다.',
        '원형 탈모는 이런 모습입니다', '스트레스와 피로가 겹칠 때 생기거나 심해지는 경우가 많습니다.',
        top_view('alopecia', [('동전 모양', '머리카락이 갑자기 둥글게 빠짐'), ('저절로 회복되기도', '작은 반점은 몇 달 사이 회복되기도 하지만 재발이 흔함'), ('여러 개이거나 빠르게 커지면', '피부과 진료를 함께 받아 주세요')]))
    return S


def write_svgs(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for s in specs():
        open(os.path.join(out_dir, s['name'] + '.svg'), 'w', encoding='utf-8').write(svg(s))


def add_figures(col_dir):
    for s in specs():
        f = os.path.join(col_dir, s['md'])
        md = open(f, encoding='utf-8').read()
        if f'img/{s["name"]}.webp' in md:
            continue
        assert md.count(s['before']) == 1, (s['md'], s['before'])
        fig = (f'<figure style="margin: 8px 0 24px">\n<img src="img/{s["name"]}.webp" alt="{s["alt"]}" '
               f'style="display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid #e2dccd">\n'
               f'<figcaption style="margin-top: 8px; font-size: 14px; color: #5d655f">{s["cap"]} (갈창림 한의원 제작 설명 그림)</figcaption>\n</figure>\n\n')
        open(f, 'w', encoding='utf-8').write(md.replace(s['before'], fig + s['before'], 1))


if __name__ == '__main__':
    import sys
    base = sys.argv[1]
    write_svgs(os.path.join(base, 'img-src2'))
    if len(sys.argv) > 2 and sys.argv[2] == 'insert':
        add_figures(base)
