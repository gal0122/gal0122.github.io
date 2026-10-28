"""Create the FAQ board (Faq.dc.html) from the Schedule board's head/header/footer, and add FAQ to every board's menus."""
import re, json, html, glob, os
P = os.path.join(os.path.dirname(__file__), '..', 'galch', 'project')

FAQ = [
 ('info', 'INFO', '진료 안내', [
  ('토·일요일에도 진료하나요?', '네. 토·일요일 모두 오전 8시 30분부터 오후 2시까지 점심시간 없이 진료합니다. 평일은 오전 8시 30분부터 오후 6시 30분까지이며, 점심시간은 오후 1시부터 2시까지입니다.', 'Schedule.dc.html', '진료시간'),
  ('어떤 진료를 받을 수 있나요?', '피부미용(레이저제모·리프팅·색소·여드름·모공·스킨부스터), 교통사고 후유증, 척추·관절 통증, 내과 질환, 다이어트, 소아 성장, 여성 질환을 진료합니다.', 'About.dc.html', '병원 소개'),
  ('예약은 어떻게 하나요?', '네이버 톡톡 상담이나 전화(053-851-0122)로 예약하실 수 있습니다. 톡톡 상담은 진료시간 중 최대한 빠르게 답해 드립니다.', None, None),
  ('주차와 대중교통은 어떻게 되나요?', '건물 주차장과 이면도로에 주차하실 수 있습니다. 하양역(대구도시철도 1호선·대구선)에서 걸어서 약 10~15분이며, 버스는 하양한전 정류장에서 내리시면 됩니다.', 'Schedule.dc.html', '오시는 길'),
  ('시술 비용은 어디서 볼 수 있나요?', '피부미용 시술과 제모 비용은 가격표에 모두 공개되어 있으며, 표시된 금액은 부가세 포함입니다.', 'Price.dc.html', '가격표'),
 ]),
 ('skin', 'SKIN', '피부미용', [
  ('한의원에서도 레이저제모·리프팅 시술을 받을 수 있나요?', '네. 갈창림 한의원은 악센토N(레이저제모·색소), 큐마스터플러스(색소·토닝), 볼뉴머·리니어펌(리프팅), 실펌X 등의 장비를 보유하고 있으며, 화~일요일에 대표원장이 직접 시술합니다. 대표원장은 대한통합레이저의학회 교육위원으로 한의사 대상 레이저 교육 강의를 하고 있습니다. 시술 전 야누스프로 피부 분석과 진찰로 피부 상태를 확인한 뒤 시술 방법을 안내해 드립니다.', 'Equipment.dc.html', '보유장비'),
  ('시술 전에 피부 분석을 받을 수 있나요?', '네. 야누스프로 피부 분석과 진찰로 피부 상태를 먼저 확인한 뒤 맞는 시술을 상담해 드립니다.', 'Skin.dc.html', '피부미용'),
  ('남자 수염 레이저제모는 몇 번 받나요?', '755nm·1064nm 두 파장의 악센토N으로 시술하며, 평균 12회(4주 간격 6회씩 두 사이클) 정도 받습니다. 수염의 양이 많거나 굵으면 18~24회까지 진행하기도 하며, 털의 굵기와 양에 따라 개인차가 있습니다.', 'HairRemoval.dc.html', '레이저제모'),
  ('기미는 한 번에 없어지나요?', '기미는 자극에 예민해 낮은 세기로 여러 번 나누어 관리합니다. 다시 생길 수 있어 시술 후에도 자외선 차단이 중요합니다.', 'Pigment.dc.html', '기미·색소'),
  ('점빼기는 어떤 방법으로 하나요?', '색이 짙고 평평한 점은 아이스 점빼기로, 튀어나오거나 깊은 점과 쥐젖·편평사마귀는 유펄스 CO2로 제거합니다. 진료 후 점마다 알맞은 방법을 정합니다.', 'Mole.dc.html', '점빼기'),
  ('리프팅은 어떤 장비로 하나요?', '초음파(리니어펌)와 고주파(볼뉴머)를 얼굴 지방량과 피부 두께에 맞춰 부위별로 나눠 시술하는 디자인리프팅을 합니다. 결과에는 개인차가 있습니다.', 'DesignLifting.dc.html', '리프팅'),
 ]),
 ('traffic', 'TRAFFIC · PAIN', '교통사고 · 통증', [
  ('교통사고 치료에 본인부담금이 있나요?', '자동차보험으로 접수하면 진료비는 보험사가 지급하므로 본인부담금은 발생하지 않습니다. 보험사 접수번호만 있으면 진료받을 수 있습니다. 접수한 보험 종류와 보장 범위는 담당 보험사에 확인해 주세요.', 'Traffic.dc.html', '교통사고'),
  ('정형외과와 같이 다녀도 되나요?', '네. 같은 날 두 곳에서 진료받으셔도 되고, 같은 사고라면 같은 접수번호로 진료받을 수 있습니다.', 'TrafficProcess.dc.html', '교통사고 치료 과정'),
  ('추나 치료도 건강보험이 되나요?', '네, 추나요법은 건강보험이 적용됩니다. 적용 대상과 횟수, 본인 부담은 기준에 따라 달라지니 내원하시면 안내해 드립니다.', 'PainSpine.dc.html', '척추 질환'),
 ]),
 ('etc', 'DIET · KIDS · WOMEN', '다이어트 · 소아 · 여성', [
  ('한약 다이어트는 어떻게 진행하나요?', '진찰 후 체질에 맞춘 탕약을 처방합니다. 카카오톡으로 매일 식사 사진을 보내 주시면 원장이 직접 확인하고 답해 드립니다. 결과에는 개인차가 있습니다.', 'Diet.dc.html', '다이어트'),
  ('성장 치료는 언제 시작하면 좋나요?', '2차 성징이 나타나기 전, 초등학생 때 시작하시는 것이 좋습니다. 한의원에서는 엑스레이를 찍지 않아, 성장판 검사가 필요하면 검사할 수 있는 병원을 안내해 드립니다.', 'Growth.dc.html', '소아 성장'),
  ('생리통이나 갱년기 증상도 진료하나요?', '네. 생리통, 출산 후 산후풍, 갱년기 증상을 진료합니다. 산부인과 치료를 받고 계셔도 복용 중인 약을 알려 주시면 함께 관리할 수 있습니다.', 'Women.dc.html', '여성 질환'),
 ]),
]

