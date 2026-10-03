"""Build the GitHub Pages website from the design artboards.

Output: /home/claude/site/  (index.html + one .html per page, assets/, .nojekyll)
"""
import re, json, os, shutil, html as htmlmod, datetime
from PIL import Image

S = '/tmp/claude-0/-home-claude/68b4eec7-1c3c-57e2-af39-86fe64cf79a4/scratchpad'
G = f'{S}/galch'
OUT = '/home/claude/site'
NAVER_KEY = 'uikplmnw9s'
ADDRESS = '경상북도 경산시 하양읍 동서2길 43'
LAT, LNG = 35.9174389, 128.8238134   # from Google plus code 8Q7CWR8F+XGGCJVH, checked on Naver map
SITE = 'https://gal0122.github.io'
LASTMOD = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
GA_ID = 'G-J8PBY1YVS7'   # Google Analytics 4 measurement ID (방문 통계)
INDEXNOW_KEY ='2f452286a2a2029189ac09582bdfdcaa'   # served at /<key>.txt (Bing, Naver, Yandex … via IndexNow)
NAVER_VERIFY = '71001f44f4ad926173e972d1f742bd136d79665f'    # content of <meta name="naver-site-verification"> from Naver Search Advisor
GOOGLE_VERIFY = 'J8QaDGTCXl33x5qhQ0BFwqwJQ9_kGM2WzyDeolMWfLE'   # content of <meta name="google-site-verification"> from Google Search Console

