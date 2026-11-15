import re, sys
F = '/tmp/bt/galch/project/Faq.dc.html'
s = open(F).read()

SUM = '<summary style="display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; font-size: 17px; font-weight: 500">'
ICON = '<span class="faq-icon" aria-hidden="true" style="flex-shrink: 0; font-size: 24px; line-height: 1">+</span></summary>'
MORE = '<p style="margin: -8px 0 20px"><a class="faq-more" href="%s"%s style="font-size: 14px; font-weight: 600; color: #2f5241; text-decoration: none">%s →</a></p>\n'

# answers already on the page, by question (kept word for word unless replaced below)
old = {}
for m in re.finditer(r'<details style="border-bottom: 1px solid #e2dccd">\n<summary[^>]*>Q\. (.*?)<span class="faq-icon".*?</summary>\n<p style="margin: 0 0 20px; color: #4d554f">(.*?)</p>\n(?:<p style="margin: -8px 0 20px"><a class="faq-more" href="([^"]*)"[^>]*>(.*?) →</a></p>\n)?</details>', s, re.S):
    old[m.group(1)] = (m.group(2), m.group(3), m.group(4))

def D(q, a=None, href=None, label=None):
    if a is None:
        a, href, label = old[q]
    x = '<details style="border-bottom: 1px solid #e2dccd">\n' + SUM + 'Q. ' + q + ICON + '\n<p style="margin: 0 0 20px; color: #4d554f">' + a + '</p>\n'
    if href:
        ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
        x += MORE % (href, ext, label)
    return x + '</details>\n'

EV = '<span data-event-until="2026-12-31">%s</span>'   # wording tied to the unlimited-rate event: remove after 2026-12-31