SUM = '<summary style="display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; font-size: 17px; font-weight: 500">'
ICON = '<span class="faq-icon" aria-hidden="true" style="flex-shrink: 0; font-size: 24px; line-height: 1">+</span></summary>'


def main_html():
    e = html.escape
    tabs = ''.join(f'<a href="#faq-{k}" style="padding: 14px 0; border-bottom: 3px solid transparent; color: #5d655f; text-decoration: none">{name}</a>\n'
                   for k, _, name, _ in FAQ)
    secs = ''
    for k, eyebrow, name, items in FAQ:
        rows = ''
        for q, a, link, label in items:
            more = (f'\n<p style="margin: -8px 0 20px"><a class="faq-more" href="{link}" style="font-size: 14px; font-weight: 600; color: #2f5241; text-decoration: none">{e(label)} 자세히 보기 →</a></p>'
                    if link else '')
            rows += (f'<details style="border-bottom: 1px solid #e2dccd">\n{SUM}Q. {e(q)}{ICON}\n'
                     f'<p style="margin: 0 0 20px; color: #4d554f">{e(a)}</p>{more}\n</details>\n')
        secs += (f'<section id="faq-{k}" style="border-top: 1px solid #e2dccd; scroll-margin-top: 80px">\n'
                 f'<div class="faq" style="max-width: 1240px; margin: 0 auto; padding: 56px 24px; display: flex; flex-direction: column; gap: 24px">\n'
                 f'<div style="display: flex; flex-direction: column; gap: 8px">\n'
                 f'<p style="margin: 0; font-size: 14px; font-weight: 700; color: #7a6b42; letter-spacing: 0.04em">{eyebrow}</p>\n'
                 f'<h2 style="margin: 0; font-size: 28px">{name}</h2>\n</div>\n'
                 f'<div style="border-top: 1px solid #2f5241">\n{rows}</div>\n</div>\n</section>\n\n')
    hero = ('<section style="background: #f1ede3; border-bottom: 1px solid #e2dccd">\n'
            '<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 0; display: flex; flex-direction: column; gap: 12px">\n'
            '<p style="margin: 0; font-size: 14px; color: #5d655f">홈 &gt; 자주 묻는 질문</p>\n'
            '<h1 style="margin: 0; font-size: 40px; line-height: 1.3">자주 묻는 질문</h1>\n'
            '<p style="margin: 0; font-size: 17px; color: #4d554f">진료시간과 예약, 피부미용, 교통사고·통증, 다이어트·소아·여성 진료에 대해 자주 받는 질문을 모았습니다. 질문을 누르면 답이 열립니다.</p>\n'
            '<nav class="ptabs eq-track" aria-label="자주 묻는 질문 분류" style="display: flex; gap: 0 28px; margin-top: 16px; font-size: 15px; overflow-x: auto; white-space: nowrap">\n'
            + tabs + '</nav>\n</div>\n</section>\n\n')
    cta = ('<section style="border-top: 1px solid #e2dccd; background: #f1ede3">\n'
           '<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 72px; display: flex; flex-direction: column; align-items: flex-start; gap: 16px">\n'
           '<h2 style="margin: 0; font-size: 26px">찾는 답이 없으신가요?</h2>\n'
           '<p style="margin: 0; font-size: 16px; color: #4d554f">네이버 톡톡이나 전화로 편하게 물어봐 주세요. 톡톡 상담은 진료시간 중 최대한 빠르게 답해 드립니다.</p>\n'
           '<div style="display: flex; flex-wrap: wrap; gap: 10px">\n'
           '<a href="https://talk.naver.com/W4F2TI" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 999px; background: #2f5241; color: #ffffff; font-weight: 700; text-decoration: none">네이버 톡톡 상담</a>\n'
           '<a href="tel:053-851-0122" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 26px; border-radius: 999px; border: 1px solid #d7c9a7; background: #ffffff; color: #2f5241; font-weight: 700; text-decoration: none">전화 053-851-0122</a>\n'
           '</div>\n</div>\n</section>\n')
    return '<main>\n\n' + hero + secs + cta + '\n</main>'