# search title / description per page (keywords: 경산 한의원, 경산 레이저제모)
SEO = {
 'index.html': ('경산 한의원 갈창림한의원 | 하양 · 토·일요일 진료',
   '경북 경산시 하양읍 갈창림한의원. 평일 08:30–18:30, 토·일 08:30–14:00 진료. 레이저제모·리프팅·색소·여드름 피부미용, 교통사고 후유증, 척추·관절 통증, 다이어트, 소아 성장, 여성 질환 진료.'),
 'about.html': ('병원 소개 | 경산 한의원 갈창림한의원',
   '경산 하양 갈창림한의원 소개. 충분히 듣고, 꼭 필요한 치료를 정직하게 제안하는 한의원입니다.'),
 'doctors.html': ('의료진 소개 | 경산 한의원 갈창림한의원',
   '갈창림 대표원장 — 대구한의대학교 한의과대학 졸업, 대한통합레이저의학회 정회원·교육위원. 경산 하양 갈창림한의원.'),
 'equipment.html': ('보유장비 | 경산 하양 갈창림한의원',
   '악센토N 레이저제모, 리니어펌·볼뉴머 리프팅, 큐마스터플러스, 실펌X 등 경산 하양 갈창림한의원의 보유 장비를 소개합니다.'),
 'schedule.html': ('진료시간·오시는길 | 경산 하양 갈창림한의원',
   '경북 경산시 하양읍 동서2길 43. 평일 08:30–18:30(점심 13:00–14:00), 토·일 08:30–14:00, 공휴일 휴진. 전화 053-851-0122.'),
 'skin.html': ('경산 피부미용 | 갈창림한의원',
   '리프팅, 스킨부스터, 레이저제모, 기미·잡티, 여드름, 모공까지 — 경산 하양 갈창림한의원의 피부미용 진료를 한눈에 안내합니다.'),
 'design-lifting.html': ('경산 리프팅 · 디자인리프팅 | 갈창림한의원',
   '리니어펌·볼뉴머로 부위별로 설계하는 초음파·고주파 리프팅. 경산 하양 갈창림한의원.'),
 'thread-lifting.html': ('경산 실리프팅 · 맞춤형실리프팅 | 갈창림한의원',
   '처짐의 방향과 볼륨을 함께 설계하는 맞춤형 실리프팅. 경산 하양 갈창림한의원.'),
 'booster-pdrn.html': ('경산 PDRN·엑소좀 스킨부스터 | 갈창림한의원',
   '라디쥬로 채우는 재생·탄력·미백 스킨부스터, PDRN·엑소좀 시술 안내. 경산 하양 갈창림한의원.'),
 'booster-plla.html': ('경산 PLLA 스킨부스터 | 갈창림한의원',
   '시간이 지나며 차오르는 볼륨과 탄력, PLLA 스킨부스터 시술 안내. 경산 하양 갈창림한의원.'),
 'booster-keratin.html': ('경산 케라틴 ANK 약침 | 갈창림한의원',
   '피부 장벽부터 튼튼하게 세우는 케라틴 ANK 약침 안내. 경산 하양 갈창림한의원.'),
 'booster-altcore.html': ('경산 알트코어 스킨부스터 | 갈창림한의원',
   '피부 세포 자체의 건강을 돕는 알트코어 스킨부스터 안내. 경산 하양 갈창림한의원.'),
 'booster-ecm.html': ('경산 ECM 진피재생약침 | 갈창림한의원',
   '무너진 진피의 골격을 다시 세우는 ECM 진피재생약침 안내. 경산 하양 갈창림한의원.'),
 'hair-removal.html': ('경산 레이저제모 | 하양 갈창림한의원',
   '경산 하양 갈창림한의원 레이저제모. 755nm 알렉산드라이트·1064nm 엔디야그 듀얼 파장 악센토N으로 털과 피부 타입에 맞춰 시술합니다. 얼굴·겨드랑이·팔·다리 부위별 비용 안내.'),
 'pigment.html': ('경산 기미·흑자·잡티 색소 | 갈창림한의원',
   '532·755·1064nm, 색소에 맞춰 고르는 세 가지 파장. 기미·흑자·잡티 진료 안내 — 경산 하양 갈창림한의원.'),
 'mole.html': ('경산 점빼기 · 쥐젖 · 편평사마귀 제거 | 갈창림한의원',
   '모양과 깊이에 맞춰 고르는 아이스 점빼기와 유펄스 CO2. 점·쥐젖·편평사마귀 제거 안내 — 경산 하양 갈창림한의원.'),
 'acne.html': ('경산 여드름 | 갈창림한의원',
   '원인을 나눠 단계별로 — 압출, 필링, ALA-PDT, 골드PTT, PDRN. 경산 하양 갈창림한의원의 여드름 진료.'),
 'acne-red.html': ('경산 여드름 붉은자국 | 갈창림한의원',
   '자국의 색에 맞춰 토닝과 스킨부스터로 진료합니다. 경산 하양 갈창림한의원.'),
 'acne-scar.html': ('경산 여드름 흉터 | 갈창림한의원',
   '흉터 모양에 맞춰 서브시전, 니들RF, CO2 핀홀, 스킨부스터로 진료합니다. 경산 하양 갈창림한의원.'),
 'pore.html': ('경산 모공 | 갈창림한의원',
   '모공의 원인에 맞춰 니들RF, 제네시스 토닝, 스킨부스터, 필링으로 진료합니다. 경산 하양 갈창림한의원.'),
 'traffic.html': ('경산 교통사고 한의원 · 후유증 | 갈창림한의원',
   '검사에서 이상이 없어도 아프다면 치료가 필요합니다. 교통사고 후유증 한방 진료, 자동차보험 진료 — 경산 하양 갈창림한의원.'),
 'traffic-process.html': ('교통사고 치료 과정 | 경산 하양 갈창림한의원',
   '사고 직후부터 회복까지, 시기에 맞춰 치료합니다. 경산 하양 갈창림한의원 교통사고 진료 과정 안내.'),
 'traffic-treat.html': ('교통사고 치료 방법 | 경산 하양 갈창림한의원',
   '증상에 맞춰 네 가지 한방 치료를 함께 씁니다. 경산 하양 갈창림한의원 교통사고 치료 방법 안내.'),
 'pain-spine.html': ('경산 목·허리 척추 통증 한의원 | 갈창림한의원',
   '목부터 허리까지, 통증을 만든 원인을 찾아 치료합니다. 경산 하양 갈창림한의원 척추 질환 진료.'),
 'pain-joint.html': ('경산 어깨·무릎 관절 통증 한의원 | 갈창림한의원',
   '쓰는 만큼 지치는 관절, 아픈 이유부터 살핍니다. 경산 하양 갈창림한의원 관절 질환 진료.'),
 'diet.html': ('경산 한방 다이어트 | 갈창림한의원',
   '체중계 숫자보다 건강하게 유지할 수 있는 몸을 목표로 합니다. 경산 하양 갈창림한의원 한방 다이어트.'),
 'growth.html': ('경산 소아 성장 한의원 | 갈창림한의원',
   '아이가 가진 성장 가능성을 충분히 키울 수 있도록 돕습니다. 경산 하양 갈창림한의원 소아 성장 진료.'),
 'women.html': ('경산 여성 질환 한의원 | 갈창림한의원',
   '생리통부터 산후 회복, 갱년기까지 여성의 몸을 살핍니다. 경산 하양 갈창림한의원 여성 질환 진료.'),
 'price.html': ('가격표 · 레이저제모 비용 | 경산 갈창림한의원',
   '레이저제모 부위별 비용, 리니어펌·볼뉴머·실리프팅, 토닝, 여드름 시술 비용 안내(부가세 포함). 경산 하양 갈창림한의원.'),
 'privacy.html': ('개인정보처리방침 | 갈창림한의원', '갈창림한의원 홈페이지 개인정보처리방침.'),
 'terms.html': ('이용약관 | 갈창림한의원', '갈창림한의원 홈페이지 이용약관.'),
}

