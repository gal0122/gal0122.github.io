"""질환 칼럼 초안(galch/drafts) -> 원장님 검토용 HTML 한 장."""
import html, os, re, sys
import markdown
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import columns

S = os.path.dirname(os.path.abspath(__file__))
OUT = f'{S}/prev/질환칼럼_초안_29편.html'
posts = sorted(columns.load_posts(f'{S}/galch/drafts'), key=lambda p: p['date'])

PAIN = '치료 방법은 원장님이 따로 정해 주시지 않아서, 홈페이지 척추·관절 진료 페이지에 있는 방법(물리치료, 침·약침, 뜸·부항, 추나, 한약)으로 적었어요. 빼거나 더할 것이 있으면 알려 주세요.'
NOTES = {
    'low-back-pain': [PAIN, '물리치료는 "핫팩과 ICT, 필요하면 견인기"로 적었어요. 실제 쓰는 장비와 맞는지 봐 주세요.'],
    'lumbar-disc': [PAIN, '"견인기로 허리뼈 사이 압박을 줄인다"고 적었어요. 견인 치료를 하시는지 확인 부탁드려요.'],
    'neck-disc': [PAIN, '"견인기로 목뼈 사이 압박을 줄인다"고 적었어요. 목 견인을 하시는지 확인 부탁드려요.'],
    'neck-shoulder-stiffness': [PAIN, '검색어는 "경산 담결림"으로 잡았어요.'],
    'frozen-shoulder': [PAIN],
    'shoulder-pain': [PAIN, '다친 뒤 팔을 전혀 들 수 없으면 힘줄 파열 여부를 먼저 확인하도록 적었어요.'],
    'knee-pain': [PAIN],
    'ankle-sprain': [PAIN, '체중을 실을 수 없거나 뼈를 누르면 아픈 경우 골절 확인을 먼저 하도록 적었어요.'],
    'carpal-tunnel': [PAIN],
    'elbow-pain': [PAIN, '검색어는 "경산 엘보"로 잡았어요(테니스·골프 엘보 함께).'],
    'plantar-fasciitis': [PAIN],
    'tmj': ['<b>턱관절 진료를 하시는지</b>, 치료 방법(침·약침, 추나, 뜸·물리치료, 습관 교정 안내)이 맞는지 꼭 확인해 주세요. 진료하지 않으시면 이 글은 빼겠습니다.'],
    'facial-palsy': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '발병 초기에는 신경과·이비인후과 진료를 함께 받도록 안내했어요.'],
    'headache': ['알려 주신 대로 침, 뜸, 부항, 약침, 추나, 한약을 모두 넣었어요.'],
    'dizziness': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '이석증이 의심되면 이비인후과 진료를, 말 어눌함·마비가 있으면 응급실을 안내했어요.'],
    'numbness': ['알려 주신 대로 침, 약침, 뜸, 한약만 적었어요.'],
    'indigestion': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '40세 이후 새로 생긴 증상이나 체중 감소, 검은 변, 삼킴 곤란이 있으면 내시경을 먼저 권하도록 적었어요.'],
    'reflux': ['알려 주신 대로 침, 뜸, 한약만 적었어요.'],
    'ibs': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '검색어는 "경산 과민성대장"으로 잡았어요.'],
    'insomnia': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '수면무호흡·하지불안 의심 시 검사, 우울감이 깊으면 정신건강의학과와 자살예방 상담전화 109를 안내했어요.'],
    'hwabyung': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '가슴 통증은 응급실, 우울감이 깊으면 정신건강의학과와 109를 안내했어요.'],
    'chronic-fatigue': ['알려 주신 대로 침, 뜸, 한약만 적었어요.'],
    'rhinitis': ['알려 주신 대로 침, 뜸, 한약만 적었어요.', '질문 "아이 비염도 치료할 수 있나요?"에 "네"라고 답했어요. 아이도 진료하시는지 확인 부탁드려요.'],
    'atopic-dermatitis': ['알려 주신 대로 케라틴 약침과 한약만 적었어요. 홈페이지 이름에 맞춰 "케라틴 ANK 약침"으로 썼어요.', '<b>아이에게도 케라틴 약침을 시술하시는지</b> 확인 부탁드려요. 지금 글은 나이 제한 없이 읽힐 수 있어요.'],
    'dysmenorrhea': ['알려 주신 대로 한약만 적었어요.', '해마다 심해지는 생리통, 생리 양 증가 등은 산부인과 검사를 먼저 권하도록 적었어요.'],
    'menopause': ['알려 주신 대로 한약만 적었어요.', '호르몬 치료 여부는 산부인과와 상의하도록 적었어요.', '질문 "남성도 갱년기가 있나요?"에서 남성 갱년기도 진료한다고 답했어요. 맞는지 확인 부탁드려요.'],
    'postpartum': ['알려 주신 대로 한약만 적었어요.', '"수유 중이라면 알려 주시면 수유 여부와 아기 상태를 고려해 처방한다"고 적었어요. 이 표현이 괜찮은지 봐 주세요.', '마지막 질문에서 산후 다이어트 상담도 가능하다고 적었어요.'],
    'cold-hands-feet': ['알려 주신 대로 침, 뜸, 부항, 한약만 적었어요.'],
    'alopecia-areata': ['알려 주신 대로 케라틴 약침과 한약만 적었어요.', '<b>두피에 케라틴 약침을 어떤 방법으로 놓는지</b>(손주사 등) 알려 주시면 더 구체적으로 쓸 수 있어요.', '검색어는 "경산 원형탈모"로 잡았어요. 일반 탈모도 진료하시면 "경산 탈모" 글을 따로 쓰는 것도 방법이에요.'],
}
assert set(NOTES) == {p['slug'] for p in posts}, set(NOTES) ^ {p['slug'] for p in posts}

