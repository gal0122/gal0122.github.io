"""새 칼럼 초안 36편(galch/drafts) -> 원장님 검토용 HTML 한 장 (그림 포함)."""
import html, os, re, sys, base64
import markdown
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, S)
import columns
OUT = f'{S}/prev/새칼럼_초안_36편.html'
posts = sorted(columns.load_posts(f'{S}/galch/drafts'), key=lambda p: (p['date'], p['src']))
STAR = {'beard-laser-hair-removal','philtrum-hair-removal','ultrasound-vs-rf-lifting','skin-booster-types','acne-scar-types','laser-toning-sessions',
        'traffic-headache-dizziness','traffic-at-fault','diet-herbal-side-effects','growth-plate-closure'}
NOTES = {
 'beard-laser-hair-removal': ['홈페이지 안내대로 "평균 12회 정도", "4주 간격 6회 = 1사이클"로 적었어요.'],
 'philtrum-hair-removal': ['인중 털에 755nm를 주로 고려한다고 적었어요. 실제 쓰시는 파장과 맞는지 봐 주세요.', '드물게 잔털이 굵어지는 현상(역설적 다모증)을 넣었어요. 가격·500원 체험은 넣지 않았어요.'],
 'armpit-hair-removal': ['굵은 털에 1064nm, 상태에 따라 755nm로 적었어요.'],
 'leg-hair-removal-timing': ['"여름 전에 끝내려면 겨울~초봄 시작"으로 적었어요.'],
 'folliculitis-after-hair-removal': [],
 'ultrasound-vs-rf-lifting': ['"어떤 게 더 좋다"는 비교 대신 고민에 따라 고르는 방식으로 적었어요.'],
 'lifting-interval': ['리니어펌 1달 간격 3회 → 6개월~1년, 볼뉴머 1회 → 6개월~1년 (홈페이지 기준).'],
 'lifting-volume-loss': ['리프팅 뒤 볼 꺼짐을 "드물지만 조심해야 하는 부작용"으로 솔직하게 적었어요. 표현이 괜찮은지 봐 주세요.'],
 'thread-lifting-duration': ['유지 기간은 숫자로 약속하지 않고 "1회 시술 후 1년 이후 상태를 다시 본다"로 적었어요.'],
 'jawline-double-chin': ['지방이 아주 많으면 리프팅만으로 한계가 있다고 적었어요.'],
 'skin-booster-types': ['5가지(PDRN·엑소좀, PLLA, 케라틴 약침, 알트코어, ECM 약침)를 "작용하는 곳" 기준으로 정리했어요.'],
 'pdrn-booster-sessions': ['라디쥬 3종 성분을 홈페이지 그대로 적었어요. 연어 알레르기 확인 문구를 넣었어요.'],
 'plla-booster': ['4~6주 간격 2~3회 (홈페이지 기준).'],
 'exosome-booster': ['엑소좀 연구가 "아직 쌓여 가는 단계"라고 적었어요. 과장 없이 쓰려고 넣은 문장이에요.'],
 'adult-jaw-acne': [],
 'acne-scar-types': ['아이스픽 → CO2 핀홀, 박스카 → 니들RF·CO2, 롤링 → 서브시전·스킨부스터 (홈페이지 기준). 시술 시간 30~40분, 붉음·미세 딱지 3~7일도 홈페이지 기준이에요.'],
 'enlarged-pores': ['제네시스 토닝 1~2주, 니들RF 4주 간격으로 적었어요.'],
 'laser-toning-sessions': ['기미 토닝 간격은 "상담 후 결정"으로 비워 두었어요. 정해진 간격이 있으면 알려 주세요.'],
 'back-acne': ['<b>등·가슴 여드름도 시술하시는지</b> 확인 부탁드려요. 지금 글은 "진찰 뒤 치료를 안내한다"로만 적고 구체적 시술은 넣지 않았어요.', '말라세지아 모낭염과 구분하는 내용을 넣었어요.'],
 'acne-red-marks': [],
 'traffic-headache-dizziness': ['위험 신호(구토 심해짐, 의식 소실, 힘 빠짐, 말 어눌함)는 큰 병원을 먼저 안내했어요.'],
 'traffic-at-fault': ['<b>보험 처리 방식은 일반적인 경우만</b> 적고, 매번 "담당 보험사에 확인"을 넣었어요. 과실 비율에 따른 세부 규정(경상환자 치료비 처리 등)은 바뀔 수 있어 숫자는 넣지 않았어요.'],
 'pedestrian-bicycle-accident': ['전동킥보드·무보험·뺑소니는 "보험사·관련 기관에 문의"로만 적었어요.'],
 'traffic-accident-pregnancy': ['<b>임신 중 침·추나·한약을 어디까지 하시는지</b> 꼭 봐 주세요. 지금은 "엎드리지 않는 자세, 자극 조절, 한약은 꼭 필요할 때만 신중히, 산부인과 확인이 먼저"로 적었어요.'],
 'traffic-herbal-medicine': ['"교통사고 한약은 자동차보험 진료 범위에서 처방할 수 있다"고 적었어요. 맞는지 확인 부탁드려요.'],
 'traffic-insomnia-anxiety': ['한 달 넘게 이어지거나 사고 장면이 계속 떠오르면 정신건강의학과 상담을 함께 권했어요.'],
 'forward-head-posture': [],
 'spinal-stenosis': ['치료는 척추 페이지 방법(침·약침, 추나, 한약, 물리치료)으로 적었어요.'],
 'trigger-finger': ['치료는 침·약침, 뜸, 물리치료로 적고, 손가락이 펴지지 않으면 정형외과를 안내했어요. 맞는지 봐 주세요.'],
 'chuna-insurance': ['<b>연간 횟수와 본인부담 비율은 숫자로 넣지 않았어요</b>(기준이 바뀔 수 있어서). 숫자를 넣고 싶으시면 지금 적용 기준을 알려 주세요.'],
 'diet-herbal-side-effects': ['부작용 표는 다이어트 페이지와 같게 적었어요. 약재 이름(마황 등)은 넣지 않았어요. 넣을지 알려 주세요.'],
 'postpartum-diet': ['<b>수유 중에는 다이어트 한약을 복용하지 않는다</b>(다이어트 페이지 기준)로 적었고, 시작 시기는 "진찰로 함께 정한다"로 두었어요.'],
 'diet-yoyo': [],
 'growth-plate-closure': ['성장판이 닫히는 시기는 "여아 대개 10대 중반, 남아 대개 10대 후반"처럼 대략으로만 적었어요.'],
 'kids-rhinitis-growth': ['"비염이 키를 직접 줄이거나 늘리는 것은 아니다"를 넣었어요.'],
 'irregular-periods': ['치료는 한약, 침·뜸으로 적었어요(여성 진료 페이지 기준). 석 달 넘게 없으면 산부인과 검사를 먼저 권했어요.'],
}
assert set(NOTES) == {p['slug'] for p in posts}, set(NOTES) ^ {p['slug'] for p in posts}