SAME_AS = ['https://blog.naver.com/gal0122', 'https://www.instagram.com/gal__clinic/']
NAVER_LINK = 'https://map.naver.com/p/search/%EA%B0%88%EC%B0%BD%EB%A6%BC%ED%95%9C%EC%9D%98%EC%9B%90'
CLINIC_ID, SITE_ID = SITE + '/#clinic', SITE + '/#website'
# services offered (names as shown on the site) -> page
SERVICES = [
 ('MedicalProcedure', '레이저제모', 'hair-removal.html'),
 ('MedicalProcedure', '디자인리프팅', 'design-lifting.html'),
 ('MedicalProcedure', '맞춤형 실리프팅', 'thread-lifting.html'),
 ('MedicalProcedure', '스킨부스터', 'booster-pdrn.html'),
 ('MedicalProcedure', '기미·흑자·잡티 색소 치료', 'pigment.html'),
 ('MedicalProcedure', '점·쥐젖·편평사마귀 제거', 'mole.html'),
 ('MedicalProcedure', '여드름 치료', 'acne.html'),
 ('MedicalProcedure', '여드름 흉터 치료', 'acne-scar.html'),
 ('MedicalProcedure', '모공 치료', 'pore.html'),
 ('MedicalTherapy', '교통사고 후유증 치료 (자동차보험 진료)', 'traffic.html'),
 ('MedicalTherapy', '척추 질환 치료', 'pain-spine.html'),
 ('MedicalTherapy', '관절 질환 치료', 'pain-joint.html'),
 ('MedicalTherapy', '한방 다이어트', 'diet.html'),
 ('MedicalTherapy', '소아 성장 치료', 'growth.html'),
 ('MedicalTherapy', '여성 질환 치료', 'women.html'),
]
LD_WEBSITE = {'@type': 'WebSite', '@id': SITE_ID, 'url': SITE + '/', 'name': '갈창림한의원',
              'alternateName': ['갈창림 한의원', '경산 갈창림한의원'], 'inLanguage': 'ko-KR',
              'publisher': {'@id': CLINIC_ID}}
