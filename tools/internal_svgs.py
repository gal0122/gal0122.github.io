"""내과 질환 페이지 그림 (SVG). Run: python3 internal_svgs.py -> galch/img/*.svg"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galch', 'img') + '/'
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif"
INK, SUB, GREY, BG = "#1a1a1a", "#8a6a5a", "#555555", "#fbfbfb"
SKIN, SKIN_L = "#f3e1d4", "#c9a48e"
RED, BLUE, GREEN = "#e2463a", "#3f86c9", "#2f5241"
HAIR = "#5b4636"


def t(x, y, s, size=16, w=400, col=INK, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="{w}" fill="{col}">{s}</text>'


def head(W, H):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
            '<defs>'
            '<radialGradient id="infl" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#e2463a" stop-opacity="0.55"/><stop offset="100%" stop-color="#e2463a" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="cold" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#3f86c9" stop-opacity="0.6"/><stop offset="100%" stop-color="#3f86c9" stop-opacity="0"/></radialGradient>'
            '<marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1a1a1a"/></marker>'
            '<marker id="arrR" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#e2463a"/></marker>'
            '<marker id="arrB" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#3f86c9"/></marker>'
            '</defs>']


def frame(x0, y0, w, h):
    return f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{BG}" stroke="#cfcfcf" stroke-width="1.5"/>'


def glow(x, y, r, gid="infl"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})"/>'


def lead(x1, y1, x2, y2, col=INK):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1.2" fill="none"/><circle cx="{x1}" cy="{y1}" r="3" fill="{col}"/>'


def label(x, y, title, desc, anchor="start", col=INK):
    return t(x, y, title, 17, 700, col, anchor) + t(x, y + 22, desc, 13.5, 400, GREY, anchor)


# ---------- 1. 소화기 ----------
def digestive_map():
    W, H = 1100, 650
    o = head(W, H)
    cx = 550
    # body
    o.append(f'<circle cx="{cx}" cy="64" r="44" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<rect x="{cx-20}" y="100" width="40" height="52" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<path d="M{cx-130} 176 Q{cx-130} 150 {cx-96} 146 L{cx+96} 146 Q{cx+130} 150 {cx+130} 176 '
             f'L{cx+118} 400 Q{cx+124} 520 {cx+140} 606 L{cx-140} 606 Q{cx-124} 520 {cx-118} 400 Z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<rect x="{cx-21}" y="128" width="42" height="26" fill="{SKIN}"/>')
    # large intestine (frame)
    colon = f'M{cx-62} 568 L{cx-70} 470 L{cx-66} 418 Q{cx-60} 404 {cx-40} 406 L{cx+60} 402 Q{cx+82} 402 {cx+84} 424 L{cx+86} 540 Q{cx+84} 584 {cx+40} 582 Q{cx+10} 580 {cx+4} 596'
    o.append(f'<path d="{colon}" fill="none" stroke="#c99a66" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="{colon}" fill="none" stroke="#ecc9a0" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>')
    for yy in range(430, 560, 22):   # haustra marks
        o.append(f'<path d="M{cx-84} {yy} q14 6 28 0" fill="none" stroke="#d3ab7d" stroke-width="1.5"/>')
        o.append(f'<path d="M{cx+70} {yy} q14 6 28 0" fill="none" stroke="#d3ab7d" stroke-width="1.5"/>')
    # small intestine (coils)
    si = f'M{cx-36} 440 q22 -14 44 0 t44 0 t20 18 q-22 14 -44 0 t-44 0 t-20 18 q22 14 44 0 t44 0 t20 18 q-22 14 -44 0 t-44 0 t-20 18 q22 14 44 0 t52 4'
    o.append(f'<path d="{si}" fill="none" stroke="#d9a593" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="{si}" fill="none" stroke="#f5d3c6" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    # esophagus
    eso = f'M{cx} 112 C{cx+2} 180 {cx+6} 240 {cx+18} 300'
    o.append(f'<path d="{eso}" fill="none" stroke="#d99a88" stroke-width="20" stroke-linecap="round"/>')
    o.append(f'<path d="{eso}" fill="none" stroke="#f4c6b8" stroke-width="15" stroke-linecap="round"/>')
    # stomach
    o.append(f'<path d="M{cx+10} 296 Q{cx+24} 284 {cx+56} 286 Q{cx+102} 292 {cx+100} 336 Q{cx+98} 380 {cx+56} 394 '
             f'Q{cx+10} 404 {cx-28} 386 L{cx-40} 372 Q{cx-30} 360 {cx-14} 366 Q{cx+20} 374 {cx+36} 358 Q{cx+48} 340 {cx+30} 322 Q{cx+18} 312 {cx+10} 296 Z" '
             f'fill="#f6d2c4" stroke="#d99a88" stroke-width="2.5"/>')
    o.append(f'<path d="M{cx+12} 300 L{cx+26} 292" stroke="#b8604d" stroke-width="5" stroke-linecap="round"/>')   # sphincter
    duo = f'M{cx-36} 380 Q{cx-50} 404 {cx-40} 438'
    o.append(f'<path d="{duo}" fill="none" stroke="#d9a593" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<path d="{duo}" fill="none" stroke="#f5d3c6" stroke-width="10" stroke-linecap="round"/>')
    # problem marks
    o.append(glow(cx + 14, 274, 34))
    o.append(f'<path d="M{cx+30} 318 C{cx+26} 300 {cx+20} 286 {cx+14} 262" fill="none" stroke="{RED}" stroke-width="2.5" marker-end="url(#arrR)"/>')
    o.append(glow(cx + 62, 340, 44))
    o.append(glow(cx + 84, 500, 44))
    o.append(glow(cx - 66, 480, 36))
    # organ names
    o.append(t(cx - 24, 214, '식도', 14, 700, SUB, 'end'))
    o.append(t(cx + 64, 350, '위', 15, 700, SUB))
    o.append(t(cx + 6, 532, '소장', 14, 700, SUB))
    o.append(t(cx - 96, 470, '대장', 14, 700, SUB, 'end'))
    # callouts
    o.append(lead(cx + 14, 286, cx - 170, 250))
    o.append(label(cx - 180, 236, '역류성 식도염', '조임근이 느슨해져 위산이 식도로 올라옴', 'end'))
    o.append(lead(cx + 76, 330, cx + 230, 316))
    o.append(label(cx + 240, 302, '기능성 소화불량', '위가 잘 늘어나지 않고 움직임이 둔해짐'))
    o.append(lead(cx + 86, 506, cx + 230, 500))
    o.append(label(cx + 240, 486, '과민성 대장 증후군', '장이 예민해져 움직임이 불규칙함'))
    o.append(t(W / 2, H - 14, '검사에서 뚜렷한 이상이 없어도 위장의 움직임과 예민함 때문에 불편이 반복될 수 있습니다', 13, 400, '#777777'))
    o.append('</svg>')
    return '\n'.join(o)


# ---------- 2. 두통 · 안면마비 ----------
def face(cx, cy, palsy=False):
    o = []
    o.append(f'<path d="M{cx-58} {cy+150} Q{cx-60} {cy+112} {cx-26} {cy+100} L{cx+26} {cy+100} Q{cx+60} {cy+112} {cx+58} {cy+150}" fill="none"/>')
    # shoulders + neck
    o.append(f'<path d="M{cx-140} {cy+204} Q{cx-136} {cy+150} {cx-70} {cy+140} L{cx-26} {cy+120} L{cx+26} {cy+120} L{cx+70} {cy+140} Q{cx+136} {cy+150} {cx+140} {cy+204} Z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<rect x="{cx-26}" y="{cy+70}" width="52" height="64" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<rect x="{cx-25}" y="{cy+120}" width="50" height="22" fill="{SKIN}"/>')
    # ears
    o.append(f'<ellipse cx="{cx-76}" cy="{cy+6}" rx="12" ry="20" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<ellipse cx="{cx+76}" cy="{cy+6}" rx="12" ry="20" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    # face
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="76" ry="96" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<path d="M{cx-77} {cy-14} Q{cx-84} {cy-104} {cx} {cy-100} Q{cx+84} {cy-104} {cx+77} {cy-14} Q{cx+68} {cy-76} {cx+16} {cy-80} Q{cx-48} {cy-82} {cx-77} {cy-14} Z" fill="{HAIR}"/>')
    # nose
    o.append(f'<path d="M{cx} {cy+2} L{cx-8} {cy+34} Q{cx} {cy+40} {cx+8} {cy+34}" fill="none" stroke="{SKIN_L}" stroke-width="2" stroke-linecap="round"/>')
    if not palsy:
        for s in (-1, 1):
            o.append(f'<path d="M{cx+s*16} {cy-22} Q{cx+s*32} {cy-30} {cx+s*48} {cy-22}" fill="none" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/>')
            o.append(f'<ellipse cx="{cx+s*32}" cy="{cy-2}" rx="10" ry="5.5" fill="{INK}"/>')
        o.append(f'<path d="M{cx-24} {cy+58} Q{cx} {cy+66} {cx+24} {cy+58}" fill="none" stroke="#b8604d" stroke-width="3.5" stroke-linecap="round"/>')
    else:
        # healthy side = viewer's right; affected = viewer's left
        o.append(f'<path d="M{cx+16} {cy-26} Q{cx+32} {cy-36} {cx+48} {cy-28}" fill="none" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="{cx+32}" cy="{cy-4}" rx="10" ry="4.5" fill="{INK}"/>')
        for k in range(3):   # forehead wrinkles only on healthy side
            yy = cy - 44 - k * 9
            o.append(f'<path d="M{cx+8} {yy} Q{cx+30} {yy-4} {cx+52} {yy}" fill="none" stroke="{SKIN_L}" stroke-width="1.6"/>')
        o.append(f'<path d="M{cx-48} {cy-16} Q{cx-32} {cy-18} {cx-16} {cy-16}" fill="none" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="{cx-32}" cy="{cy}" rx="11" ry="9" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{cx-32}" cy="{cy+1}" r="5.5" fill="{INK}"/>')
        o.append(f'<path d="M{cx-38} {cy+14} q-3 8 0 12 q3 -4 0 -12" fill="#9fc6e8"/>')   # tear
        o.append(f'<path d="M{cx-28} {cy+70} Q{cx-6} {cy+62} {cx+8} {cy+58} Q{cx+20} {cy+54} {cx+28} {cy+50}" fill="none" stroke="#b8604d" stroke-width="3.5" stroke-linecap="round"/>')
    return '\n'.join(o)


def headache_types():
    W, H = 1200, 480
    o = head(W, H)
    panels = [(15, '긴장성 두통', '머리를 띠로 조이듯 뻐근하고, 목·어깨가 굳어 있음'),
              (415, '편두통', '주로 한쪽이 욱신욱신, 빛과 소리에 예민해짐'),
              (815, '안면마비 (벨마비)', '한쪽 얼굴 근육에 갑자기 힘이 빠짐')]
    for i, (x0, name, desc) in enumerate(panels):
        o.append(frame(x0, 30, 370, 344))
        cx, cy = x0 + (185 if i == 1 else 212), 168
        o.append(face(cx, cy, palsy=(i == 2)))
        if i == 0:
            o.append(f'<ellipse cx="{cx}" cy="{cy-40}" rx="84" ry="26" fill="none" stroke="{RED}" stroke-width="12" opacity="0.45"/>')
            for s in (-1, 1):
                o.append(f'<path d="M{cx+s*126} {cy-40} L{cx+s*96} {cy-40}" stroke="{RED}" stroke-width="2.5" marker-end="url(#arrR)"/>')
            o.append(glow(cx - 74, cy + 150, 30))
            o.append(glow(cx + 74, cy + 150, 30))
            o.append(lead(cx - 74, cy + 150, x0 + 50, cy + 104))
            o.append(t(x0 + 22, cy + 76, '굳은', 14, 700, RED, 'start'))
            o.append(t(x0 + 22, cy + 96, '목·어깨', 14, 700, RED, 'start'))
            o.append(t(x0 + 22, 62, '조이는 느낌', 14, 700, RED, 'start'))
            o.append(f'<path d="M{x0+70} 68 L{cx-60} {cy-58}" stroke="{INK}" stroke-width="1.2"/>')
        elif i == 1:
            o.append(glow(cx + 66, cy - 30, 46))
            for k, r in enumerate((26, 38, 50)):
                o.append(f'<path d="M{cx+80+r*0.5} {cy-30-r*0.8} A{r} {r} 0 0 1 {cx+80+r*0.5} {cy-30+r*0.8}" fill="none" stroke="{RED}" stroke-width="2.5" opacity="{0.9-k*0.25}"/>')
            o.append(t(x0 + 348, 62, '한쪽 관자놀이', 14, 700, RED, 'end'))
            o.append(t(x0 + 348, 82, '욱신욱신', 14, 400, GREY, 'end'))
        else:
            o.append(lead(cx - 26, cy - 54, x0 + 30, 74))
            o.append(t(x0 + 26, 62, '이마 주름이 안 잡힘', 13.5, 700, RED, 'start'))
            o.append(lead(cx - 44, cy + 2, x0 + 70, cy + 22))
            o.append(t(x0 + 20, cy + 36, '눈이 잘', 13.5, 700, RED, 'start'))
            o.append(t(x0 + 20, cy + 54, '감기지 않음', 13.5, 700, RED, 'start'))
            o.append(lead(cx - 28, cy + 70, x0 + 70, cy + 100))
            o.append(t(x0 + 20, cy + 116, '입꼬리', 13.5, 700, RED, 'start'))
            o.append(t(x0 + 20, cy + 134, '처짐', 13.5, 700, RED, 'start'))
        o.append(t(x0 + 185, 412, name, 20, 700))
        o.append(t(x0 + 185, 440, desc, 14.5, 400, GREY))
    o.append('</svg>')
    return '\n'.join(o)


# ---------- 3. 수면 ----------
def sleep_types():
    W, H = 1200, 440
    o = head(W, H)
    x0, hour = 270, 100      # 22:00 at x0
    X = lambda h: x0 + (h - 22) * hour
    rows = [('정상 수면', '', [(23.25, 6.5, 's')]),
            ('잠들기 어려운 불면', '수면 개시 장애', [(23.0, 1.5, 'w'), (1.5, 6.5, 's')]),
            ('잠을 유지하기 어려운 불면', '수면 유지 장애', [(23.25, 1.6, 's'), (1.6, 2.15, 'w'), (2.15, 3.5, 's'), (3.5, 3.85, 'w'), (3.85, 4.6, 's'), (4.6, 6.5, 'w')])]
    norm = lambda h: h + 24 if h < 12 else h
    # legend
    o.append(f'<rect x="{W-330}" y="26" width="18" height="18" rx="4" fill="{GREEN}"/>' + t(W - 304, 41, '잠든 시간', 14, 500, INK, 'start'))
    o.append(f'<rect x="{W-190}" y="26" width="18" height="18" rx="4" fill="#f2b56b"/>' + t(W - 164, 41, '깨어 있는 시간', 14, 500, INK, 'start'))
    for i, (name, sub, segs) in enumerate(rows):
        y = 100 + i * 96
        o.append(t(x0 - 24, y + 4, name, 16, 700, INK, 'end'))
        if sub:
            o.append(t(x0 - 24, y + 26, sub, 13, 400, GREY, 'end'))
        o.append(f'<rect x="{X(23)}" y="{y-14}" width="{X(30.5)-X(23)}" height="36" rx="8" fill="#f2efe8"/>')
        for a, b, kind in segs:
            a, b = norm(a), norm(b)
            col = GREEN if kind == 's' else '#f2b56b'
            o.append(f'<rect x="{X(a)+1}" y="{y-14}" width="{X(b)-X(a)-2}" height="36" rx="6" fill="{col}"/>')
        if i == 1:
            o.append(t((X(23) + X(25.5)) / 2, y + 9, '누워도 잠이 오지 않음', 13, 700, '#7a4a12'))
        if i == 2:
            o.append(t((X(28.6) + X(30.5)) / 2, y + 9, '새벽에 깨서 못 잠', 13, 700, '#7a4a12'))
            for a in (25.6, 27.5):
                o.append(f'<path d="M{X(a)+8} {y-22} L{X(a)+8} {y-16}" stroke="#7a4a12" stroke-width="2"/>')
            o.append(t(X(26.5), y - 26, '자주 깸', 13, 700, '#7a4a12'))
    ay = 100 + 3 * 96 - 20
    o.append(f'<line x1="{X(22)}" y1="{ay}" x2="{X(31)}" y2="{ay}" stroke="#bbbbbb" stroke-width="1.5"/>')
    for h in range(22, 32):
        o.append(f'<line x1="{X(h)}" y1="{ay-6}" x2="{X(h)}" y2="{ay+6}" stroke="#bbbbbb" stroke-width="1.5"/>')
        o.append(t(X(h), ay + 26, f'{h % 24:02d}시', 13, 500, GREY))
    o.append(t(W / 2, H - 12, '두 가지가 함께 나타나는 경우도 많습니다. 시간은 이해를 돕기 위한 예시입니다', 13, 400, '#777777'))
    o.append('</svg>')
    return '\n'.join(o)


# ---------- 4. 비염 ----------
def wall(x0, x1, y, amp, thick, up, fill, line):
    """mucosa wall: wavy edge at y, extending `thick` away (up=True -> upper wall)."""
    pts = []
    n = 8
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        yy = y + (amp if k % 2 else -amp) * (1 if up else -1) * 0.6
        pts.append((x, yy))
    edge = ' '.join(f'{x:.1f} {yy:.1f}' for x, yy in pts)
    far = y - thick if up else y + thick
    return (f'<path d="M{x0} {far} L{edge.split(" ")[0]} {pts[0][1]:.1f} '
            + ' '.join(f'Q{(pts[k][0]+pts[k+1][0])/2:.1f} {pts[k][1] + (8 if up else -8):.1f} {pts[k+1][0]:.1f} {pts[k+1][1]:.1f}' for k in range(n))
            + f' L{x1} {far} Z" fill="{fill}" stroke="{line}" stroke-width="2"/>')


def rhinitis_nose():
    W, H = 1100, 440
    o = head(W, H)
    for i, x0 in enumerate((15, 565)):
        o.append(frame(x0, 30, 520, 316))
        a, b = x0 + 40, x0 + 480
        bone = '#f1e7da'
        o.append(f'<rect x="{a}" y="56" width="{b-a}" height="40" fill="{bone}" stroke="#b9a48c" stroke-width="1.5"/>')
        o.append(f'<rect x="{a}" y="282" width="{b-a}" height="40" fill="{bone}" stroke="#b9a48c" stroke-width="1.5"/>')
        if i == 0:
            o.append(wall(a, b, 140, 6, 44, True, '#f6cfc8', '#d99a8f'))
            o.append(wall(a, b, 238, 6, 44, False, '#f6cfc8', '#d99a8f'))
            for yy in (172, 190, 208):
                o.append(f'<path d="M{a+20} {yy} L{b-30} {yy}" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrB)"/>')
            o.append(t(x0 + 260, 378, '정상 코 점막', 20, 700))
            o.append(t(x0 + 260, 406, '숨길이 넓고 공기가 잘 지나갑니다', 14.5, 400, GREY))
        else:
            o.append(wall(a, b, 172, 9, 76, True, '#f0a99f', '#cf6f62'))
            o.append(wall(a, b, 206, 9, 76, False, '#f0a99f', '#cf6f62'))
            o.append(f'<path d="M{a+20} 189 L{a+150} 189" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrB)"/>')
            for dx, dy in ((200, 156), (290, 160), (370, 152), (250, 228), (340, 224), (420, 230)):
                o.append(f'<path d="M{x0+dx} {dy} q-6 10 0 14 q6 -4 0 -14" fill="#cfe4f5" stroke="#8fb7d9" stroke-width="1"/>')
            for dx, dy in ((14, 120), (26, 150), (10, 230), (30, 262), (18, 200)):
                o.append(f'<circle cx="{a+dx-30}" cy="{dy}" r="4" fill="#c99a3a"/>')
            o.append(lead(x0 + 330, 130, x0 + 420, 48))
            o.append(t(x0 + 500, 50, '점막이 붓고 예민해짐', 13.5, 700, RED, 'end'))
            o.append(lead(x0 + 343, 232, x0 + 420, 330))
            o.append(t(x0 + 500, 340, '맑은 콧물', 13.5, 700, BLUE, 'end'))
            o.append(t(x0 + 22, 340, '알레르기 물질·찬 공기', 12.5, 700, '#9a7426', 'start'))
            o.append(t(x0 + 260, 378, '비염', 20, 700))
            o.append(t(x0 + 260, 406, '점막이 부어 숨길이 좁아지고 콧물·재채기가 납니다', 14.5, 400, GREY))
        o.append(t(a, 50, '코 안쪽 숨길을 옆에서 본 모습', 12.5, 500, '#888888', 'start'))
    o.append(t(560 + 15, 433, '집먼지진드기·꽃가루 같은 알레르기 물질이나 찬 공기에 점막이 과민하게 반응합니다', 13, 400, '#777777'))
    o.append('</svg>')
    return '\n'.join(o)


# ---------- 5. 수족냉증 ----------
def limb(pts, w):
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{SKIN_L}" stroke-width="{w+4}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{SKIN}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def cold_body():
    W, H = 1000, 640
    o = head(W, H)
    cx = 500
    o.append(limb([(cx - 34, 330), (cx - 40, 460), (cx - 42, 585)], 40))
    o.append(limb([(cx + 34, 330), (cx + 40, 460), (cx + 42, 585)], 40))
    o.append(limb([(cx - 78, 168), (cx - 100, 262), (cx - 112, 352)], 30))
    o.append(limb([(cx + 78, 168), (cx + 100, 262), (cx + 112, 352)], 30))
    o.append(f'<path d="M{cx-82} 160 Q{cx-86} 150 {cx-60} 146 L{cx+60} 146 Q{cx+86} 150 {cx+82} 160 L{cx+70} 250 L{cx+66} 340 L{cx-66} 340 L{cx-70} 250 Z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<rect x="{cx-16}" y="112" width="32" height="40" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    o.append(f'<circle cx="{cx}" cy="78" r="42" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>')
    for x, y, r in ((cx - 112, 356, 46), (cx + 112, 356, 46), (cx - 42, 588, 44), (cx + 42, 588, 44), (cx, 300, 52), (cx - 40, 462, 28), (cx + 40, 462, 28)):
        o.append(glow(x, y, r, 'cold'))
    left = [((cx - 112, 356), 356, '손끝', '혈관이 쉽게 수축해 차고 시림'),
            ((cx - 42, 588), 560, '발끝', '양말을 신어야 잠들 수 있음')]
    right = [((cx, 300), 290, '아랫배', '늘 차고 생리통과 함께 오기도 함'),
             ((cx + 40, 462), 450, '무릎', '시리고 찬 기운이 듦')]
    for (x, y), ly, name, desc in left:
        o.append(f'<path d="M{x-10} {y} L{330} {ly} L{300} {ly}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        o.append(t(290, ly - 2, name, 17, 700, BLUE, 'end'))
        o.append(t(290, ly + 20, desc, 13.5, 400, GREY, 'end'))
    for (x, y), ly, name, desc in right:
        o.append(f'<path d="M{x+12} {y} L{670} {ly} L{700} {ly}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        o.append(t(710, ly - 2, name, 17, 700, BLUE, 'start'))
        o.append(t(710, ly + 20, desc, 13.5, 400, GREY, 'start'))
    o.append(f'<rect x="170" y="604" width="660" height="30" fill="#f2f2f2"/>')
    o.append(t(500, 625, '적은 근육량, 스트레스와 긴장, 무리한 다이어트, 흡연이 손발을 더 차게 합니다', 14, 500, INK))
    o.append('</svg>')
    return '\n'.join(o)


files = {
    'digestive-map.svg': digestive_map(),
    'headache-types.svg': headache_types(),
    'sleep-types.svg': sleep_types(),
    'rhinitis-nose.svg': rhinitis_nose(),
    'cold-body.svg': cold_body(),
}
if __name__ == '__main__':
    for n, s in files.items():
        open(OUT + n, 'w', encoding='utf-8').write(s)
    print('ok', list(files))