def kday(iso):
    y, m, d = iso.split('-'); return f'{int(m)}월 {int(d)}일'

def inline_img(m):
    f = f'{S}/galch/drafts/img/{m.group(1)}'
    return 'src="data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode() + '"'

css = re.search(r'<style>(.*?)</style>', open(f'{S}/prev/색소칼럼_초안_16편.html', encoding='utf-8').read(), re.S).group(1)
css += '.kw{display:inline-block;margin:0 6px 6px 0;padding:2px 10px;border-radius:999px;background:#e6efe9;color:#2f5241;font-size:13px;font-weight:700}\n'
css += '.cat{color:#4d554f;font-size:14px;margin:0 0 10px}.star{color:#a8452f;font-weight:800}\nfigure{margin:16px 0}figure img{max-width:100%}\n'
css += 'table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}td,th{border-bottom:1px solid #e2dccd;padding:8px;text-align:left;vertical-align:top}\n'
css += '@media (prefers-color-scheme: dark){.kw{background:#24382d;color:#8fc3a6}}\n'

toc, arts = [], []
for i, p in enumerate(posts, 1):
    st = '<span class="star">★ </span>' if p['slug'] in STAR else ''
    toc.append(f'<li><a href="#{p["slug"]}"><span class="d">{kday(p["date"])}</span>{st}{html.escape(p["title"])}</a></li>')
    body = markdown.markdown(p['body_md'], extensions=['tables'])
    body = re.sub(r'src="img/([^"]+)"', inline_img, body)
    faq = ''.join(f'<div class="qa"><strong>Q. {html.escape(q)}</strong><p>A. {html.escape(a)}</p></div>' for q, a in p['faq'])
    notes = NOTES[p['slug']] or ['따로 확인하실 부분은 없어요. 내용만 봐 주세요.']
    refs = ''.join(f'<li>{html.escape(n)}</li>' for n, u in p['refs'])
    arts.append(f'''<article id="{p['slug']}">
<p class="no">{i:02d} · {kday(p['date'])} 발행 예정 {st}</p>
<h2>{html.escape(p['title'])}</h2>
<p class="cat">분류: {html.escape(p['category'])} · 검색어: <span class="kw">{html.escape(p['keyword'])}</span></p>
<div class="check"><strong>원장님 확인</strong><ul>{''.join(f'<li>{n}</li>' for n in notes)}</ul></div>
<div class="sum"><strong>요약</strong>{html.escape(p['summary'])}</div>
<div class="body">{body}</div>
<h3>자주 묻는 질문</h3>{faq}
<p class="cat">참고 자료</p><ul>{refs}</ul>
<p class="top"><a href="#toc">↑ 목록으로</a></p>
</article>''')

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>새 칼럼 초안 36편</title>
<style>{css}</style></head><body><div class="wrap">
<h1>새 칼럼 초안 36편</h1>
<p class="lead">지금 예약된 칼럼이 끝나는 다음 날인 11월 11일부터 하루 3편씩(11월 22일까지) 올라가도록 날짜를 잡았어요. ★ 10편을 먼저 올리고, 나머지는 분류가 섞이도록 배치했어요. 원장님 확인 전에는 올라가지 않아요.</p>
<div class="check"><strong>공통 사항</strong><ul>
<li><b>그림:</b> 36편 모두 설명 그림 1장씩 넣었어요(인터넷 이미지 없이 직접 그린 그림). 글의 내용과 숫자만 썼어요.</li>
<li><b>근거:</b> 장비, 시술 횟수와 간격 같은 진료 내용은 홈페이지 진료 페이지에 적힌 내용을 기준으로 썼어요. 참고 자료는 국가건강정보포털, 한의표준임상진료지침, 학회지 논문으로 달았어요.</li>
<li><b>안전 문구:</b> 모든 글에 개인차 문구와 "먼저 큰 병원·다른 과 진료가 필요한 경우"를 넣었고, 최고·완치·보장·유일 같은 표현, 다른 병원과의 비교, 후기·전후 사진은 쓰지 않았어요.</li>
<li><b>발행자 정보:</b> 모든 칼럼(앞으로 올라갈 글 포함)의 구조화 데이터에 병원 이름·주소·로고가 자동으로 들어가요. 따로 하실 일은 없어요.</li>
<li><b>서로 연결:</b> 글 끝 "관련 진료·칼럼 안내"에 아직 올라가지 않은 칼럼 링크가 있으면, 그 글이 올라가는 날부터 자동으로 보이게 했어요.</li>
</ul></div>
<nav id="toc"><strong>목록 (발행 예정일)</strong><ol>{''.join(toc)}</ol></nav>
{''.join(arts)}
</div></body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print(OUT, len(page) // 1024, 'KB', len(posts))
