# 교통사고 3개 페이지 상단: 접수 방법과 진료시간을 한 줄로 (본인부담 금액은 강조하지 않음 — 자주 묻는 질문에 사실대로만)
import re, os
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galch', 'project')
CHIP = 'flex: 0 0 auto; display: inline-flex; align-items: center; min-height: 36px; padding: 0 14px; border-radius: 999px; background: #ffffff; border: 1px solid #e2dccd; color: #24302a'
STRIP = ('<ul data-traffic-strip="true" class="eq-track" aria-label="교통사고 진료 안내" style="list-style: none; margin: 12px 0 0; padding: 0 0 4px; display: flex; gap: 8px; overflow-x: auto; white-space: nowrap; font-size: 14px">\n'
         f'<li style="{CHIP.replace("background: #ffffff; border: 1px solid #e2dccd; color: #24302a", "background: #2f5241; border: 1px solid #2f5241; color: #ffffff")}; font-weight: 700">자동차보험 진료</li>\n'
         f'<li style="{CHIP}">보험사 접수번호만 있으면 접수</li>\n'
         f'<li style="{CHIP}">평일 08:30 – 18:30</li>\n'
         f'<li style="{CHIP}">토·일 08:30 – 14:00</li>\n'
         f'<li style="{CHIP}">주차 가능</li>\n'
         f'<li style="{CHIP}"><a href="tel:053-851-0122" style="color: #2f5241; font-weight: 700; text-decoration: none">전화 053-851-0122</a></li>\n'
         '</ul>\n')
for b in ['Traffic', 'TrafficProcess', 'TrafficTreat']:
    p = f'{G}/{b}.dc.html'
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'<ul data-traffic-strip="true".*?</ul>\n', '', t, flags=re.S)
    i = t.index('<nav aria-label="교통사고 하위 메뉴"')
    t = t[:i] + STRIP + t[i:]
    open(p, 'w', encoding='utf-8').write(t)
    print(b)