SECTIONS = [
 ('faq-info', 'INFO', '진료 안내', [
  D('토·일요일에도 진료하나요?'),
  D('월요일에도 피부 시술을 받을 수 있나요?'),
  D('공휴일에도 진료하나요?',
    '공휴일은 휴진합니다. 2026년 12월에는 13일(일)에 미용 세미나 참석으로, 25일(금) 성탄절에 휴진합니다. 그 밖에 따로 쉬는 날은 진료시간 페이지의 이달의 진료 일정과 홈페이지 공지에서 확인하실 수 있습니다.',
    'Schedule.dc.html', '이달의 진료 일정 자세히 보기'),
  D('예약은 어떻게 하나요?',
    '네이버 예약에서 원하는 날짜와 시간을 바로 예약하실 수 있습니다. 네이버 톡톡 상담이나 전화(053-851-0122)로도 예약하실 수 있으며, 톡톡 상담은 진료시간 중 최대한 빠르게 답해 드립니다.',
    'https://m.booking.naver.com/booking/16/bizes/1769133', '네이버 예약 바로 가기'),
  D('한의원은 어디에 있나요?',
    '경상북도 경산시 하양읍 동서2길 43, 3층에 있습니다. 하양역에서 걸어서 약 10~15분 거리이며, 하양·진량·와촌·압량 등 경산 지역과 영천 금호, 대구 동구(안심·반야월)에서도 찾아오십니다.',
    'Schedule.dc.html', '오시는 길 자세히 보기'),
  D('주차와 대중교통은 어떻게 되나요?'),
  D('어떤 진료를 받을 수 있나요?'),
  D('시술 비용은 어디서 볼 수 있나요?'),
 ]),
 ('faq-skin', 'SKIN', '피부미용 공통', [
  D('한의원에서도 레이저제모·리프팅 시술을 받을 수 있나요?',
    '네. 갈창림 한의원은 악센토N(레이저제모·색소), 큐마스터플러스(색소·토닝), 유펄스(점·쥐젖·편평사마귀), 볼뉴머·리니어펌(리프팅), 실펌X 등의 장비를 보유하고 있으며, 화~일요일에 대표원장이 직접 시술합니다. 대표원장은 대한통합레이저의학회 교육위원으로 한의사 대상 레이저 교육 강의를 하고 있습니다. 시술 전 야누스프로 피부 분석과 진찰로 피부 상태를 확인한 뒤 시술 방법을 안내해 드립니다.',
    'Equipment.dc.html', '보유장비 자세히 보기'),
  D('시술 전에 피부 분석을 받을 수 있나요?'),
 ]),
 ('faq-hair', 'HAIR REMOVAL', '레이저제모', [
  D('레이저제모 비용은 얼마인가요?',
    '1회 기준 여성 인중·겨드랑이 11,000원, 남성 겨드랑이 22,000원, 남성 얼굴 전체(수염) 88,000원이며, 5회권은 각각 44,000원, 88,000원, 264,000원입니다(부가세 포함). '
    + EV % '2026년 12월 31일까지는 1년 무제한·평생 무제한 요금도 운영합니다. 여성 인중·겨드랑이는 1년 77,000원·평생 115,500원, 남성 얼굴 전체는 1년 462,000원·평생 693,000원이며, 시술 간격은 4주 이상입니다. '
    + '인중 제모가 처음이신 분은 첫 체험 1회를 500원에 받으실 수 있습니다(인중만, 1인 1회). 다른 부위의 금액은 가격표에서 확인하실 수 있습니다.',
    'Price.dc.html#price-hair', '제모 부위별 가격표 자세히 보기'),
  D('5회권과 무제한 요금 중 무엇이 유리한가요?',
    EV % '필요한 횟수에 따라 다릅니다. 팔다리나 겨드랑이처럼 6회 안팎으로 마무리될 가능성이 높은 부위는 5회권이, 남성 수염처럼 12회 이상이 예상되는 부위는 1년·평생 무제한 요금이 유리한 경우가 많습니다. 5회권을 쓰다가 무제한 요금으로 바꿀 수는 없으니, 처음 상담 때 예상 횟수를 듣고 정하시길 권합니다.',
    'column-laser-hair-removal-cost.html', '제모 비용 계산 예시 자세히 보기'),
  D('레이저제모는 몇 번 받아야 하나요?',
    '레이저는 자라고 있는 털에만 작용해 한 번에 끝나지 않습니다. 4주 간격 6회, 약 6개월을 1사이클로 안내하며, 가늘고 숱이 적은 털은 1사이클로도 변화를 느끼시는 경우가 있고 굵고 진한 털은 2~4사이클이 필요한 경우가 많습니다. 색이 아주 옅은 솜털이나 흰 털은 효과가 제한적일 수 있으며, 결과에는 개인차가 있습니다.',
    'column-laser-hair-removal-sessions.html', '제모 횟수 자세히 보기'),
  D('남자 수염 레이저제모는 몇 번 받나요?'),
  D('레이저제모는 아픈가요? 마취를 하나요?',
    '대부분 마취 없이 받으십니다. 조사 전후로 냉각 가스를 뿌려 피부 표면을 보호하며, 부위와 개인에 따라 느끼는 정도가 달라 통증이 걱정되시면 마취 크림을 바른 뒤 시술합니다.',
    'HairRemoval.dc.html', '레이저제모 자세히 보기'),
  D('제모 기간에 면도나 왁싱을 해도 되나요?',
    '시술 직후 3일은 면도를 쉬어 주시고, 그 뒤로는 면도로 정리하셔도 괜찮습니다. 다만 털을 뽑거나 왁싱하면 레이저가 작용해야 할 모낭까지 함께 빠지므로 시술 기간에는 피해 주세요.',
    'HairRemoval.dc.html', '제모 전후 주의사항 자세히 보기'),
 ]),
 ('faq-pigment', 'PIGMENT · MOLE', '색소 · 토닝 · 점', [
  D('기미는 한 번에 없어지나요?'),
  D('레이저토닝 가격과 횟수는 어떻게 되나요?',
    '토닝은 1회 88,000원, 10회 550,000원이며(부가세 포함), 트리플토닝과 제네시스토닝이 포함되어 있습니다. 횟수는 색소 종류에 따라 달라, 주근깨나 흑자는 비교적 적은 횟수로 변화를 보는 경우가 많고 기미는 2주 간격으로 최소 10~20회를 안내해 드립니다. 야누스프로 촬영과 진찰 후 계획을 세우며, 결과에는 개인차가 있습니다.',
    'column-laser-toning-price.html', '토닝 가격과 횟수 자세히 보기'),
  D('GD토닝은 일반 토닝과 무엇이 다른가요?',
    '골드 입자와 다이아몬드 결정 성분이 담긴 앰플을 먼저 바른 뒤 큐마스터플러스로 토닝합니다. 토닝과 각질 정리를 한 번에 받는 방식으로, 피부결이 거칠고 피부톤이 칙칙한 분께 권하며 보통 2~4주 간격으로 진행합니다. 비용은 1회 165,000원입니다(부가세 포함).',
    'Peeling.dc.html', 'GD토닝 자세히 보기'),
  D('점빼기는 어떤 방법으로 하나요?',
    '색이 짙고 평평한 점은 피부를 깎지 않는 아이스 점빼기로, 튀어나오거나 깊은 점과 쥐젖·편평사마귀는 유펄스로 제거합니다. 유펄스는 최대 출력 100W의 울트라펄스 CO2 레이저로, 짧은 순간에 에너지를 전달해 주변 피부의 열 손상을 줄입니다. 비용은 2mm 이하 1개 5,000원이며, 2mm 이상은 상담 후 결정됩니다.',
    'Mole.dc.html', '점빼기 자세히 보기'),
  D('편평사마귀(편사)나 쥐젖이 여러 개인데 한 번에 제거할 수 있나요?',
    '네, 개수가 많아도 보이는 병변은 한 번에 꼼꼼히 제거합니다. 다만 편평사마귀는 바이러스로 생기는 병변이라 새로 생기거나 번질 수 있어 경과를 함께 확인하며, 시술 부위를 긁거나 면도로 자극하지 않는 것이 좋습니다.',
    'Mole.dc.html', '쥐젖·편평사마귀 자세히 보기'),
  D('점 뺀 자리에 갈색 자국이 남나요?'),
 ]),
 ('faq-acne', 'ACNE · SCAR · PORE', '여드름 · 흉터 · 모공', [
  D('여드름 치료는 어떻게 하나요?',
    '여드름의 종류와 피지 상태에 따라 압출, 필링, ALA-PDT, 골드PTT, PDRN을 조합합니다. 붉게 곪는 염증성 여드름이 많으면 ALA-PDT를, 피지가 많고 여드름이 반복되면 골드PTT를 먼저 고려하며, 보통 1주 간격으로 여러 번 받으면서 경과를 확인합니다. 여드름은 다시 생길 수 있어 세안과 생활 관리 방법도 함께 안내해 드립니다.',
    'Acne.dc.html', '여드름 자세히 보기'),
  D('여드름 흉터는 어떻게 치료하나요?'),
  D('넓어진 모공은 어떻게 관리하나요?',
    '모공은 피지가 많아 넓어진 경우, 탄력이 줄어 늘어진 경우, 여드름 뒤 패인 경우에 따라 방법이 다릅니다. 야누스프로로 모공과 피부결을 확인한 뒤 니들RF(실펌X), 제네시스토닝, 스킨부스터, 필링 가운데 모공에 맞는 시술을 계획합니다.',
    'Pore.dc.html', '모공 자세히 보기'),
  D('블랙헤드와 피지가 많은데 어떤 관리를 받나요?'),
 ]),
 ('faq-lifting', 'LIFTING · EYE · BOOSTER', '리프팅 · 눈밑지방 · 스킨부스터', [
  D('리프팅은 어떤 장비로 하나요?'),
  D('실리프팅도 받을 수 있나요?',
    '네. 처짐 정도에 맞춰 실의 종류와 위치를 정하는 맞춤형 실리프팅을 합니다. 피부 탄력 저하는 초음파·고주파 리프팅으로, 뚜렷한 조직 처짐은 실리프팅으로 나누어 관리하는 경우가 많으며, 유지 기간에는 개인차가 있습니다.',
    'ThreadLifting.dc.html', '실리프팅 자세히 보기'),
  D('눈밑지방, 수술 없이 관리할 수 있나요?',
    'DA채움 패치에 1064nm 큐스위치 레이저를 조사해 만든 레이저 유도 충격파로, 절개 없이 지방을 받치는 조직을 자극해 볼록한 경계를 완만하게 관리합니다. 지방을 빼거나 옮기는 시술은 아니어서 지방 돌출이 심하면 한계가 있으며, 2주 간격 3회를 기본으로 합니다. 비용은 패치 2장 기준 1회 330,000원, 3회 880,000원이며(부가세 포함), 결과에는 개인차가 있습니다.',
    'Shockwave.dc.html', '눈밑지방·흉터 충격파 자세히 보기'),
  D('스킨부스터는 어떤 종류가 있나요?',
    '피부 속에 필요한 성분을 직접 채워 넣는 시술로, PDRN·엑소좀(라디쥬), PLLA, 케라틴, 알트코어, ECM 다섯 가지가 있습니다. 야누스프로 분석으로 수분, 탄력, 피부결 상태를 확인한 뒤 피부에 맞는 성분을 고릅니다.',
    'Skin.dc.html#booster', '스킨부스터 자세히 보기'),
 ]),
 ('faq-traffic', 'TRAFFIC · PAIN', '교통사고 · 통증', [
  D('교통사고 치료에 본인부담금이 있나요?'),
  D('교통사고 진료를 받으러 갈 때 무엇을 챙겨야 하나요?'),
  D('사고 후 며칠이 지나서 아프기 시작했는데 치료받을 수 있나요?',
    '네. 사고 직후에는 긴장 때문에 통증을 잘 느끼지 못하다가 며칠 뒤 나타나는 경우가 많습니다. 통증이 시작되었다면 미루지 말고 진료를 받아 보세요.',
    'Traffic.dc.html', '교통사고 후유증 자세히 보기'),
  D('교통사고 치료도 토·일요일에 받을 수 있나요?',
    '네. 토·일요일은 오전 8시 30분부터 오후 2시까지 점심시간 없이 진료하며, 자동차보험 진료도 똑같이 받으실 수 있습니다. 공휴일은 휴진합니다.',
    'Traffic.dc.html', '교통사고 진료 자세히 보기'),
  D('정형외과와 같이 다녀도 되나요?'),
  D('추나 치료도 건강보험이 되나요?'),
 ]),
 ('faq-etc', 'DIET · KIDS · WOMEN', '다이어트 · 소아 · 여성', [
  D('한약 다이어트는 어떻게 진행하나요?'),
  D('성장 치료는 언제 시작하면 좋나요?'),
  D('생리통이나 갱년기 증상도 진료하나요?'),
 ]),
]

