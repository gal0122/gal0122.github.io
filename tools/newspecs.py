"""Explanatory pictures for the 36 new columns (원장 검토 전 초안). Same primitives as diagrams.py.
Usage: python3 newspecs.py <drafts_dir> <svg_out_dir> [insert]"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrams import (W, H, INK, SUB, GREEN, GOLD, LINE, CREAM, CARD, WARN, EPI, DER, FAT,
                      text, wrap, frame, card, cards, flow, callout, compare, timeline, skin, LESIONS)

BROWN = '#8a6d3b'




def bars(rows, hl, y=200):
    out = ''
    x0, bw = 360, 640
    for i, (lab, val, txt) in enumerate(rows):
        yy = y + i * 110
        on = i == hl
        t, _ = text(x0 - 30, yy + 44, lab, 26, GREEN if on else INK, 800, 'end')
        out += t
        out += f'<rect x="{x0}" y="{yy}" width="{bw}" height="64" rx="14" fill="#efe8d8"/>'
        out += f'<rect x="{x0}" y="{yy}" width="{bw * val / 100:.0f}" height="64" rx="14" fill="{GREEN if on else "#c9b98f"}"/>'
        t, _ = text(x0 + bw * val / 100 + 18, yy + 43, txt, 24, GREEN if on else SUB, 800)
        out += t
    _B[0] = y + (len(rows) - 1) * 110 + 64
    return out


# ---- auto-fitting layout: boxes shrink to their text, notes follow right below ----
import diagrams as D
_B = [170]


def _card_h(w, head, body, numbered=True):
    hx = 80 if numbered else 28
    yy = 58 + len(wrap(head, 25, w - hx - 20)) * 25 * 1.45
    yy = max(yy, 100) + 6
    for b in body:
        yy += len(wrap(b, 20, w - 56)) * 30 + 6
    return yy + 22


def callout(x, y, t, color=WARN, w=W - 120):
    y = _B[0] + 28
    lines = wrap(t, 21, w - 72)
    h = 30 + len(lines) * 31
    _B[0] = y + h
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fbf0ec" stroke="{color}" stroke-width="2"/>'
    out += f'<text x="{x + 24}" y="{y + 40}" font-size="22" font-weight="800" fill="{color}">!</text>'
    t_, _ = text(x + 48, y + 40, t, 21, color, 600, maxw=w - 72, lh=1.45)
    return out + t_


def gcallout(x, y, t, w=W - 120):
    y = _B[0] + 28
    lines = wrap(t, 21, w - 72)
    h = 30 + len(lines) * 31
    _B[0] = y + h
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#eef3ef" stroke="{GREEN}" stroke-width="2"/>'
    out += f'<circle cx="{x + 30}" cy="{y + 33}" r="7" fill="{GREEN}"/>'
    t_, _ = text(x + 48, y + 40, t, 21, GREEN, 600, maxw=w - 72, lh=1.45)
    return out + t_


def cards(items, y=170, h=None, gap=24, accent=GREEN, numbered=True):
    n = len(items)
    w = (W - 120 - gap * (n - 1)) / n
    h = max(_card_h(w, hd, bd, numbered) for hd, bd in items)
    _B[0] = y + h
    return D.cards(items, y, h, gap, accent, numbered)


def flow(items, y=180, h=None, note=None, accent=GREEN):
    n = len(items)
    w = (W - 120 - 56 * (n - 1)) / n
    h = max(_card_h(w, hd, bd) for hd, bd in items)
    _B[0] = y + h
    return D.flow(items, y, h, None, accent) + (callout(60, 0, note) if note else '')


def compare(left, right, y=170, h=None, note=None):
    w = (W - 120 - 32) / 2
    need = 0
    for head, sub, body, accent in (left, right):
        yy = 66 + len(wrap(head, 30, w - 64)) * 30 * 1.45
        if sub:
            yy += 2 + len(wrap(sub, 20, w - 64)) * 29
        yy += 14
        for b in body:
            yy += len(wrap(b, 21, w - 96)) * 31.5 + 10
        need = max(need, yy + 14)
    _B[0] = y + need
    return D.compare(left, right, y, need) + (callout(60, 0, note) if note else '')


def timeline(points, y=None, note=None, hl=None):
    y = 260
    _B[0] = y + 150
    return D.timeline(points, y, None, hl) + (callout(60, 0, note) if note else '')


LESIONS['none'] = lambda cx, top, ep, de: ''


def _booster(cx, top, ep, de):
    out = f'<line x1="{cx - 235}" y1="{top + ep - 8}" x2="{cx + 265}" y2="{top + ep - 8}" stroke="#c49a7c" stroke-width="10" opacity="0.6"/>'
    out += f'<text x="{cx - 225}" y="{top + ep - 22}" font-size="18" font-weight="700" fill="{GOLD}">기저층</text>'
    out += f'<circle cx="{cx + 120}" cy="{top + ep + 120}" r="34" fill="#f6efe2" stroke="#b9ab86" stroke-width="3"/>'
    out += f'<ellipse cx="{cx + 120}" cy="{top + ep + 120}" rx="14" ry="8" fill="#c9822f"/>'
    for n, (dx, dy) in enumerate([(-40, ep - 8), (-150, ep + 60), (-60, ep + 110), (-170, ep + 170), (120, ep + 120)], 1):
        out += f'<circle cx="{cx + dx}" cy="{top + dy}" r="19" fill="{GREEN}" stroke="#fff" stroke-width="3"/>'
        out += f'<text x="{cx + dx}" y="{top + dy + 7}" font-size="19" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>'
    return out


LESIONS['booster'] = _booster


def _scars(cx, top, ep, de):
    out = ''
    # icepick: narrow and deep, boxcar: flat bottom, rolling: wide wave
    out += f'<path d="M{cx - 222} {top - 1} L{cx - 200} {top + 120} L{cx - 178} {top - 1}z" fill="{CREAM}"/>'
    out += f'<path d="M{cx - 50} {top - 1} L{cx - 44} {top + 52} H{cx + 44} L{cx + 50} {top - 1}z" fill="{CREAM}"/>'
    out += f'<path d="M{cx + 120} {top - 1} Q{cx + 200} {top + 70} {cx + 280} {top - 1}z" fill="{CREAM}"/>'
    out += f'<path d="M{cx + 200} {top + 36} q-20 60 -60 120 M{cx + 200} {top + 36} q20 60 60 120" stroke="#b98d70" stroke-width="4" fill="none" stroke-dasharray="8 6"/>'
    for lx, lab in [(cx - 200, '아이스픽'), (cx, '박스카'), (cx + 200, '롤링')]:
        out += f'<text x="{lx}" y="{top - 16}" font-size="21" font-weight="800" fill="{GREEN}" text-anchor="middle">{lab}</text>'
    return out


LESIONS['scars'] = _scars


def head_posture():
    out = ''
    for i, (lab, fwd, txt) in enumerate([('바른 자세', 0, '귀가 어깨 위에 있어 목뼈가 무게를 받침'),
                                         ('거북목', 110, '머리가 앞으로 나올수록 뒷목·어깨 근육이 끌어당겨 버팀')]):
        gx = 60 + i * 556
        out += f'<rect x="{gx}" y="170" width="524" height="470" rx="24" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
        sx, sy = gx + 230, 472          # top of the shoulder line (side view, facing right)
        out += f'<path d="M{sx - 90} {sy + 98} L{sx - 70} {sy + 10} Q{sx} {sy - 20} {sx + 60} {sy + 10} L{sx + 80} {sy + 98}z" fill="#e8dfcf" stroke="#b9ab86" stroke-width="3"/>'
        hx, hy = sx + fwd, sy - 150
        out += f'<path d="M{sx} {sy - 4} Q{sx + fwd * 0.15} {sy - 70} {hx - 8} {hy + 58}" stroke="#ddc3aa" stroke-width="40" fill="none" stroke-linecap="round"/>'
        out += f'<circle cx="{hx}" cy="{hy}" r="70" fill="#f0dcc7" stroke="#c9a98f" stroke-width="3"/>'
        out += f'<path d="M{hx + 68} {hy - 4} l14 22 l-14 6" fill="#f0dcc7" stroke="#c9a98f" stroke-width="3"/>'
        out += f'<ellipse cx="{hx - 8}" cy="{hy + 6}" rx="10" ry="15" fill="#c9a98f"/>'
        out += f'<line x1="{sx}" y1="{hy - 60}" x2="{sx}" y2="{sy + 30}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="8 8"/>'
        if fwd:
            out += f'<path d="M{sx - 30} {sy - 30} Q{sx - 30} {hy + 60} {hx - 70} {hy + 40}" stroke="{WARN}" stroke-width="5" fill="none" stroke-dasharray="10 7"/>'
            out += f'<text x="{sx - 44}" y="{sy - 80}" font-size="18" font-weight="700" fill="{WARN}" text-anchor="end">긴장한</text>'
            out += f'<text x="{sx - 44}" y="{sy - 56}" font-size="18" font-weight="700" fill="{WARN}" text-anchor="end">뒷목 근육</text>'
        t, _ = text(gx + 262, 220, lab, 28, WARN if fwd else GREEN, 800, 'middle')
        out += t
        t, _ = text(gx + 262, 604, txt, 19, SUB, 600, 'middle', maxw=470)
        out += t
    return out


def canal():
    out = ''
    for i, (lab, narrow) in enumerate([('정상 척추관', False), ('좁아진 척추관', True)]):
        gx = 60 + i * 556
        cx = gx + 262
        out += f'<rect x="{gx}" y="170" width="524" height="420" rx="24" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
        out += f'<rect x="{cx - 110}" y="210" width="220" height="130" rx="50" fill="#e8dfcf" stroke="#b9ab86" stroke-width="3"/>'
        out += f'<text x="{cx}" y="282" font-size="21" font-weight="700" fill="{SUB}" text-anchor="middle">척추뼈</text>'
        out += f'<path d="M{cx - 120} 360 Q{cx - 140} 480 {cx} 500 Q{cx + 140} 480 {cx + 120} 360" fill="none" stroke="#b9ab86" stroke-width="30" stroke-linecap="round"/>'
        r = 26 if narrow else 52
        if narrow:
            out += f'<path d="M{cx - 80} 360 Q{cx} 420 {cx + 80} 360" fill="#e2c26e" stroke="#c9a54a" stroke-width="3"/>'
            out += f'<path d="M{cx - 70} 470 Q{cx} 430 {cx + 70} 470" fill="#e2c26e" stroke="#c9a54a" stroke-width="3"/>'
        out += f'<ellipse cx="{cx}" cy="425" rx="{r + 20}" ry="{r}" fill="none" stroke="{WARN if narrow else GREEN}" stroke-width="3" stroke-dasharray="6 5"/>'
        out += f'<circle cx="{cx}" cy="425" r="{r - 8 if narrow else 24}" fill="#c9822f"/>'
        t, _ = text(cx, 560, lab, 25, WARN if narrow else GREEN, 800, 'middle')
        out += t
    out += f'<text x="{60 + 556 + 262 + 150}" y="388" font-size="19" font-weight="700" fill="{GOLD}">두꺼워진</text>'
    out += f'<text x="{60 + 556 + 262 + 150}" y="414" font-size="19" font-weight="700" fill="{GOLD}">인대</text>'
    out += f'<text x="{60 + 262 + 150}" y="432" font-size="19" font-weight="700" fill="{GOLD}">신경</text>'
    return out


def trigger():
    out = ''
    for i, (lab, bad) in enumerate([('부드럽게 지나감', False), ('두꺼워져 걸림', True)]):
        gy = 180 + i * 220
        out += f'<rect x="60" y="{gy}" width="1080" height="190" rx="24" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
        out += f'<rect x="120" y="{gy + 80}" width="760" height="{34 if not bad else 34}" rx="17" fill="#e9d7b6" stroke="#c9a54a" stroke-width="2"/>'
        if bad:
            out += f'<ellipse cx="420" cy="{gy + 97}" rx="46" ry="34" fill="#e2c26e" stroke="#c9a54a" stroke-width="3"/>'
        px = 500
        out += f'<rect x="{px}" y="{gy + 58}" width="90" height="{78}" rx="14" fill="none" stroke="{WARN if bad else GREEN}" stroke-width="{10 if bad else 6}"/>'
        out += f'<text x="{px + 45}" y="{gy + 44}" font-size="19" font-weight="700" fill="{GOLD}" text-anchor="middle">힘줄 통로</text>'
        out += f'<text x="140" y="{gy + 44}" font-size="19" font-weight="700" fill="{GOLD}">손가락을 굽히는 힘줄</text>'
        t, _ = text(1100, gy + 106, lab, 26, WARN if bad else GREEN, 800, 'end')
        out += t
    return out


def pores():
    items = [('피지 모공', ['둥글고 넓게 열림', '코·이마, 지성 피부'], 'round'),
             ('늘어진 모공', ['아래로 길게 늘어짐', '볼, 나이가 들며'], 'drop'),
             ('흉터 모공', ['모양이 고르지 않게 패임', '여드름을 앓은 자리'], 'scar')]
    gap = 24
    w = (W - 120 - gap * 2) / 3
    out = ''
    for i, (head, body, kind) in enumerate(items):
        x = 60 + i * (w + gap)
        out += card(x, 170, w, 370, head, body, i + 1)
        cx, cy = x + w / 2, 430
        out += f'<rect x="{x + 30}" y="{cy - 70}" width="{w - 60}" height="140" rx="18" fill="{EPI}"/>'
        if kind == 'round':
            out += f'<circle cx="{cx}" cy="{cy}" r="34" fill="#c49a7c"/><circle cx="{cx}" cy="{cy}" r="18" fill="#8a5a3c"/>'
        elif kind == 'drop':
            out += f'<path d="M{cx} {cy - 44} C{cx + 34} {cy}, {cx + 26} {cy + 50}, {cx} {cy + 50} C{cx - 26} {cy + 50}, {cx - 34} {cy}, {cx} {cy - 44}z" fill="#c49a7c"/>'
        else:
            out += f'<path d="M{cx - 40} {cy - 20} l26 -16 l30 10 l22 -8 l6 34 l-18 30 l-34 6 l-30 -14z" fill="#c49a7c"/>'
    return out


def specs():
    S = []

    def add(slug, before, name, alt, cap, title, sub, body):
        S.append(dict(slug=slug, before=before, name=name, alt=alt, cap=cap, title=title, sub=sub, body=body))

    add('beard-laser-hair-removal', '## 진료실에서 자주 보는 경우', 'beard-sessions',
        '수염 레이저제모에 횟수가 많이 필요한 세 가지 이유 그림: 굵고 진한 털, 깊은 모낭, 빽빽한 털', '수염의 양이 많거나 굵으면 18~24회까지 진행하기도 하며, 털의 굵기와 양에 따라 개인차가 있습니다.',
        '수염은 왜 횟수가 많이 필요할까요?', '레이저제모는 털이 자라는 성장기 모낭에 가장 잘 작용합니다.',
        cards([('굵고 진한 털', ['모낭이 크고 재생력이 강해', '한두 번으로는 다시 자라기 쉬움']),
               ('깊은 모낭', ['열이 깊은 곳까지 닿도록', '파장과 조사 시간을 맞춤']),
               ('빽빽한 털', ['차례로 성장기에 들어오는', '모낭을 여러 번 나눠 만남'])], h=280)
        + gcallout(60, 480, '4주 간격 6회가 1사이클(약 6개월)입니다. 수염은 평균 12회 정도이며, 양이 많거나 굵으면 18~24회까지 진행하기도 합니다.'))

    add('traffic-headache-dizziness', '## 진료실에서 자주 보는 경우', 'traffic-headache',
        '교통사고 후 두통 비교 그림: 목 주변 긴장으로 생기는 흔한 두통과 바로 큰 병원에 가야 하는 두통', '머리를 부딪혔거나 위험 신호가 있다면 영상 검사가 가능한 병원에서 먼저 확인하세요.',
        '교통사고 후 두통, 먼저 이것부터 구분합니다', '머리와 목이 앞뒤로 흔들리면 목 주변 근육이 긴장해 두통과 어지럼이 생기기 쉽습니다.',
        compare(('흔한 사고 후 두통', '목·어깨 근육의 긴장', ['뒷머리·관자놀이가 조이듯 아픔', '어지럼, 귀울림, 눈의 피로', '며칠 뒤 시작되기도 함'], GREEN),
                ('바로 큰 병원으로', '이런 신호가 하나라도 있으면', ['두통과 구토가 점점 심해짐', '의식을 잃었던 경우', '힘이 빠지거나 말이 어눌해짐'], WARN), h=400))

    add('diet-herbal-side-effects', '## 처방 전에 꼭 알려 주세요', 'diet-safety-flow',
        '다이어트 한약 복용 과정의 안전 확인 그림: 처방 전 건강 상태 확인, 복용 중 점검과 처방 조절, 이상 시 바로 연락', '반응의 종류와 정도에는 개인차가 있어 복용하는 동안 컨디션을 보며 처방을 조절합니다.',
        '다이어트 한약, 이렇게 확인하며 복용합니다', '가슴 두근거림, 잠들기 어려움, 입마름·변비, 속 불편이 나타날 수 있습니다.',
        flow([('처방 전', ['고혈압·심장·갑상선', '복용 중인 약', '임신·수유 여부 확인']),
              ('복용 중', ['인바디로 근육·부종', '두근거림·잠·피로 확인', '처방과 복용 시간 조절']),
              ('이상이 있으면', ['참지 말고', '바로 연락'])], y=180, h=300,
             note='임신 중이거나 모유 수유 중에는 다이어트 한약을 복용하지 않습니다.'))

    add('growth-plate-closure', '## 사춘기가 빠르면 자랄 기간이 짧아질 수 있습니다', 'growth-plate-timeline',
        '성장판이 닫히기까지의 흐름 그림: 사춘기 전 꾸준히 자라고, 사춘기에 빠르게 자란 뒤 성장판이 닫힘', '시기는 아이마다 차이가 크며, 정확한 상태는 엑스레이로 뼈 나이를 확인해야 합니다.',
        '성장판이 닫히기까지', '사춘기에 한 번 빠르게 자란 뒤 성장판이 닫히면서 키 성장이 멈춥니다.',
        timeline([('사춘기 전', ['꾸준히 자라는 시기', '성장 상태 확인']), ('사춘기', ['한동안 빠르게 자람', '닫힐 시기도 다가옴']),
                  ('성장판 닫힘', ['여아 대개 10대 중반', '남아 대개 10대 후반'])], hl=0,
                 note='여자아이 만 8세 전, 남자아이 만 9세 전에 사춘기 신호가 나타나면 소아청소년과 검사를 받아 보세요.'))

    add('philtrum-hair-removal', '## 진료실에서 자주 보는 경우', 'philtrum-hair',
        '인중 레이저제모에서 살피는 세 가지 그림: 가늘고 옅은 털, 높은 성장기 비율, 잔털이 굵어지는 현상', '털 상태에 따라 횟수를 조정하며, 결과에는 개인차가 있습니다.',
        '인중 털은 섬세하게 다룹니다', '레이저제모는 털이 다시 자라는 힘을 약하게 해 털을 가늘고 적게 만드는 방법입니다.',
        cards([('가늘고 옅은 털', ['멜라닌이 적어', '파장·에너지를 정밀하게', '755nm를 주로 고려']),
               ('성장기 비율이 높음', ['얼굴 털은 한 시점에', '60~70%가 성장기']),
               ('잔털 변화에 주의', ['드물게 주변 잔털이', '굵어질 수 있어', '에너지를 세심하게 조절'])], h=300)
        + callout(60, 500, '털이 짧은 기간에 갑자기 굵고 많아졌거나 생리가 불규칙해졌다면 산부인과나 내과 진료를 먼저 받아 보세요.'))

    add('traffic-at-fault', '## 진료실에서 자주 보는 경우', 'traffic-fault-insurance',
        '교통사고 과실이 있을 때 보험 접수 그림: 상대 차량 보험과 내 차 보험의 일반적인 경우', '가입한 담보와 처리 방식은 사람마다 달라 접수 전에 담당 보험사에 확인해 주세요.',
        '과실이 있어도 치료는 받을 수 있습니다', '달라지는 것은 치료비를 어느 보험에서 처리하느냐입니다.',
        compare(('상대 차량 보험', '상대 과실이 있는 사고', ['상대 보험사에 접수', '접수번호로 진료 시작'], GREEN),
                ('내 차 보험', '내 과실이 크거나 단독 사고', ['자동차상해·자기신체사고 담보', '상대가 무보험이면 무보험차상해'], BROWN), h=330,
                note='과실 비율과 다친 정도에 따라 상대 보험과 내 보험이 나누어 처리하는 경우도 있습니다. 담당 보험사에 확인해 주세요.'))

    add('ultrasound-vs-rf-lifting', '## 진료실에서 자주 보는 경우', 'hifu-vs-rf',
        '초음파 리프팅과 고주파 리프팅 비교 그림: 정해진 깊이에 열을 모으는 방식과 넓고 고르게 퍼뜨리는 방식', '두 고민이 함께 있다면 복합 시술을 설계하며, 결과에는 개인차가 있습니다.',
        '열을 전달하는 방식이 다릅니다', '두 리프팅 모두 피부 속에 열을 만들어 콜라겐이 새로 만들어지도록 돕습니다.',
        compare(('초음파 · 리니어펌', '정해진 깊이에 한 점처럼 모음', ['2.0·3.0·4.5·6.0mm 깊이', '처진 윤곽과 턱선 정돈', '볼 처짐, 이중턱'], GREEN),
                ('고주파 · 볼뉴머', '넓고 고르게 퍼뜨림', ['진피와 피하조직을 넓게 데움', '피부 탄력과 타이트닝', '잔주름, 모공, 느슨한 피부'], BROWN), h=420))

    add('skin-booster-types', '## 진료실에서 자주 보는 경우', 'booster-layers',
        '스킨부스터 종류별로 주로 작용하는 곳 그림: 기저층의 케라틴 약침, 진피의 PDRN·엑소좀·PLLA·ECM, 세포의 알트코어', '야누스프로 분석과 상담으로 지금 피부에 필요한 것을 먼저 정합니다.',
        '스킨부스터, 작용하는 곳이 다릅니다', '이름은 같아도 성분마다 목적이 다릅니다.',
        skin('booster', [('① 기저층 · 케라틴 약침', '상피세포 정상화, 예민·트러블 피부'), ('② 진피 · PDRN·엑소좀', '재생과 콜라겐, 탄력·톤'),
                      ('③ 진피 · PLLA', '콜라겐 유도로 볼륨'), ('④ 진피 구조 · ECM 약침', '진피 골격 강화'), ('⑤ 세포 · 알트코어', '세포 에너지와 기능')], w=560))

    add('acne-scar-types', '## 치료는 이렇게 작용합니다', 'acne-scar-shapes',
        '여드름 흉터 모양 그림: 좁고 깊은 아이스픽, 바닥이 평평한 박스카, 넓게 물결치는 롤링', '한 얼굴에 여러 모양이 섞인 경우가 많아 조합해 치료하며, 개선 정도에는 개인차가 있습니다.',
        '여드름 흉터, 모양에 따라 치료가 다릅니다', '염증이 진피까지 번져 콜라겐이 손상되면 패인 흉터가 남습니다.',
        skin('scars', [('아이스픽', '좁고 깊게 패임 → CO2 핀홀'), ('박스카', '경계가 뚜렷하고 바닥이 평평함 → 니들RF·CO2 핀홀'),
                       ('롤링', '아래로 당기는 섬유띠 → 서브시전·스킨부스터')]))

    add('laser-toning-sessions', '## 목적에 따라 간격이 다릅니다', 'toning-why-many',
        '레이저토닝을 여러 번 받는 이유 그림: 강하게 한 번보다 낮은 세기로 여러 번 나누어 조금씩 옅게 함', '횟수는 몇 회 뒤 변화를 확인하며 조정하고, 결과에는 개인차가 있습니다.',
        '토닝은 약하게, 여러 번 나누어 합니다', '기미처럼 자극에 예민한 색소는 한 번에 강하게 치료하면 오히려 짙어질 수 있습니다.',
        compare(('강하게 한 번', '예민한 색소에는', ['자극이 커서', '오히려 짙어질 수 있음'], WARN),
                ('약하게 여러 번', '레이저토닝', ['낮은 세기로 얼굴 전체에 고르게', '조금씩 옅게', '경과를 보며 세기·횟수 조정'], GREEN), h=360)
        + gcallout(60, 560, '기미는 호르몬과 자외선의 영향으로 다시 생길 수 있어 자외선 차단을 함께 지켜야 합니다.'))

    add('armpit-hair-removal', '## 진료실에서 자주 보는 경우', 'armpit-growth-phase',
        '부위별 성장기 털 비율 그림: 얼굴 60~70%, 겨드랑이 약 30%, 팔·다리 약 20%', '나머지 털이 차례로 성장기에 들어올 때마다 다시 만나야 해 여러 번 시술합니다.',
        '한 시점에 성장기인 털의 비율', '레이저는 성장기 모낭에 가장 잘 작용합니다.',
        bars([('얼굴 (인중·턱)', 65, '60~70%'), ('겨드랑이', 30, '약 30%'), ('팔·다리', 20, '약 20%')], hl=1)
        + gcallout(60, 560, '기본 일정은 4주 간격 6회(1사이클, 약 6개월)이며, 털이 굵고 많으면 2사이클 이상이 필요할 수 있습니다.'))

    add('pedestrian-bicycle-accident', '## 접수는 이렇게 합니다', 'pedestrian-injury',
        '보행자·자전거 교통사고에서 다치기 쉬운 곳 그림: 부딪힌 곳, 넘어지며 짚은 손목·무릎·발목, 허리와 어깨', '골절이나 머리 부상이 의심되면 큰 병원 검사가 먼저입니다.',
        '보행자·자전거 사고는 여러 곳을 함께 다칩니다', '몸을 보호해 줄 차체가 없어 충격을 그대로 받습니다.',
        cards([('부딪힌 곳', ['차와 직접', '부딪힌 부위']), ('땅을 짚은 곳', ['넘어지며 짚은', '손목·무릎·발목']),
               ('함께 다치기 쉬운 곳', ['허리·어깨', '며칠 뒤 아파 오기도'])], h=260)
        + gcallout(60, 470, '사고를 낸 차량의 보험사에 접수해 접수번호를 받으면 자동차보험으로 진료받을 수 있습니다. 차와 관계없이 혼자 넘어진 경우는 대상이 아닐 수 있습니다.'))

    add('forward-head-posture', '## 집에서 확인해 보세요', 'forward-head',
        '바른 자세와 거북목 비교 그림: 머리가 어깨보다 앞으로 나오면 뒷목과 어깨 근육이 버텨야 하는 부담이 커짐', '자세 습관을 바꾸는 것이 기본이며, 굳은 근육과 균형은 치료로 함께 풀어 줍니다.',
        '머리가 앞으로 나올수록 목은 더 힘듭니다', '옆에서 봤을 때 귀가 어깨보다 앞으로 나와 있는 자세가 굳은 상태가 거북목입니다.',
        head_posture())

    add('postpartum-diet', '## 진료실에서 자주 보는 경우', 'postpartum-diet-timeline',
        '산후 다이어트 시기별 중심 그림: 출산 직후 회복, 수유 중 식사와 생활 관리, 수유가 끝난 뒤 본격적인 감량', '시작 시기는 출산 방법과 회복 정도, 수유 여부에 따라 진찰로 함께 정합니다.',
        '산후 다이어트, 시기에 따라 할 일이 다릅니다', '출산 후에는 붓기, 체력 저하, 부족한 잠, 불규칙한 식사가 겹칩니다.',
        timeline([('출산 직후', ['몸의 회복', '무리한 감량은 하지 않음']), ('수유 중', ['세 끼를 챙기고', '단 음식·야식 줄이기']),
                  ('수유가 끝난 뒤', ['몸 상태 확인 후', '맞춤 처방과 식단 관리'])], hl=2,
                 note='모유 수유 중에는 다이어트 한약을 복용하지 않습니다.'))

    add('kids-rhinitis-growth', '## 집에서 살펴보세요', 'rhinitis-growth-flow',
        '잦은 감기와 비염이 성장에 영향을 주는 흐름 그림: 코막힘과 잦은 감기, 잠과 식욕이 흔들림, 성장에 쓸 힘이 줄어듦', '비염이 키를 직접 줄이거나 늘리는 것은 아니며, 결과에는 개인차가 있습니다.',
        '자주 아프면 성장에 쓸 힘이 줄어듭니다', '성장호르몬은 깊이 잠든 동안 많이 나옵니다.',
        flow([('코막힘 · 잦은 감기', ['입을 벌리고 자거나', '자주 뒤척임']), ('잠과 식욕이 흔들림', ['자주 깨고', '입맛이 떨어짐']),
              ('성장에 쓸 힘이 줄어듦', ['회복에 먼저', '힘을 쓰게 됨'])], y=180, h=280)
        + gcallout(60, 500, '코골이가 심하고 자다가 숨을 멈추는 모습이 보이면 이비인후과 진료를 받아 보세요.'))

    add('leg-hair-removal-timing', '## 진료실에서 자주 보는 경우', 'leg-hair-timing',
        '팔·다리 레이저제모를 여름 전에 마치는 일정 그림: 가을~겨울에 시작해 적어도 6회, 약 6개월 뒤 여름 전에 1사이클 마무리', '굵고 진한 털은 2사이클 이상 필요할 수 있어 여유 있게 계획하세요.',
        '여름 전에 끝내려면 가을~겨울에 시작하세요', '팔·다리는 한 시점에 성장기인 털이 약 20%로 다른 부위보다 적습니다.',
        timeline([('가을~겨울', ['시작', '4주 간격']), ('봄', ['몇 회 뒤 털이', '가늘어지고 느리게 자람']), ('여름 전', ['적어도 6회', '약 6개월 뒤 1사이클 마무리'])], hl=0,
                 note='햇볕에 그을렸거나 태닝한 직후에는 화상과 색소침착 위험이 커져, 시술 전에 꼭 말씀해 주세요.'))

    add('traffic-accident-pregnancy', '## 진료실에서 자주 보는 경우', 'traffic-pregnancy-flow',
        '임신 중 교통사고 진료 순서 그림: 산부인과 확인, 임신 사실과 주수 알리기, 자세와 자극을 조절한 진료', '진찰 결과에 따라 치료보다 산부인과 경과 관찰이 먼저라고 안내드리기도 합니다.',
        '임신 중 교통사고, 이 순서로 확인하세요', '사고가 가벼워 보여도 아기와 엄마 상태를 먼저 확인하는 것이 우선입니다.',
        flow([('산부인과 확인', ['아프지 않아도', '먼저 확인']), ('임신 사실 알리기', ['주수와', '산부인과 진료 내용']),
              ('조절한 진료', ['엎드리지 않는 자세', '자극 조절, 한약은 신중히'])], y=180, h=280,
             note='배 통증, 출혈, 양수가 새는 느낌, 태동 감소가 있으면 바로 병원으로 가세요.'))

    add('spinal-stenosis', '## 허리디스크와는 어떻게 다를까요?', 'stenosis-canal',
        '척추관협착증 그림: 인대가 두꺼워지며 신경이 지나는 척추관이 좁아진 모습', '걸으면 다리가 저려 쉬었다 가야 하고, 허리를 숙이면 편해지는 것이 특징입니다.',
        '신경이 지나는 길이 좁아진 상태', '나이가 들며 인대가 두꺼워지고 뼈가 자라 척추관이 좁아지면 신경이 눌립니다.',
        canal())

    add('diet-yoyo', '## 체중보다 체성분을 봐야 합니다', 'yoyo-cycle',
        '요요가 오는 흐름 그림: 굶어서 감량하면 근육과 기초대사량이 함께 줄고, 예전처럼 먹으면 체중이 다시 오름', '감량 후에는 식사량을 천천히 늘리며 유지 기간을 둡니다. 결과에는 개인차가 있습니다.',
        '요요는 이렇게 옵니다', '빨리 빼려고 굶으면 몸은 지방과 함께 근육도 잃습니다.',
        flow([('굶어서 감량', ['짧은 기간에', '체중을 크게 줄임']), ('근육·기초대사량 감소', ['가만히 있어도 쓰는', '에너지가 줄어듦']),
              ('예전처럼 먹으면', ['체중이 쉽게', '다시 오름'])], y=180, h=280)
        + gcallout(60, 500, '감량 중에는 근육을 지키고, 목표 체중 뒤에는 요요 방지 한약과 함께 식사량을 조금씩 늘려 갑니다.'))

    add('irregular-periods', '## 산부인과 검사가 먼저 필요한 경우', 'irregular-periods-causes',
        '생리불순의 흔한 원인 그림: 생활의 변화, 체중 변화와 무리한 운동, 호르몬 이상과 임신', '원인에 따라 살피는 방법이 달라 검사가 먼저 필요한 경우를 확인합니다.',
        '생리불순, 원인부터 살핍니다', '생리 주기는 보통 21~35일 사이이며 사람마다 조금씩 다릅니다.',
        cards([('생활의 변화', ['큰 스트레스', '수면 부족, 생활 리듬 변화']), ('체중·운동', ['짧은 기간의 체중 변화', '갑자기 늘린 운동량']),
               ('호르몬 · 임신', ['다낭성난소증후군, 갑상선 질환', '늦어지면 임신 확인 먼저'])], h=280)
        + callout(60, 480, '석 달 넘게 생리가 없거나, 양이 갑자기 늘었거나, 생리 기간이 아닌데 출혈이 있으면 산부인과 검사를 먼저 받아 보세요.'))

    add('folliculitis-after-hair-removal', '## 진료실에서 자주 보는 경우', 'folliculitis-vs-reaction',
        '레이저제모 후 흔한 반응과 모낭염 비교 그림', '반응의 정도와 회복에는 개인차가 있습니다.',
        '흔한 반응일까요, 모낭염일까요?', '시술 직후 털구멍 주변이 붉고 붓는 것은 흔한 반응입니다.',
        compare(('시술 직후 반응', '레이저가 모낭에 닿았다는 신호', ['시술 직후 생김', '털구멍 주변이 고르게 붉고 부음', '하루 안에 가라앉음'], GREEN),
                ('모낭염', '털구멍에 생긴 염증', ['하루에서 며칠 뒤 생김', '털구멍을 따라 좁쌀·고름', '며칠 이어지거나 늘어날 수 있음'], BROWN), h=380,
                note='짜거나 긁지 마세요. 붉음과 통증이 점점 심해지거나 물집·진물이 생기면 바로 연락해 주세요.'))

    add('traffic-herbal-medicine', '## 진료실에서 자주 보는 경우', 'traffic-herbal-directions',
        '교통사고 뒤 증상에 따른 한약 처방 방향 그림: 어혈, 놀람과 불면, 소화불량, 굳은 근육', '같은 사고라도 증상이 달라 진찰 뒤 지금 상태에 맞게 처방합니다.',
        '증상에 따라 처방 방향이 다릅니다', '침·약침과 추나가 아픈 부위를 살핀다면, 한약은 몸 전체의 회복을 돕습니다.',
        cards([('어혈', ['멍, 붓기,', '찌르는 듯한 통증']), ('놀람 · 불면', ['깜짝 놀람, 불안,', '잠 못 듦']),
               ('소화불량', ['메스꺼움,', '입맛 없음']), ('굳은 근육', ['쑤시는 통증,', '근육과 순환'])], h=260)
        + gcallout(60, 470, '복용 중인 약과 임신 여부, 간·콩팥 질환을 미리 알려 주세요. 보험 처리 범위는 담당 보험사에 확인해 주세요.'))

    add('trigger-finger', '## 이런 증상이 있습니다', 'trigger-finger-pulley',
        '방아쇠수지 그림: 손가락을 굽히는 힘줄이 두꺼워져 좁은 통로를 지날 때 걸림', '손을 쉬게 하고 꽉 쥐는 동작을 줄이는 것이 기본입니다.',
        '힘줄이 통로를 지날 때 걸립니다', '손을 반복해서 많이 쓰면 힘줄과 통로가 붓고 두꺼워집니다.',
        trigger())

    add('lifting-interval', '## 왜 간격을 두고 받을까요?', 'lifting-schedule',
        '리니어펌 리프팅 권장 일정 그림: 1달 간격 3회 뒤 6개월~1년마다 유지', '볼뉴머는 1회 뒤 6개월~1년마다 받으며, 피부 상태에 따라 상담 때 조정합니다.',
        '리니어펌 권장 일정', '콜라겐이 차오르는 데는 수주에서 수개월이 걸립니다.',
        timeline([('1회', ['시작']), ('1달 뒤', ['2회']), ('2달 뒤', ['3회']), ('6개월~1년', ['유지 시술'])], hl=3,
                 note='같은 부위에 짧은 간격으로 강한 에너지를 반복하면 붉음, 화상, 볼 꺼짐 같은 부담이 커질 수 있습니다.'))

    add('traffic-insomnia-anxiety', '## 진료실에서 자주 보는 경우', 'traffic-mind',
        '교통사고 뒤 나타나기 쉬운 마음과 잠의 반응 그림: 불면, 깜짝 놀람, 운전 불안, 예민함', '대부분 시간이 지나며 줄어들지만, 통증과 겹치면 함께 살피는 것이 좋습니다.',
        '몸만 다치는 것이 아닙니다', '놀란 몸과 마음이 아직 가라앉지 않아 생기는 흔한 반응입니다.',
        cards([('잠', ['잠들기 어렵거나', '자주 깸']), ('놀람', ['작은 소리에도', '가슴이 두근거림']), ('운전 불안', ['차에 타기가', '두려움']),
               ('예민함', ['신경이 날카롭고', '집중이 안 됨'])], h=240)
        + gcallout(60, 450, '사고 장면이 계속 떠오르거나 한 달이 지나도 일상이 힘들면 정신건강의학과 상담을 함께 받아 보세요.'))

    add('chuna-insurance', '## 추나 전후 알아 두세요', 'chuna-steps',
        '추나요법 진행 순서 그림: 진찰, 물리치료, 침·약침, 추나', '건강보험 추나는 1년에 20회까지 받을 수 있고, 본인부담은 단순추나·복잡추나 등 추나 종류에 따라 다릅니다.',
        '추나요법은 이렇게 진행합니다', '근육을 먼저 충분히 풀고 상태에 맞게 강도를 정합니다.',
        flow([('진찰', ['아픈 곳과', '자세·균형 확인']), ('물리치료', ['굳은 근육을', '따뜻하게 풀기']), ('침·약침', ['통증 부위', '풀어 주기']),
              ('추나', ['척추와 골반', '바로잡기'])], y=180, h=260,
             note='추나 뒤 하루 이틀 가벼운 뻐근함이 있을 수 있습니다. 골다공증, 수술 이력, 임신 중이라면 미리 알려 주세요.'))

    add('lifting-volume-loss', '## 볼륨이 함께 줄었다면', 'lifting-zones',
        '리프팅 부위 나누기 그림: 볼륨을 지킬 앞볼·관자놀이와 정돈이 필요한 턱선·이중턱', '부위별로 깊이와 에너지를 다르게 쓰며, 결과에는 개인차가 있습니다.',
        '부위를 나눠 깊이와 에너지를 다르게 씁니다', '얼굴 살이 적은 분이 깊은 층까지 강하게 받으면 볼이 더 말라 보일 수 있습니다.',
        compare(('볼륨을 지킬 곳', '앞볼 · 관자놀이', ['깊은 카트리지를 줄이고', '에너지를 낮춤', '얇고 느슨하면 볼뉴머 고려'], GREEN),
                ('정돈이 필요한 곳', '턱선 · 이중턱', ['처진 윤곽을 정돈', '리니어펌을 부위에 맞게'], BROWN), h=380))

    add('thread-lifting-duration', '## 얼마나 유지될까요?', 'thread-types',
        '실리프팅 실의 종류 그림: 모노실, 코그실, 채움실·볼륨실의 역할', '실의 종류와 넣는 방향은 처짐 정도와 피부 두께, 지방 분포에 따라 정합니다.',
        '실의 종류에 따라 역할이 다릅니다', '개수보다 어디를 어느 방향으로 옮길지가 더 중요합니다.',
        cards([('모노실', ['표면이 매끈한 가는 실', '피부 탄력과 피부결']), ('코그실', ['표면에 미세한 돌기', '처진 조직을 옮기고 지지']),
               ('채움실 · 볼륨실', ['입체 구조', '꺼진 부위의 볼륨 보완'])], h=260)
        + gcallout(60, 470, '실은 시간이 지나며 녹아 없어지지만, 그 사이 실 주변에서 콜라겐이 새로 만들어지며 효과가 오래 유지될 수 있습니다. 유지 기간에는 개인차가 있습니다.'))

    add('jawline-double-chin', '## 진료실에서 자주 보는 경우', 'jawline-causes',
        '턱선이 흐려지는 세 가지 원인과 접근 그림: 처짐, 턱 아래 지방, 피부 탄력 저하', '대부분 세 가지가 섞여 있어, 어떤 원인이 큰지 먼저 살핍니다.',
        '턱선이 흐려지는 세 가지 이유', '원인에 따라 맞는 방법이 다릅니다.',
        cards([('처짐', ['조직이 아래로 내려옴', '→ 리니어펌 · 코그실']), ('턱 아래 지방', ['지방이 아주 많으면', '리프팅만으로는 한계,', '체중 관리 함께']),
               ('탄력 저하', ['피부가 얇고 느슨해짐', '→ 볼뉴머'])], h=300))

    add('pdrn-booster-sessions', '## 라디쥬, 세 가지 중에서 고릅니다', 'pdrn-schedule',
        'PDRN 스킨부스터 권장 일정 그림: 2~4주 간격 3~5회 뒤 유지 관리', '간격과 횟수는 피부 상태와 목적에 따라 조정하며, 결과에는 개인차가 있습니다.',
        'PDRN은 간격을 두고 쌓아 가는 시술입니다', '피부가 재생하고 콜라겐이 새로 만들어지는 데는 시간이 걸립니다.',
        timeline([('1회', ['2~4주 간격으로']), ('2~3회', ['피부결 변화를', '느끼는 경우가 많음']), ('3~5회', ['기본 일정', '마무리']), ('이후', ['피부 상태에 맞춰', '유지 관리'])], hl=2))

    add('plla-booster', '## 진료실에서 자주 보는 경우', 'plla-timeline',
        'PLLA 스킨부스터 시간에 따른 변화 그림: 시술 직후 잠시 차 보였다가 가라앉고, 1~2개월부터 콜라겐이 만들어지며, 3개월 이후 자리 잡음', '실제 변화는 시술 직후보다 그 뒤에 천천히 나타나며, 개인차가 있습니다.',
        'PLLA는 천천히 차오릅니다', '채워 넣는 시술이 아니라, 콜라겐 생성을 이끌어 차오르게 돕는 시술입니다.',
        timeline([('시술 직후', ['수분으로 잠시 차 보임', '며칠 안에 가라앉음']), ('약 1~2개월', ['콜라겐이', '만들어지기 시작']),
                  ('약 3개월 이후', ['볼륨과 탄력이', '서서히 자리 잡음'])], hl=2,
                 note='드물게 피부 아래 작은 알갱이가 만져질 수 있어, 오래가면 연락해 주세요.'))

    add('exosome-booster', '## 진료실에서 자주 보는 경우', 'radiju-original',
        '라디쥬 오리지널 구성 그림: PDRN, 엑소좀, 미백 성분에 HA 앰플을 함께 사용', '권장 주기는 2~4주 간격 3~5회이며, 피부 상태에 따라 조정합니다.',
        '엑소좀은 이렇게 함께 씁니다', '엑소좀만 단독으로 쓰기보다 PDRN과 함께 담은 라디쥬 오리지널을 사용합니다.',
        cards([('PDRN 1%', ['지친 피부의', '재생을 도움']), ('엑소좀 1%', ['세포가 신호를 전하는', '아주 작은 주머니']),
               ('미백 성분 + HA', ['칙칙한 톤과 잡티', '보습과 사용감'])], h=260)
        + gcallout(60, 470, '미용 분야의 엑소좀 연구는 아직 쌓여 가는 단계라, 근거가 비교적 많은 PDRN과 함께 쓰며 피부 변화를 보고 조정합니다.'))

    add('adult-jaw-acne', '## 진료실에서 자주 보는 경우', 'adult-acne-causes',
        '성인 턱 여드름에 영향을 주는 요인 그림: 호르몬 변화, 스트레스와 수면 부족, 마찰, 맞지 않는 화장품', '모공 막힘, 피지, 염증 가운데 무엇이 큰지에 따라 치료를 조합합니다.',
        '턱과 입 주변 여드름, 이런 요인이 겹칩니다', '성인 여드름은 턱과 입 주변, 턱선에 반복되는 경우가 많습니다.',
        cards([('호르몬', ['생리 전후로', '심해지기도']), ('스트레스 · 수면', ['피지와 피부 회복에', '영향']), ('마찰', ['마스크, 턱 괴기,', '휴대전화']),
               ('화장품', ['유분이 많거나', '모공을 막는 제품'])], h=240)
        + callout(60, 450, '생리가 불규칙하거나 털이 갑자기 늘었다면 호르몬 이상이 원인일 수 있어 산부인과나 내과 검사를 먼저 받아 보세요.'))

    add('enlarged-pores', '## 치료는 이렇게 작용합니다', 'pore-types',
        '모공이 넓어지는 세 가지 모양 그림: 둥글게 열린 피지 모공, 아래로 늘어진 모공, 고르지 않게 패인 흉터 모공', '원인이 다르면 맞는 시술도 달라 모공에 맞게 조합합니다.',
        '모공은 원인에 따라 모양이 다릅니다', '모공 입구는 깨끗하게, 모공을 받쳐 주는 진피는 탄탄하게 관리합니다.',
        pores())

    add('acne-red-marks', '## 진료실에서 자주 보는 경우', 'acne-mark-colors',
        '여드름 붉은 자국과 갈색 자국 비교 그림: 늘어난 모세혈관과 남은 멜라닌 색소', '자국의 색에 맞춰 토닝과 스킨부스터를 조합하며, 결과에는 개인차가 있습니다.',
        '붉은 자국과 갈색 자국', '자국은 피부 표면은 평평하고 색만 남은 상태입니다.',
        compare(('붉은 자국', '염증 뒤 늘어난 모세혈관', ['눌러 보면 잠시 옅어짐', '혈관 토닝 + 스킨부스터'], '#b5424f'),
                ('갈색 자국', '염증 뒤 남은 멜라닌 색소', ['눌러도 색이 그대로', '색소 토닝 + 스킨부스터'], BROWN), h=330)
        + gcallout(60, 530, '회복 중인 피부는 자외선에 예민해 자국이 더 짙어질 수 있어 자외선 차단을 함께 지켜 주세요.'))
    return S


def write_svgs(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for s in specs():
        open(os.path.join(out_dir, s['name'] + '.svg'), 'w', encoding='utf-8').write(frame(s['title'], s['sub'], s['body']))


def add_figures(col_dir):
    for s in specs():
        fs = glob.glob(os.path.join(col_dir, f'*-{s["slug"]}.md'))
        assert len(fs) == 1, s['slug']
        md = open(fs[0], encoding='utf-8').read()
        if f'img/{s["name"]}.webp' in md:
            continue
        assert md.count(s['before']) == 1, (s['slug'], s['before'])
        fig = (f'<figure style="margin: 8px 0 24px">\n<img src="img/{s["name"]}.webp" alt="{s["alt"]}" '
               f'style="display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid #e2dccd">\n'
               f'<figcaption style="margin-top: 8px; font-size: 14px; color: #5d655f">{s["cap"]} (갈창림 한의원 제작 설명 그림)</figcaption>\n</figure>\n\n')
        open(fs[0], 'w', encoding='utf-8').write(md.replace(s['before'], fig + s['before'], 1))


if __name__ == '__main__':
    write_svgs(sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3] == 'insert':
        add_figures(sys.argv[1])