LD_CLINIC = {
 '@type': 'MedicalClinic', '@id': CLINIC_ID,
 'name': '갈창림한의원', 'alternateName': ['갈창림 한의원', 'Gal Chang Lim Korean Medicine Clinic'],
 'description': SEO['index.html'][1],
 'url': SITE + '/', 'telephone': '+82-53-851-0122',
 'image': SITE + '/assets/og-image.png', 'logo': SITE + '/assets/favicon.png',
 'address': {'@type': 'PostalAddress', 'streetAddress': '하양읍 동서2길 43', 'addressLocality': '경산시',
             'addressRegion': '경상북도', 'addressCountry': 'KR'},
 'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LNG},
 'openingHoursSpecification': [
   {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:30', 'closes': '18:30'},
   {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Saturday', 'Sunday'], 'opens': '08:30', 'closes': '14:00'}],
 'medicalSpecialty': ['Dermatologic', 'Musculoskeletal'],
 'hasMap': NAVER_LINK,
 'areaServed': [{'@type': 'City', 'name': '경상북도 경산시'}],
 'employee': {'@type': 'Person', 'name': '갈창림', 'jobTitle': '대표원장', 'url': SITE + '/doctors.html',
              'alumniOf': {'@type': 'CollegeOrUniversity', 'name': '대구한의대학교 한의과대학'}},
 'availableService': [{'@type': t, 'name': n, 'url': f'{SITE}/{u}'} for t, n, u in SERVICES],
 'sameAs': SAME_AS,
}
# breadcrumb label (as shown on each page) -> section page
CRUMB = {'홈': '', '병원소개': 'about.html', '피부미용': 'skin.html', '리프팅': 'design-lifting.html',
         '스킨부스터': 'booster-pdrn.html', '제모': 'hair-removal.html', '색소': 'pigment.html',
         '여드름': 'acne.html', '모공': 'pore.html', '교통사고': 'traffic.html', '통증': 'pain-spine.html',
         '다이어트': 'diet.html', '소아·여성': 'growth.html', '가격표': 'price.html'}
NON_MEDICAL = {'index.html', 'about.html', 'doctors.html', 'equipment.html', 'schedule.html', 'price.html',
               'privacy.html', 'terms.html'}


def plain(fragment):
    return re.sub(r'\s+', ' ', htmlmod.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def faq_pairs(body):
    """Q&A pairs from the visible FAQ accordions (<div class="faq"> … <details><summary>Q…</summary><p>A</p>)."""
    out = []
    for m in re.finditer(r'class="faq"', body):
        end = body.find('</section>', m.end())
        chunk = body[m.end(): end if end > 0 else None]
        for q, a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)</details>', chunk, re.S):
            q = re.sub(r'<span class="faq-icon".*?</span>', '', q, flags=re.S)
            q, a = re.sub(r'^Q\.\s*', '', plain(q)), plain(a)
            if q and a:
                out.append((q, a))
    return out


def page_ld(slug_, title, desc, url, body):
    graph = []
    if slug_ == 'index.html':
        graph += [LD_WEBSITE, dict(LD_CLINIC)]
    wp = {'@type': 'WebPage' if slug_ in NON_MEDICAL else 'MedicalWebPage', '@id': url + '#webpage',
          'url': url, 'name': title, 'description': desc, 'inLanguage': 'ko-KR',
          'isPartOf': {'@id': SITE_ID}, 'about': {'@id': CLINIC_ID}, 'dateModified': LASTMOD}
    m = re.search(r'<p style="margin: 0; font-size: 14px; color: #5d655f">(홈 &gt;.*?)</p>', body)
    if m:
        labels = [plain(x) for x in m.group(1).split('&gt;')]
        items, seen = [], set()
        for i, lab in enumerate(labels):
            last = i == len(labels) - 1
            link = url if last else (SITE + '/' + CRUMB[lab]) if lab in CRUMB else None
            if not link or link in seen:
                if last and items:          # e.g. "여드름 > 여드름": keep one entry, name it after the page
                    items[-1] = {**items[-1], 'name': lab}
                continue
            seen.add(link)
            items.append({'name': lab, 'item': link})
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, **it} for i, it in enumerate(items)]})
        wp['breadcrumb'] = {'@id': url + '#breadcrumb'}
    graph.insert(0 if slug_ != 'index.html' else 2, wp)
    qa = faq_pairs(body)
    if qa:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'url': url, 'inLanguage': 'ko-KR',
                      'isPartOf': {'@id': url + '#webpage'},
                      'mainEntity': [{'@type': 'Question', 'name': q,
                                      'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]})
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + data.replace('</', '<\\/') + '</script>\n', len(qa)

# blob id -> local file (same map the measuring script uses)
BLOB = json.loads(re.search(r'const MAP = (\{.*?\});', open(f'{S}/measure.js', encoding='utf-8').read()).group(1))

canvas = json.load(open(f'{G}/project/canvas.json', encoding='utf-8'))
order = canvas['order']
NON_PAGES = {'Popup.dc.html'}          # design-only boards, not web pages
pages = [f for f in order if f not in NON_PAGES]


def slug(dc):
    name = dc.replace('.dc.html', '')
    if name == 'Main':
        return 'index.html'
    return re.sub(r'(?<=[a-z])(?=[A-Z])', '-', name).lower() + '.html'


SLUG = {f: slug(f) for f in pages}

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(f'{OUT}/assets')
open(f'{OUT}/.nojekyll', 'w').close()

asset_url = {}


def asset(bid):
    if bid in asset_url:
        return asset_url[bid]
    src = BLOB[bid]
    base, ext = os.path.splitext(os.path.basename(src))
    ext = ext.lower()
    if ext in ('.svg', '.woff2'):
        name = base + ext
        shutil.copyfile(src, f'{OUT}/assets/{name}')
    else:
        name = base + '.webp'
        im = Image.open(src)
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(f'{OUT}/assets/{name}', 'WEBP', quality=84)
    asset_url[bid] = f'assets/{name}'
    return asset_url[bid]


# favicon from the logo mark
fav = Image.open(f'{G}/img/logo-mark.png').convert('RGBA')
fav.thumbnail((192, 192))
fav.save(f'{OUT}/assets/favicon.png')

# share-preview image (KakaoTalk, Naver, etc.)
from PIL import ImageDraw, ImageFont
FONT = '/root/.fonts/PretendardVariable.ttf'
def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f
og = Image.new('RGB', (1200, 630), '#faf7f0')
d = ImageDraw.Draw(og)
d.rectangle([0, 560, 1200, 630], fill='#2f5241')
logo = Image.open(f'{G}/img/logo-horizontal.png').convert('RGBA')
logo.thumbnail((640, 200))
og.paste(logo, ((1200 - logo.width) // 2, 150), logo)
line = '경산 하양 한의원 · 토·일요일 진료'
fnt = font(40, 600)
w = d.textlength(line, font=fnt)
d.text(((1200 - w) / 2, 400), line, font=fnt, fill='#4d554f')
foot = '경북 경산시 하양읍 동서2길 43  ·  053-851-0122'
fnt2 = font(28, 500)
w2 = d.textlength(foot, font=fnt2)
d.text(((1200 - w2) / 2, 580), foot, font=fnt2, fill='#ffffff')
og.save(f'{OUT}/assets/og-image.png', optimize=True)


def fix_links(html):
    def rep(m):
        name, frag = m.group(1), m.group(2) or ''
        return f'href="{SLUG[name + ".dc.html"]}{frag}"'
    return re.sub(r'href="([A-Za-z]+)\.dc\.html(#[\w-]+)?"', rep, html)


def blobs(html):
    return re.sub(r'/_blob/([0-9a-f]{32})', lambda m: asset(m.group(1)), html)


BASE_JS = '''<script>
function slide(btn, dir) {
  var root = btn.closest('[data-eq-slider]');
  var track = root ? root.querySelector('[data-eq-track]') : null;
  if (!track) return;
  var first = track.firstElementChild;
  var step = first ? first.getBoundingClientRect().width + 16 : 276;
  var visible = Math.max(1, Math.floor(track.clientWidth / step));
  track.scrollBy({ left: dir * step * visible, behavior: 'smooth' });
}
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href="#"]');
  if (a) e.preventDefault();
});
// mobile full menu: end just above the bottom quick bar / browser toolbar so the last items stay reachable
(function () {
  var d = document.querySelector('.m-menu');
  var nav = d && d.querySelector('nav');
  if (!nav) return;
  var hd = document.querySelector('.site-hd'), qn = document.querySelector('.qn');
  function fit() {
    if (!d.open) return;
    var top = hd ? hd.getBoundingClientRect().bottom : 72, bottom = window.innerHeight;
    if (qn) {
      var r = qn.getBoundingClientRect();
      if (r.width > window.innerWidth / 2 && r.top > window.innerHeight / 2) bottom = r.top;  // bar along the bottom (phones)
    }
    nav.style.boxSizing = 'border-box';
    nav.style.maxHeight = Math.max(160, Math.ceil(bottom - top) + 2) + 'px';  // tuck 2px under the bar: no gap
  }
  d.addEventListener('toggle', fit);
  window.addEventListener('resize', fit);
})();
</script>'''

MAP_JS = f'''<script src="https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId={NAVER_KEY}"></script>
<script>
(function () {{
  var boxes = document.querySelectorAll('[data-naver-map]');
  if (!boxes.length || !window.naver || !naver.maps) return;
  window.navermap_authFailure = function () {{
    document.querySelectorAll('[data-naver-map] > .nmap').forEach(function (el) {{ el.remove(); }});
  }};
  var pin = '<div style="transform:translate(-50%,calc(-100% - 8px));display:flex;flex-direction:column;align-items:center">'
    + '<div style="white-space:nowrap;padding:8px 14px;border-radius:999px;background:#2f5241;color:#ffffff;font:700 13px Pretendard,sans-serif;box-shadow:0 6px 16px rgba(36,48,42,.25)">갈창림한의원</div>'
    + '<div style="width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-top:8px solid #2f5241"></div></div>';
  // {ADDRESS} (checked on the map: next to 베네치아아파트 103동, 동서2길 35)
  var pos = new naver.maps.LatLng({LAT}, {LNG});
  boxes.forEach(function (box) {{
    var wrap = document.createElement('div');
    wrap.className = 'nmap';
    wrap.style.cssText = 'position:absolute;top:0;left:0;right:0;bottom:0;z-index:0;isolation:isolate;overflow:hidden;border-radius:inherit';
    var el = document.createElement('div');
    el.style.cssText = 'width:100%;height:100%';
    wrap.appendChild(el);
    box.appendChild(wrap);
    var map = new naver.maps.Map(el, {{
      center: pos, zoom: 17, scrollWheel: false,
      zoomControl: true,
      zoomControlOptions: {{ position: naver.maps.Position.TOP_RIGHT, style: naver.maps.ZoomControlStyle.SMALL }}
    }});
    new naver.maps.Marker({{ position: pos, map: map, icon: {{ content: pin, anchor: new naver.maps.Point(0, 0) }} }});
  }});
}})();
</script>'''

FALLBACK = (f'<a href="{NAVER_LINK}" target="_blank" rel="noopener" '
            'style="font-size: 14px; font-weight: 600; color: #2f5241">네이버 지도에서 위치 보기 →</a>')


def balanced_div(html, start):
    """Return the <div ...>...</div> element that begins at index `start`."""
    depth, i = 0, start
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return html[start:start + m.end()]
    raise ValueError('unbalanced div')


# ---- home-page popups (designed on the "Popup" board) ----
POPUP_HTML, POPUP_CSS = '', ''
if os.path.exists(f'{G}/project/Popup.dc.html'):
    psrc = open(f'{G}/project/Popup.dc.html', encoding='utf-8').read()
    pbody = psrc.split('</helmet>', 1)[1]
    layer = balanced_div(pbody, pbody.index('<div class="pop-layer" data-popups>'))
    POPUP_HTML = ('<div class="pop-overlay" id="site-popups" hidden>\n' + blobs(fix_links(layer)) + '\n</div>')
    pcss = re.search(r'<style>(.*?)</style>', psrc, re.S).group(1)
    keep = [l for l in pcss.strip().splitlines()
            if not l.startswith(('@font-face', 'body{', '.pop-stage{'))]
    POPUP_CSS = '\n'.join(keep) + '''
.pop-overlay{position:fixed;top:0;left:0;right:0;bottom:0;z-index:100;display:flex;justify-content:center;align-items:flex-start;padding:110px 20px 40px;box-sizing:border-box;overflow-y:auto;background:rgba(36,48,42,.55);font-family:'Pretendard','Pretendard Variable',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;color:#24302a;line-height:1.6}
.pop-overlay[hidden]{display:none}
@media (max-width:640px){.pop-overlay{align-items:flex-start;padding:16px 16px 76px}.pop-layer{width:100%;margin:auto 0}.pop-cal td{height:36px}.pop-body{gap:12px}.pop-reasons li{padding:9px 14px}.pop-open{padding:11px 14px}.pop{flex:0 1 auto;width:100%;max-width:380px}.pop-body{padding:24px 22px 20px}.pop-date{font-size:30px}.pop-title{font-size:20px!important}}'''

POPUP_JS = '''<script>
(function () {
  var overlay = document.getElementById('site-popups');
  if (!overlay) return;
  var layer = overlay.querySelector('.pop-layer');
  var KEY = 'galclinic-popup-hide-';
  var DAY = 24 * 60 * 60 * 1000;
  var now = Date.now();
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  var pops = [].slice.call(overlay.querySelectorAll('.pop')).filter(function (p) {
    var until = p.getAttribute('data-until');
    var expired = until && now > new Date(until + 'T23:59:59+09:00').getTime();
    var snoozed = Number(load(KEY + p.getAttribute('data-pop')) || 0) > now;
    if (expired || snoozed) { p.parentNode.removeChild(p); return false; }
    return true;
  });
  var mq = window.matchMedia('(max-width: 640px)');
  function layout() {
    pops.forEach(function (p, i) { p.style.display = (!mq.matches || i === 0) ? '' : 'none'; });
    overlay.hidden = pops.length === 0;
    document.documentElement.style.overflow = pops.length ? 'hidden' : '';
  }
  function closePop(p, remember) {
    if (remember) save(KEY + p.getAttribute('data-pop'), String(Date.now() + DAY));
    if (p.parentNode) p.parentNode.removeChild(p);
    pops = pops.filter(function (x) { return x !== p; });
    layout();
  }
  pops.forEach(function (p) {
    p.querySelector('.pop-close').addEventListener('click', function () {
      closePop(p, p.querySelector('.pop-check input').checked);
    });
  });
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay || e.target === layer) pops.slice().forEach(function (p) { closePop(p, false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pops.length) closePop(pops[0], false);
  });
  if (mq.addEventListener) mq.addEventListener('change', layout);
  layout();
})();
</script>'''

# Google Analytics 4 — no ad features (privacy policy 제10조 ③); phone / TalkTalk taps counted as events
GA_HEAD = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_ID}', {{ allow_google_signals: false, allow_ad_personalization_signals: false }});
document.addEventListener('click', function (e) {{
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var h = a.getAttribute('href') || '';
  if (h.indexOf('tel:') === 0) gtag('event', 'call_click', {{ link_text: (a.textContent || '').trim().slice(0, 40) }});
  else if (h.indexOf('talk.naver.com') > -1) gtag('event', 'talk_click', {{ link_text: (a.textContent || '').trim().slice(0, 40) }});
}});
</script>
''' if GA_ID else ''

report = []
for f in pages:
    src = open(f'{G}/project/{f}', encoding='utf-8').read()
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    # extra helmet styles (e.g. Privacy/Terms media rule) live in the same <style>; also keep any 2nd style block
    extra = re.findall(r'<style>(.*?)</style>', src.split('</helmet>')[0], re.S)[1:]
    is_home = f == 'Main.dc.html'
    style = blobs('\n'.join([style] + extra + ([POPUP_CSS] if is_home and POPUP_HTML else [])))
    body = src.split('</helmet>', 1)[1].split('</x-dc>', 1)[0]
    body = fix_links(body)
    body = body.replace('onClick="{{ prev }}"', 'onclick="slide(this,-1)"').replace('onClick="{{ next }}"', 'onclick="slide(this,1)"')
    body = blobs(body)
    has_map = 'data-naver-map' in body
    if has_map:
        body = body.replace('<span style="font-size: 13px; color: #5d655f">실제 홈페이지에서 지도가 표시됩니다</span>', FALLBACK)
    assert '{{' not in body and '/_blob/' not in body and '.dc.html' not in body, f

    raw = re.sub(r'^\d+\s*', '', canvas['boards'][f]['title'])
    page = raw.split(' · ')[-1]
    title, desc = SEO.get(SLUG[f], (f'{page} | 갈창림한의원', f'{raw} — 경산 하양 갈창림한의원'))
    url = SITE + '/' + ('' if SLUG[f] == 'index.html' else SLUG[f])
    extra_head = ''
    if is_home:
        if NAVER_VERIFY:
            extra_head += f'<meta name="naver-site-verification" content="{NAVER_VERIFY}">\n'
        if GOOGLE_VERIFY:
            extra_head += f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">\n'
    ld, n_faq = page_ld(SLUG[f], title, desc, url, body)
    extra_head += ld

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{GA_HEAD}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="갈창림한의원">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{extra_head}<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<link rel="preload" href="assets/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin>
<style>
{style.strip()}
</style>
</head>
<body>
{body.strip()}
{POPUP_HTML if is_home else ''}
{BASE_JS}
{POPUP_JS if is_home and POPUP_HTML else ''}
{MAP_JS if has_map else ''}
</body>
</html>
'''
    open(f'{OUT}/{SLUG[f]}', 'w', encoding='utf-8').write(html)
    report.append((SLUG[f], len(html) // 1024, has_map, n_faq))

# sitemap.xml + robots.txt for Naver Search Advisor / Google Search Console
urls = [SITE + '/' + ('' if SLUG[f] == 'index.html' else SLUG[f]) for f in pages]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sm.append(f'  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod></url>')
sm.append('</urlset>')
open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
AI_BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
           'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot', 'Applebot-Extended',
           'Bingbot', 'Googlebot', 'Yeti', 'Daumoa']
robots = ('User-agent: *\nAllow: /\n\n'
          '# Search engines and AI search / answer services are welcome to read this site\n'
          + ''.join(f'User-agent: {b}\n' for b in AI_BOTS) + 'Allow: /\n\n'
          f'Sitemap: {SITE}/sitemap.xml\n')
open(f'{OUT}/robots.txt', 'w', encoding='utf-8').write(robots)
open(f'{OUT}/{INDEXNOW_KEY}.txt', 'w', encoding='utf-8').write(INDEXNOW_KEY)

# llms.txt — plain-language summary for AI assistants (https://llmstxt.org)
GROUPS = [('병원 안내', ['about.html', 'doctors.html', 'equipment.html', 'schedule.html', 'price.html']),
          ('피부미용', ['skin.html', 'hair-removal.html', 'design-lifting.html', 'thread-lifting.html',
                    'booster-pdrn.html', 'booster-plla.html', 'booster-keratin.html', 'booster-altcore.html',
                    'booster-ecm.html', 'pigment.html', 'mole.html', 'acne.html', 'acne-red.html',
                    'acne-scar.html', 'pore.html']),
          ('교통사고 · 통증', ['traffic.html', 'traffic-process.html', 'traffic-treat.html', 'pain-spine.html',
                         'pain-joint.html']),
          ('다이어트 · 소아 · 여성', ['diet.html', 'growth.html', 'women.html'])]
grouped = {s for _, ss in GROUPS for s in ss}
assert grouped | {'index.html', 'privacy.html', 'terms.html'} == set(SLUG.values()), set(SLUG.values()) - grouped
seo_of = lambda s: SEO.get(s, (s, ''))
llms = ['# 갈창림한의원', '',
        '> 경상북도 경산시 하양읍 동서2길 43에 있는 한의원입니다. 평일(월~금) 08:30–18:30(점심 13:00–14:00), '
        '토·일요일 08:30–14:00(점심시간 없음) 진료하며 공휴일은 휴진합니다. 전화 053-851-0122.', '',
        '대표원장 갈창림(대구한의대학교 한의과대학 졸업)이 직접 진찰하고 치료합니다. 레이저제모·리프팅·색소·여드름·모공·스킨부스터 등 '
        '피부미용, 교통사고 후유증(자동차보험 진료), 척추·관절 통증, 다이어트, 소아 성장, 여성 질환을 진료합니다. '
        '하양역(대구도시철도 1호선·대구선)에서 걸어서 약 10~15분이며, 건물 주차장과 이면도로에 주차할 수 있습니다. '
        '상담·예약은 네이버 톡톡 또는 전화로 할 수 있습니다. 시술 결과와 필요한 횟수는 개인에 따라 차이가 있습니다.', '']
for name, slugs in GROUPS:
    llms += [f'## {name}', '']
    for s in slugs:
        t, d = seo_of(s)
        llms.append(f'- [{t.split(" | ")[0]}]({SITE}/{s}): {d}')
    llms.append('')
llms += ['## Optional', '', f'- [개인정보처리방침]({SITE}/privacy.html)', f'- [이용약관]({SITE}/terms.html)', '']
open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write('\n'.join(llms))

total = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(OUT) for x in fs)
for r in report:
    print(f'{r[0]:24s} {r[1]:4d} KB' + ('  [map]' if r[2] else '') + (f'  faq={r[3]}' if r[3] else ''))
print(len(report), 'pages,', len(os.listdir(f'{OUT}/assets')), 'assets, total', total // 1024, 'KB')