def section(sid, eyebrow, title, items):
    return ('<section id="%s" style="border-top: 1px solid #e2dccd; scroll-margin-top: 80px">\n'
            '<div class="faq" style="max-width: 1240px; margin: 0 auto; padding: 56px 24px; display: flex; flex-direction: column; gap: 24px">\n'
            '<div style="display: flex; flex-direction: column; gap: 8px">\n'
            '<p style="margin: 0; font-size: 14px; font-weight: 700; color: #7a6b42; letter-spacing: 0.04em">%s</p>\n'
            '<h2 style="margin: 0; font-size: 28px">%s</h2>\n</div>\n<div style="border-top: 1px solid #2f5241">\n%s</div>\n</div>\n</section>\n') % (sid, eyebrow, title, ''.join(items))

a = s.index('<section id="faq-info"')
b = s.index('<section style="border-top: 1px solid #e2dccd; background: #f1ede3">', a)
body = '\n'.join(section(*x) for x in SECTIONS) + '\n'
s = s[:a] + body + s[b:]

TABS = [('faq-info', '진료 안내'), ('faq-skin', '피부 공통'), ('faq-hair', '제모'), ('faq-pigment', '색소 · 점'), ('faq-acne', '여드름 · 모공'),
        ('faq-lifting', '리프팅 · 눈밑지방'), ('faq-traffic', '교통사고 · 통증'), ('faq-etc', '다이어트 · 소아 · 여성')]
n1 = s.index('<nav class="ptabs eq-track" aria-label="자주 묻는 질문 분류"'); n2 = s.index('</nav>', n1)
head = s[n1:s.index('>', n1) + 1]
s = s[:n1] + head + '\n' + ''.join('<a href="#%s" style="padding: 14px 0; border-bottom: 3px solid transparent; color: #5d655f; text-decoration: none">%s</a>\n' % t for t in TABS) + s[n2:]
intro_old = '진료시간과 예약, 피부미용, 교통사고·통증, 다이어트·소아·여성 진료에 대해 자주 받는 질문을 모았습니다. 질문을 누르면 답이 열립니다.'
assert intro_old in s
s = s.replace(intro_old, '진료시간과 예약, 레이저제모·색소·점빼기·여드름·리프팅 같은 피부미용, 교통사고·통증, 다이어트·소아·여성 진료에 대해 자주 받는 질문을 모았습니다. 질문을 누르면 답이 열립니다.')
open(F, 'w').write(s)
print('questions', s.count('<details style="border-bottom'), 'kept-from-page', len(old))