def kday(iso):
    y, m, d = iso.split('-')
    return f'{int(m)}월 {int(d)}일'

css = re.search(r'<style>(.*?)</style>', open(f'{S}/prev/색소칼럼_초안_16편.html', encoding='utf-8').read(), re.S).group(1)
css += '.kw{display:inline-block;margin:0 6px 6px 0;padding:2px 10px;border-radius:999px;background:#e6efe9;color:#2f5241;font-size:13px;font-weight:700}\n'
css += '.local{background:#f1ede3;border-radius:12px;padding:12px 16px;color:#4d554f;font-size:14px}\n'
css += '.cat{color:#4d554f;font-size:14px;margin:0 0 10px}\n'
css += '@media (prefers-color-scheme: dark){.kw{background:#24382d;color:#8fc3a6}.local{background:#1e2a24;color:#b9c3bc}}\n'

toc, arts = [], []
for i, p in enumerate(posts, 1):
    toc.append(f'<li><a href="#{p["slug"]}"><span class="d">{kday(p["date"])}</span>{html.escape(p["title"])}</a></li>')
    body = markdown.markdown(p['body_md'], extensions=['tables'])
    faq = ''.join(f'<div class="qa"><strong>Q. {html.escape(q)}</strong><p>A. {html.escape(a)}</p></div>' for q, a in p['faq'])
    notes = ''.join(f'<li>{n}</li>' for n in NOTES[p['slug']])
    c = html.escape(p['condition'])
    arts.append(f'''<article id="{p['slug']}">
<p class="no">{i:02d} · {kday(p['date'])} 발행 예정</p>
<h2>{html.escape(p['title'])}</h2>
<p class="cat">분류: {html.escape(p['category'])} · 검색 제목: <span class="kw">{html.escape(p['keyword'])}</span></p>
<div class="check"><strong>원장님 확인</strong><ul>{notes}</ul></div>
<div class="sum"><strong>요약</strong>{html.escape(p['summary'])}</div>
<div class="body">{body}</div>
<h3>자주 묻는 질문</h3>{faq}
<p class="local">글 끝에 자동으로 붙는 칸: <b>경산·하양에서 {c} 진료를 찾으신다면</b> — 주소, 하양역 거리, 주차, 진료시간, 전화·톡톡 안내</p>
<p class="top"><a href="#toc">↑ 목록으로</a></p>
</article>''')

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>질환 칼럼 초안 29편</title>
<style>{css}</style></head><body><div class="wrap">
<h1>질환 칼럼 초안 29편</h1>
<p class="lead">피부 칼럼이 끝나는 다음 날인 10월 30일부터 하루 한 편씩, 아침 9시 40분쯤 올라가도록 날짜를 잡았어요. 원장님 확인 전에는 올라가지 않아요. 글마다 노란 칸에 확인하실 부분을 적었어요.</p>
<div class="check"><strong>공통 사항</strong><ul>
<li><b>치료 방법:</b> 질환 17편은 알려 주신 방법만 적었어요. 통증 12편(허리~턱관절)은 홈페이지 척추·관절 페이지에 있는 방법으로 적었으니 확인 부탁드려요.</li>
<li><b>검색:</b> 글마다 검색 제목이 "경산 OO | 글 제목 – 갈창림한의원"으로 나가고, 글 끝에 "경산·하양에서 OO 진료를 찾으신다면" 안내 칸이 자동으로 붙어요. 진료시간이 바뀌면 한 곳만 고치면 29편 모두 바뀌어요.</li>
<li><b>분류:</b> 통증 12편은 교통사고·통증, 생리통·갱년기·산후풍은 소아·여성, 나머지 14편은 새 분류 "질환·건강"에 넣었어요.</li>
<li><b>안전 문구:</b> 응급실이나 검사가 먼저 필요한 경우를 글마다 넣었고, 모든 글에 개인차 문구가 있어요. 최고·완치·보장 같은 표현은 쓰지 않았어요.</li>
</ul></div>
<nav id="toc"><strong>목록 (발행 예정일)</strong><ol>{''.join(toc)}</ol></nav>
{''.join(arts)}
</div></body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print(OUT, len(page) // 1024, 'KB', len(posts))