def add_menu(s, current=False):
    cur = ' aria-current="page"' if current else ''
    s, n1 = re.subn(r'(<a href="Price\.dc\.html"[^>]*>가격표</a>\n)(</nav>)',
                    lambda m: m.group(1) + f'<a href="Faq.dc.html"{cur} style="text-decoration: none; padding: 10px 0{"; color: #2f5241" if current else ""}">FAQ</a>\n' + m.group(2), s, count=1)
    i = s.index('>전체 가격표</a>')
    j = s.index('</nav>', i)
    block = ('<div style="padding: 14px 0; border-top: 1px solid #ebe6da">\n'
             '<p style="margin: 0 0 6px; font-size: 13px; font-weight: 700; color: #7a6b42">FAQ</p>\n'
             '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 12px; font-size: 15px">\n'
             f'<a href="Faq.dc.html"{cur} style="padding: 8px 0; text-decoration: none{"; color: #2f5241; font-weight: 700" if current else ""}">자주 묻는 질문</a>\n'
             '</div>\n</div>\n')
    s = s[:j] + block + s[j:]
    assert n1 == 1
    return s


if __name__ == '__main__':
    for f in sorted(glob.glob(f'{P}/*.dc.html')):
        s = open(f, encoding='utf-8').read()
        if '>전체 가격표</a>' not in s or 'href="Faq.dc.html"' in s:
            continue
        open(f, 'w', encoding='utf-8').write(add_menu(s))
    src = open(f'{P}/Schedule.dc.html', encoding='utf-8').read()
    head, rest = src.split('<main>', 1)
    foot = rest.split('</main>', 1)[1]
    head = re.sub(r'<title>[^<]*</title>', '<title>자주 묻는 질문</title>', head, count=1)
    head = head.replace('<a href="Faq.dc.html" style="text-decoration: none; padding: 10px 0">FAQ</a>',
                        '<a href="Faq.dc.html" aria-current="page" style="text-decoration: none; padding: 10px 0; color: #2f5241">FAQ</a>')
    head = head.replace('<a href="Faq.dc.html" style="padding: 8px 0; text-decoration: none">자주 묻는 질문</a>',
                        '<a href="Faq.dc.html" aria-current="page" style="padding: 8px 0; text-decoration: none; color: #2f5241; font-weight: 700">자주 묻는 질문</a>')
    if '.ptabs a:hover' not in head:
        head = head.replace('</style>', '.ptabs a:hover{color:#2f5241;border-bottom-color:#d7c9a7!important}\n</style>', 1)
    open(f'{P}/Faq.dc.html', 'w', encoding='utf-8').write(head + main_html() + foot)
    c = json.load(open(f'{P}/canvas.json', encoding='utf-8'))
    if 'Faq.dc.html' not in c['order']:
        c['order'].insert(c['order'].index('Price.dc.html') + 1, 'Faq.dc.html')
        mx = max(b['x'] for b in c['boards'].values())
        c['boards']['Faq.dc.html'] = {'expand': 'fill', 'h': 3000, 'is_interactive': True, 'title': '30-1 자주 묻는 질문 (FAQ)', 'w': 1280, 'x': mx + 1360, 'y': 0}
        json.dump(c, open(f'{P}/canvas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok')
