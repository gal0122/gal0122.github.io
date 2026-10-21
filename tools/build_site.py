"""Build the GitHub Pages website from the design artboards.

Output: /home/claude/site/  (index.html + one .html per page, assets/, .nojekyll)
"""
import re, json, os, sys, shutil, html as htmlmod, datetime
from PIL import Image

# Work folder (build_site.py, columns.py, measure.js, galch/, fonts/, pyshim/). Any copy works: GAL_S or the script's folder.
S = os.environ.get('GAL_S') or os.path.dirname(os.path.abspath(__file__))
G = f'{S}/galch'
OUT = os.environ.get('GAL_OUT', '/home/claude/site')
NAVER_KEY = 'ga0nqeox26'   # NCP Maps app d1 (Web URL: https://galclinic.co.kr); old app 'gal' = uikplmnw9s
ADDRESS = '경상북도 경산시 하양읍 동서2길 43, 3층'
LAT, LNG = 35.9174389, 128.8238134   # from Google plus code 8Q7CWR8F+XGGCJVH, checked on Naver map
DOMAIN = 'galclinic.co.kr'            # custom domain (가비아) → GitHub Pages; old gal0122.github.io redirects here
SITE = 'https://' + DOMAIN
LASTMOD = os.environ.get('GAL_TODAY') or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')   # today in Korea
REVIEWED = '2026-10-08'   # 시술 페이지 '최종 검토' 날짜 (작성·검토 표시와 같이 바꿀 것)
GA_ID = 'G-J8PBY1YVS7'   # Google Analytics 4 measurement ID (방문 통계)
INDEXNOW_KEY ='2f452286a2a2029189ac09582bdfdcaa'   # served at /<key>.txt (Bing, Naver, Yandex … via IndexNow)
NAVER_VERIFY = ['849e986ffddc741f0bba21c98f16c7d7777531d6', '71001f44f4ad926173e972d1f742bd136d79665f']  # galclinic.co.kr, old gal0122.github.io    # content of <meta name="naver-site-verification"> from Naver Search Advisor
GOOGLE_VERIFY = 'J8QaDGTCXl33x5qhQ0BFwqwJQ9_kGM2WzyDeolMWfLE'   # content of <meta name="google-site-verification"> from Google Search Console

# search title / description per page (keywords: 경산 한의원, 경산 레이저제모)
SEO = {
 'index.html': ('경산 한의원 갈창림 한의원 | 하양 · 토·일요일 진료',
   '경상북도 경산시 하양읍 갈창림 한의원. 평일 08:30–18:30, 토·일 08:30–14:00 진료. 레이저제모·리프팅·색소·여드름 피부미용, 교통사고 후유증, 척추·관절 통증, 소화불량·두통·불면·비염, 다이어트, 소아 성장, 여성 질환.'),
 'about.html': ('병원 소개 | 경산 한의원 갈창림 한의원',
   '경산 하양 갈창림 한의원 소개. 충분히 듣고, 꼭 필요한 치료를 정직하게 제안하는 한의원입니다. 평일은 아침 8시 30분부터, 토·일요일에도 진료합니다.'),
 'doctors.html': ('갈창림 대표원장 소개 | 경산 하양 갈창림 한의원',
   '갈창림 대표원장 — 대구한의대학교 한의과대학 졸업, 대한통합레이저의학회 정회원·교육위원. 경산 하양 갈창림 한의원.'),
 'equipment.html': ('피부 레이저 보유장비 · 악센토N · 실펌X · 야누스프로 | 갈창림 한의원',
   '악센토N 레이저제모, 리니어펌·볼뉴머 리프팅, 큐마스터플러스, 실펌X 등 경산 하양 갈창림 한의원의 보유 장비를 소개합니다.'),
 'schedule.html': ('진료시간·오시는길 | 경산 하양 갈창림 한의원',
   '경상북도 경산시 하양읍 동서2길 43, 3층. 평일 08:30–18:30(점심 13:00–14:00), 토·일 08:30–14:00, 공휴일 휴진. 전화 053-851-0122.'),
 'skin.html': ('경산 피부미용 · 레이저토닝 · 제모 · 리프팅 | 갈창림 한의원',
   '리프팅, 스킨부스터, 레이저제모, 기미·잡티, 여드름, 모공까지 — 경산 하양 갈창림 한의원의 피부미용 진료를 한눈에 안내합니다.'),
 'design-lifting.html': ('경산 리프팅 · 리니어펌·볼뉴머 디자인리프팅 | 갈창림 한의원',
   '리니어펌(초음파)과 볼뉴머(고주파)를 얼굴 지방량과 피부 두께에 맞춰 부위별로 설계하는 디자인리프팅. 권장 주기, 가능한 부작용과 주의사항, 가격 안내 — 경산 하양 갈창림 한의원.'),
 'thread-lifting.html': ('경산 실리프팅 · 맞춤형실리프팅 | 갈창림 한의원',
   '처짐의 방향과 볼륨을 함께 설계하는 맞춤형 실리프팅. 녹는 실을 캐뉼라로 넣는 시술 방법과 회복 기간, 가능한 부작용과 주의사항을 안내합니다. 경산 하양 갈창림 한의원.'),
 'booster-pdrn.html': ('경산 PDRN·엑소좀 스킨부스터 | 갈창림 한의원',
   'PDRN·엑소좀을 담은 라디쥬(오리지널·플러스·퓨어)로 재생·탄력·미백을 돕는 스킨부스터. 권장 주기, 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'booster-plla.html': ('경산 PLLA 스킨부스터 | 갈창림 한의원',
   '시간이 지나며 내 피부의 콜라겐으로 차오르는 볼륨과 탄력, PLLA 스킨부스터. 시술 방법과 권장 주기, 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'booster-keratin.html': ('경산 케라틴 ANK 약침 | 갈창림 한의원',
   '피부 장벽부터 튼튼하게 세우는 케라틴 ANK 약침. 주입 방법과 권장 주기, 가능한 부작용과 시술 후 주의사항을 안내합니다. 경산 하양 갈창림 한의원.'),
 'booster-altcore.html': ('경산 알트코어 스킨부스터 | 갈창림 한의원',
   '미토콘드리아에 작용해 피부 세포 자체의 건강을 돕는 알트코어 스킨부스터. 주입 방법과 권장 주기, 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'booster-ecm.html': ('경산 ECM 진피재생약침 | 갈창림 한의원',
   '콜라겐·엘라스틴 등 ECM 성분으로 무너진 진피의 골격을 다시 세우는 ECM 진피재생약침. 권장 주기, 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'hair-removal.html': ('경산 레이저제모 · 남자 수염제모 · 악센토N | 갈창림 한의원',
   '듀얼 파장(755nm·1064nm) 악센토N으로 털과 피부 타입에 맞춰 시술하는 레이저제모. 필요한 횟수, 가능한 부작용과 주의사항, 부위별 가격표 안내 — 경산 하양 갈창림 한의원.'),
 'pigment.html': ('경산 기미·흑자·잡티 · 레이저토닝 | 갈창림 한의원',
   '532·755·1064nm, 색소에 맞춰 고르는 세 가지 파장. 기미·흑자·잡티 진료와 레이저토닝·트리플토닝, 가능한 부작용·주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'mole.html': ('경산 점빼기 · 점제거 · 쥐젖 · 편평사마귀 | 갈창림 한의원',
   '모양과 깊이에 맞춰 고르는 아이스 점빼기와 유펄스 CO2. 점제거와 쥐젖·편평사마귀 제거 방법, 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'acne.html': ('경산 여드름 치료 · PDT · 골드PTT | 갈창림 한의원',
   '원인을 나눠 단계별로 — 압출, 필링, ALA-PDT, 골드PTT, PDRN. 시술 정보와 가능한 부작용 안내 — 경산 하양 갈창림 한의원의 여드름 진료.'),
 'acne-red.html': ('경산 여드름 붉은자국 | 갈창림 한의원',
   '여드름이 가라앉은 뒤 남은 붉은 자국과 갈색 자국, 자국의 색에 맞춰 토닝과 스킨부스터로 진료합니다. 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'acne-scar.html': ('경산 여드름 흉터 | 갈창림 한의원',
   '아이스픽·박스카·롤링, 흉터 모양에 맞춰 서브시전, 니들RF(실펌X), CO2 핀홀, 스킨부스터를 조합합니다. 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'pore.html': ('경산 모공 | 갈창림 한의원',
   '피지·탄력·흉터, 모공이 넓어진 원인에 맞춰 니들RF, 제네시스 토닝, 스킨부스터, 필링으로 진료합니다. 가능한 부작용과 주의사항 안내 — 경산 하양 갈창림 한의원.'),
 'traffic.html': ('경산 교통사고 한의원 · 후유증 | 갈창림 한의원',
   '검사에서 이상이 없어도 아프다면 치료가 필요합니다. 교통사고 후유증 한방 진료, 자동차보험 진료 — 경산 하양 갈창림 한의원.'),
 'traffic-process.html': ('교통사고 치료 과정 | 경산 하양 갈창림 한의원',
   '사고 직후부터 회복까지, 통증의 시기에 맞춰 치료 목표가 달라집니다. 첫 진료 때 확인하는 것과 자동차보험 진료 안내 — 경산 하양 갈창림 한의원 교통사고 치료 과정.'),
 'traffic-treat.html': ('교통사고 치료 방법 | 경산 하양 갈창림 한의원',
   '침·약침, 추나, 한약, 뜸·부항·물리치료를 증상에 맞춰 함께 씁니다. 교통사고 후유증 한방 치료 방법과 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'pain-spine.html': ('경산 목·허리 척추 통증 한의원 | 갈창림 한의원',
   '목디스크·허리디스크·척추관협착증 등 목부터 허리까지, 통증을 만든 원인을 찾아 치료합니다. 침·약침·추나·한약 치료와 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'pain-joint.html': ('경산 어깨·무릎 관절 통증 한의원 | 갈창림 한의원',
   '어깨·팔꿈치·손목·무릎·발목, 쓰는 만큼 지치는 관절이 아픈 이유부터 살핍니다. 침·약침·추나·한약 치료와 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'internal-digestive.html': ('경산 소화불량·역류성 식도염 한의원 | 갈창림 한의원',
   '검사는 괜찮다는데 계속 불편한 속, 원인부터 살핍니다. 기능성 소화불량, 역류성 식도염, 과민성 대장 증후군 — 경산 하양 갈창림 한의원 소화기 질환 진료.'),
 'internal-neuro.html': ('경산 두통·안면마비·손발 저림 한의원 | 갈창림 한의원',
   '반복되는 두통과 갑작스러운 안면마비, 손발 저림까지 원인을 살핍니다. 경산 하양 갈창림 한의원 두통·신경 질환 진료.'),
 'internal-sleep.html': ('경산 불면증·화병 한의원 | 갈창림 한의원',
   '잠 못 드는 밤, 답답한 가슴, 풀리지 않는 피로를 함께 살핍니다. 경산 하양 갈창림 한의원 불면·스트레스 진료.'),
 'internal-rhinitis.html': ('경산 비염·수족냉증 한의원 | 갈창림 한의원',
   '찬 공기에 예민한 코와 차가운 손발, 원인부터 살핍니다. 비염·수족냉증 침·뜸·부항·한약 치료와 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'diet.html': ('경산 한방 다이어트 | 갈창림 한의원',
   '체중계 숫자보다 건강하게 유지할 수 있는 몸을 목표로 합니다. 맞춤 탕약과 매일 카카오톡 식단 관리, 다이어트 한약의 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'growth.html': ('경산 소아 성장 한의원 | 갈창림 한의원',
   '아이가 가진 성장 가능성을 충분히 키울 수 있도록 성장을 방해하는 요인을 살핍니다. 성장 진료 과정과 성장 한약의 가능한 부작용 안내 — 경산 하양 갈창림 한의원.'),
 'women.html': ('경산 여성 질환 한의원 | 갈창림 한의원',
   '생리통부터 산후 회복, 갱년기까지 시기마다 달라지는 여성의 몸을 살핍니다. 한약·침·뜸 치료와 가능한 부작용 안내 — 경산 하양 갈창림 한의원 여성 질환 진료.'),
 'price.html': ('가격표 · 레이저제모 비용 | 경산 갈창림 한의원',
   '레이저제모 부위별 비용, 리니어펌·볼뉴머·실리프팅, 토닝, 필링·여드름, 라디쥬 등 스킨부스터, 패키지 비용 안내(부가세 포함). 경산 하양 갈창림 한의원.'),
 'column.html': ('원장 칼럼 – 피부미용·건강·질환 정보 | 경산 갈창림 한의원',
   '경산 하양 갈창림 한의원 대표원장이 피부미용, 교통사고, 척추·관절 통증, 내과 질환, 다이어트, 소아·여성 건강에 대해 진료실에서 자주 받는 질문에 직접 답하는 칼럼입니다.'),
 'privacy.html': ('개인정보처리방침 | 갈창림 한의원', '갈창림 한의원 홈페이지 개인정보처리방침.'),
 'terms.html': ('이용약관 | 갈창림 한의원', '갈창림 한의원 홈페이지 이용약관.'),
}

SAME_AS = ['https://blog.naver.com/gal0122', 'https://www.instagram.com/gal__clinic/']   # + place links below
NAVER_LINK = 'https://naver.me/FW6SmWrn'                                  # 네이버 지도 플레이스 (원장님 공유 링크)
KAKAO_LINK = 'https://place.map.kakao.com/628214691'                       # 카카오맵 장소
GOOGLE_LINK = 'https://maps.google.com/?cid=18044492256827464131'          # 구글 지도 (비즈니스 프로필)
CLINIC_ID, SITE_ID = SITE + '/#clinic', SITE + '/#website'
DIRECTOR_ID = SITE + '/doctors.html#director'
LD_DIRECTOR = {'@type': 'Person', '@id': DIRECTOR_ID, 'name': '갈창림', 'jobTitle': '대표원장 (한의사)',
               'url': SITE + '/doctors.html', 'image': SITE + '/assets/director.webp',
               'worksFor': {'@id': CLINIC_ID},
               'alumniOf': {'@type': 'CollegeOrUniversity', 'name': '대구한의대학교 한의과대학'},
               'memberOf': [{'@type': 'OrganizationRole', 'roleName': '정회원·교육위원', 'memberOf': {'@type': 'Organization', 'name': '대한통합레이저의학회'}},
                            {'@type': 'OrganizationRole', 'roleName': '정회원', 'memberOf': {'@type': 'Organization', 'name': '국제레이저미용피부과학회'}}],
               'hasCredential': {'@type': 'EducationalOccupationalCredential', 'name': 'RMSK (미국 근골격 초음파 자격)', 'credentialCategory': 'certification'}}
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
 ('MedicalTherapy', '소화기 질환 치료 (기능성 소화불량·역류성 식도염·과민성 대장 증후군)', 'internal-digestive.html'),
 ('MedicalTherapy', '두통·안면마비·손발 저림 치료', 'internal-neuro.html'),
 ('MedicalTherapy', '불면증·화병·만성 피로 치료', 'internal-sleep.html'),
 ('MedicalTherapy', '비염·수족냉증 치료', 'internal-rhinitis.html'),
 ('MedicalTherapy', '한방 다이어트', 'diet.html'),
 ('MedicalTherapy', '소아 성장 치료', 'growth.html'),
 ('MedicalTherapy', '여성 질환 치료', 'women.html'),
]
SERVICE_LD = {u: (t, n) for t, n, u in SERVICES}
SERVICE_LD.update({
 'booster-plla.html': ('MedicalProcedure', 'PLLA 스킨부스터'), 'booster-keratin.html': ('MedicalProcedure', '케라틴 ANK 약침'),
 'booster-altcore.html': ('MedicalProcedure', '알트코어 스킨부스터'), 'booster-ecm.html': ('MedicalProcedure', 'ECM 진피재생약침'),
 'acne-red.html': ('MedicalProcedure', '여드름 붉은 자국 치료'), 'traffic-treat.html': ('MedicalTherapy', '교통사고 후유증 한방 치료'),
})
SERVICE_LD['booster-pdrn.html'] = ('MedicalProcedure', 'PDRN·엑소좀 스킨부스터')
LD_WEBSITE = {'@type': 'WebSite', '@id': SITE_ID, 'url': SITE + '/', 'name': '갈창림 한의원',
              'alternateName': ['갈창림한의원', '경산 갈창림 한의원'], 'inLanguage': 'ko-KR',
              'publisher': {'@id': CLINIC_ID}}
LD_CLINIC = {
 '@type': 'MedicalClinic', '@id': CLINIC_ID,
 'name': '갈창림 한의원', 'alternateName': ['갈창림한의원', 'Gal Chang Lim Korean Medicine Clinic'],
 'description': SEO['index.html'][1],
 'url': SITE + '/', 'telephone': '+82-53-851-0122',
 'image': SITE + '/assets/og-image.png', 'logo': SITE + '/assets/logo-512.png',
 'address': {'@type': 'PostalAddress', 'streetAddress': '하양읍 동서2길 43, 3층', 'addressLocality': '경산시',
             'addressRegion': '경상북도', 'postalCode': '38417', 'addressCountry': 'KR'},
 'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LNG},
 'openingHoursSpecification': [
   {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:30', 'closes': '13:00'},
   {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '14:00', 'closes': '18:30'},
   {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Saturday', 'Sunday'], 'opens': '08:30', 'closes': '14:00'}],
 'specialOpeningHoursSpecification': [   # 공휴일·임시 휴진일 (진료 일정 페이지와 맞출 것)
   {'@type': 'OpeningHoursSpecification', 'validFrom': '2026-11-01', 'validThrough': '2026-11-01', 'opens': '00:00', 'closes': '00:00'},
   {'@type': 'OpeningHoursSpecification', 'validFrom': '2026-12-25', 'validThrough': '2026-12-25', 'opens': '00:00', 'closes': '00:00'}],
 'medicalSpecialty': ['https://schema.org/Dermatologic', 'https://schema.org/Musculoskeletal'],
 'hasMap': NAVER_LINK,
 'areaServed': [{'@type': 'City', 'name': '경상북도 경산시'}],
 'employee': {'@type': 'Person', '@id': SITE + '/doctors.html#director', 'name': '갈창림', 'jobTitle': '대표원장 (한의사)', 'url': SITE + '/doctors.html',
              'alumniOf': {'@type': 'CollegeOrUniversity', 'name': '대구한의대학교 한의과대학'}},
 'availableService': [{'@type': t, 'name': n, 'url': f'{SITE}/{u}'} for t, n, u in SERVICES],
 'sameAs': SAME_AS + [NAVER_LINK, KAKAO_LINK, GOOGLE_LINK],
}
# breadcrumb label (as shown on each page) -> section page
CRUMB = {'홈': '', '병원소개': 'about.html', '피부미용': 'skin.html', '리프팅': 'design-lifting.html',
         '스킨부스터': 'booster-pdrn.html', '제모': 'hair-removal.html', '색소': 'pigment.html',
         '여드름': 'acne.html', '모공': 'pore.html', '교통사고': 'traffic.html', '통증': 'pain-spine.html', '내과 질환': 'internal-digestive.html',
         '다이어트': 'diet.html', '소아·여성': 'growth.html', '가격표': 'price.html', '원장 칼럼': 'column.html'}
NON_MEDICAL = {'index.html', 'column.html', 'about.html', 'doctors.html', 'equipment.html', 'schedule.html', 'price.html',
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
    wp = {'@type': 'CollectionPage' if slug_ in COL_LISTS else 'WebPage' if slug_ in NON_MEDICAL else 'MedicalWebPage', '@id': url + '#webpage',
          'url': url, 'name': title, 'description': desc, 'inLanguage': 'ko-KR',
          'isPartOf': {'@id': SITE_ID}, 'about': {'@id': CLINIC_ID}, 'dateModified': PAGE_DATE.get(slug_, LASTMOD)}
    if wp['@type'] == 'MedicalWebPage':     # matches the visible "작성·검토 갈창림 대표원장(한의사) · 최종 검토" line
        reviewer = {'@type': 'Person', '@id': DIRECTOR_ID, 'name': '갈창림',
                    'jobTitle': '대표원장 (한의사)', 'url': SITE + '/doctors.html'}
        rv = re.search(r'최종 검토 (\d{4})년 (\d{1,2})월 (\d{1,2})일', body)   # the page's own visible review date
        reviewed = f'{rv.group(1)}-{int(rv.group(2)):02d}-{int(rv.group(3)):02d}' if rv else REVIEWED
        wp.update({'author': reviewer, 'reviewedBy': reviewer, 'lastReviewed': reviewed})
        rs = re.search(r'<section data-refs="true".*?</section>', body, re.S)
        if rs:
            wp['citation'] = [htmlmod.unescape(u) for u in re.findall(r'href="(https?://[^"]+)"', rs.group(0))]
    m = re.search(r'<p style="margin: 0; font-size: 14px; color: #5d655f">(홈 &gt;.*?)</p>', body)
    if slug_ in COL_CRUMBS:     # 원장 칼럼 pages: category names clash with section names (피부미용 -> skin.html)
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(COL_CRUMBS[slug_])]})
        wp['breadcrumb'] = {'@id': url + '#breadcrumb'}
    elif m:
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
    if COL_LISTS.get(slug_):
        graph.append({'@type': 'ItemList', '@id': url + '#posts', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': f"{SITE}/{p['file']}", 'name': p['title']}
            for i, p in enumerate(COL_LISTS[slug_])]})
        wp['mainEntity'] = {'@id': url + '#posts'}
    if slug_ in POST_META:
        pm = POST_META[slug_]
        if pm.get('condition'):     # 질환 칼럼: the page is about this condition, written by the clinic
            wp['about'] = {'@type': 'MedicalCondition', 'name': pm['condition']}
            wp['mentions'] = {'@id': CLINIC_ID}
        if pm.get('keyword'):
            wp['keywords'] = pm['keyword']
        wp.update({'headline': pm['title'], 'datePublished': pm['date'], 'dateModified': max(pm['date'], pm['reviewed'])})
    if slug_ in SERVICE_LD:
        t, n = SERVICE_LD[slug_]
        graph.append({'@type': t, '@id': url + '#service', 'name': n, 'url': url, 'description': desc})
        wp['mainEntity'] = {'@id': url + '#service'}
    if slug_ in POST_META:
        pm = POST_META[slug_]
        graph.append({'@type': 'BlogPosting', '@id': url + '#article', 'headline': pm['title'], 'description': pm['description'],
                      'url': url, 'mainEntityOfPage': {'@id': url + '#webpage'}, 'inLanguage': 'ko-KR',
                      'image': f"{SITE}/{OG_IMG.get(slug_, 'assets/og-image.png')}",
                      'datePublished': pm['date'], 'dateModified': max(pm['date'], pm['reviewed']),
                      'author': {'@id': DIRECTOR_ID}, 'publisher': {'@id': CLINIC_ID}, 'articleSection': pm['category'],
                      **({'citation': [u for _, u in pm['refs']]} if pm.get('refs') else {})})
        wp['mainEntity'] = {'@id': url + '#article'}
    if slug_ == 'doctors.html':
        wp['mainEntity'] = {'@id': DIRECTOR_ID}
        graph.append(LD_DIRECTOR)
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
BLOB = {k: S + v.split('/scratchpad', 1)[1] if '/scratchpad/' in v else v for k, v in BLOB.items()}   # MAP was written for the first work folder

canvas = json.load(open(f'{G}/project/canvas.json', encoding='utf-8'))
order = canvas['order']
NON_PAGES = {'Popup.dc.html', 'ColumnPost.dc.html'}          # design-only boards, not web pages
pages = [f for f in order if f not in NON_PAGES]


def slug(dc):
    name = dc.replace('.dc.html', '')
    if name == 'Main':
        return 'index.html'
    return re.sub(r'(?<=[a-z])(?=[A-Z])', '-', name).lower() + '.html'


SLUG = {f: slug(f) for f in pages}
SLUG['ColumnPost.dc.html'] = 'column.html'   # template board; sample links fall back to the list
# ---- 원장 칼럼 posts (galch/columns/*.md) ----
sys.path.insert(0, S)
import columns
ALL_POSTS = columns.load_posts(f'{G}/columns')
POSTS = [p for p in ALL_POSTS if p['date'] <= LASTMOD]   # a post goes live on its date (예약 발행)
POST_META = {p['file']: p for p in POSTS}
CATS = columns.used_categories(POSTS)                 # categories with at least one post
COL_LISTS = {columns.cat_file(k): ([p for p in POSTS if p['cat_key'] == k] if k != 'all' else POSTS)
             for k in ['all'] + [k for k, _ in CATS]}  # list pages -> the posts they show
HOME_C, COL_C = ('홈', SITE + '/'), ('원장 칼럼', SITE + '/column.html')
COL_CRUMBS = {columns.cat_file(k): [HOME_C, COL_C, (n, f'{SITE}/{columns.cat_file(k)}')] for k, n in CATS}
COL_CRUMBS.update({p['file']: [HOME_C, COL_C, (p['category'], f"{SITE}/{columns.cat_file(p['cat_key'])}"),
                               (p['title'], f"{SITE}/{p['file']}")] for p in POSTS})

for k, n in CATS:
    SEO[columns.cat_file(k)] = (f'{n} 칼럼 | 원장 칼럼 · 경산 갈창림 한의원', f'{columns.CAT_INTRO[k]} 경산 하양 갈창림 한의원.')

def col_links(body):
    """Menu links 'column.html#skin' -> the category page; drop categories that have no post yet."""
    have = {k for k, _ in CATS}
    for k, _ in columns.CATEGORIES:
        if k not in have:
            body = re.sub(rf'<a href="column\.html#{k}"[^>]*>[^<]*</a>\n?', '', body)
    body = re.sub(r'href="column\.html#([a-z-]+)"', lambda m: f'href="{columns.cat_file(m.group(1))}"', body)
    assert 'column.html#' not in body
    # links from service pages to a post (<a data-col="slug" …>): shown only once the post is published
    live = {p['slug'] for p in POSTS}
    def col_section(m):   # '원장 칼럼에서 더 알아보기' lists: published posts only; no section until one is out
        sec = re.sub(r'<li[^>]*>\s*<a data-col="([a-z0-9-]+)"[^>]*>[^<]*</a>\s*</li>\n?',
                     lambda x: x.group(0).replace(f' data-col="{x.group(1)}"', '') if x.group(1) in live else '', m.group(0))
        return sec.replace(' data-col-section="true"', '') if '<li' in sec else ''
    body = re.sub(r'<section data-col-section="true">.*?</section>\n*', col_section, body, flags=re.S)
    body = re.sub(r'<p[^>]*>\s*<a data-col="([a-z0-9-]+)"[^>]*>[^<]*</a>\s*</p>\n?',
                  lambda m: m.group(0).replace(f' data-col="{m.group(1)}"', '') if m.group(1) in live else '', body)
    assert 'data-col=' not in body
    return body

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(f'{OUT}/assets')
open(f'{OUT}/.nojekyll', 'w').close()

asset_url = {}
IMG_SIZE = {}
IMG_SMALL = {}


def img_size(path):
    if path.endswith('.svg'):
        t = open(path, encoding='utf-8').read(3000)
        w = re.search(r'<svg[^>]*?\swidth="([\d.]+)', t); h = re.search(r'<svg[^>]*?\sheight="([\d.]+)', t)
        if w and h:
            return round(float(w.group(1))), round(float(h.group(1)))
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', t)
        return (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else None
    if path.endswith('.woff2'):
        return None
    with Image.open(path) as im:
        return im.size


def img_attrs(body):
    """width/height on every image (no layout shift); lazy loading below the first screen (after the hero section)."""
    m = re.search(r'</section>', body)
    fold = m.end() if m else 0
    def one(mm):
        tag = mm.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            return tag
        add = ''
        size = IMG_SIZE.get(src.group(1))
        if size and ' width=' not in tag and ' height=' not in tag:
            add += f' width="{size[0]}" height="{size[1]}"'
        small = IMG_SMALL.get(src.group(1))
        if small and 'srcset=' not in tag:
            add += f' srcset="{small[0]} {small[1]}w, {src.group(1)} {small[2]}w" sizes="(max-width: 640px) 100vw, {small[2]}px"'
        if mm.start() > fold and 'loading=' not in tag:
            add += ' loading="lazy" decoding="async"'
        return tag[:4] + add + tag[4:]
    return re.sub(r'<img\b[^>]*>', one, body)


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
        if im.width > 1000:  # a smaller copy for phones (srcset)
            sm = base + '-800.webp'
            im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(f'{OUT}/assets/{sm}', 'WEBP', quality=84)
            IMG_SMALL[f'assets/{name}'] = (f'assets/{sm}', 800, im.width)
    asset_url[bid] = f'assets/{name}'
    IMG_SIZE[asset_url[bid]] = img_size(f'{OUT}/assets/{name}')
    return asset_url[bid]


# favicon from the logo mark
fav = Image.open(f'{G}/img/logo-mark.png').convert('RGBA')
fav.thumbnail((192, 192))
fav.save(f'{OUT}/assets/favicon.png')
_ico = Image.new('RGBA', (max(fav.size),) * 2, (0, 0, 0, 0)); _ico.paste(fav, ((_ico.width - fav.width) // 2, (_ico.height - fav.height) // 2), fav)
_ico.save(f'{OUT}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])  # crawlers look at /favicon.ico first
sq = Image.new('RGB', (512, 512), '#faf7f0')
mk = Image.open(f'{G}/img/logo-mark.png').convert('RGBA')
mk.thumbnail((400, 400))
sq.paste(mk, ((512 - mk.width) // 2, (512 - mk.height) // 2), mk)
sq.save(f'{OUT}/assets/logo-512.png', optimize=True)

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
foot = '경상북도 경산시 하양읍 동서2길 43, 3층  ·  053-851-0122'
fnt2 = font(28, 500)
w2 = d.textlength(foot, font=fnt2)
d.text(((1200 - w2) / 2, 580), foot, font=fnt2, fill='#ffffff')
og.save(f'{OUT}/assets/og-image.png', optimize=True)

# per-page share images (KakaoTalk·Naver previews): section, page title, one line — text only, no photos
OG_IMG = {}
os.makedirs(f'{OUT}/assets/og', exist_ok=True)
OG_MARK = Image.open(f'{G}/img/logo-mark.png').convert('RGBA')
OG_MARK.thumbnail((52, 52))


def og_wrap(d, text, fnt, width, max_lines):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
            continue
        if cur:
            lines.append(cur)
        cur = w
        while d.textlength(cur, font=fnt) > width:      # a single long word: break by characters
            i = len(cur)
            while i > 1 and d.textlength(cur[:i], font=fnt) > width:
                i -= 1
            lines.append(cur[:i]); cur = cur[i:]
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while d.textlength(lines[-1] + '…', font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip(' ,·') + '…'
    return lines


def make_og(out, f, body):
    if out in ('index.html', 'privacy.html', 'terms.html'):
        return
    if out in POST_META:
        pm = POST_META[out]
        eyebrow, title, sub, size = '원장 칼럼 · ' + pm['category'], pm['title'], '', 58
    else:
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        if not h1:
            return
        title = plain(h1.group(1))
        after = body[h1.end():h1.end() + 1500]
        sp = re.search(r'<p[^>]*>(.*?)</p>', after, re.S)
        sub = plain(sp.group(1)) if sp else ''
        raw = re.sub(r'^\d+(-\d+)?\s*', '', canvas['boards'][f]['title'])
        parts = raw.split(' · ')
        eyebrow = ' · '.join(dict.fromkeys(parts[:-1])) or '갈창림 한의원'
        if out in COL_LISTS:
            eyebrow = '원장 칼럼'
        size = 72
    im = Image.new('RGB', (1200, 630), '#faf7f0')
    d = ImageDraw.Draw(im)
    d.ellipse([960, 300, 1360, 700], fill='#efe9dc')
    tf, sf = font(size, 800), font(32, 500)
    tl = og_wrap(d, title, tf, 1020, 3 if out in POST_META else 2)
    sl = og_wrap(d, sub, sf, 1020, 2) if sub else []
    lh = round(size * 1.28)
    block = 40 + 30 + len(tl) * lh + (14 + len(sl) * 46 if sl else 0)     # eyebrow + rule + title + sub
    y = max(56, (540 - block) // 2)
    d.text((80, y), eyebrow, font=font(30, 700), fill='#7a6b42')
    d.rectangle([80, y + 50, 128, y + 54], fill='#2f5241')
    y += 74
    for ln in tl:
        d.text((80, y), ln, font=tf, fill='#24302a')
        y += lh
    if sl:
        y += 14
        for ln in sl:
            d.text((80, y), ln, font=sf, fill='#4d554f')
            y += 46
    d.rectangle([0, 540, 1200, 630], fill='#2f5241')
    d.rounded_rectangle([80, 555, 140, 615], radius=12, fill='#faf7f0')
    im.paste(OG_MARK, (80 + (60 - OG_MARK.width) // 2, 555 + (60 - OG_MARK.height) // 2), OG_MARK)
    d.text((160, 566), '갈창림 한의원', font=font(32, 700), fill='#ffffff')
    right = '경산 하양 · 053-851-0122'
    rf = font(26, 500)
    d.text((1120 - d.textlength(right, font=rf), 572), right, font=rf, fill='#d7c9a7')
    name = 'assets/og/' + out.replace('.html', '.jpg')
    im.save(f'{OUT}/{name}', 'JPEG', quality=88, optimize=True, progressive=True)
    OG_IMG[out] = name


def fix_links(html):
    def rep2(m):
        name, frag = m.group(2), m.group(3) or ''
        target = SLUG[name + ".dc.html"]
        return f'{m.group(1)}="{"/" if target == "index.html" else target}{frag}"'
    return re.sub(r'(href|action)="([A-Za-z]+)\.dc\.html(#[\w-]+)?"', lambda m: rep2(m), html)


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
// calendars (진료 일정, 휴진 팝업): mark today's date in Korean time
(function () {
  var k = new Date(Date.now() + 9 * 3600 * 1000);
  var y = k.getUTCFullYear(), m = k.getUTCMonth() + 1, d = String(k.getUTCDate());
  [].forEach.call(document.querySelectorAll('table.cal, table.pop-cal'), function (t) {
    var c = t.querySelector('caption'), mm = c && c.textContent.match(/(\d{4})년\s*(\d{1,2})월/);
    if (!mm || +mm[1] !== y || +mm[2] !== m) return;
    [].forEach.call(t.querySelectorAll('td'), function (td) {
      var n = td.querySelector('strong, b');
      if (!n || n.textContent.trim() !== d) return;
      td.classList.add('is-today');
      td.setAttribute('aria-current', 'date');
      if (t.classList.contains('cal')) {
        var s = document.createElement('span');
        s.className = 'today-tag'; s.textContent = '오늘';
        n.insertAdjacentElement('afterend', s);
      }
    });
  });
})();
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
      // bar along the bottom (phones), or its folded tab in the bottom-right corner
      if (r.height && r.top > window.innerHeight / 2 && (r.width > window.innerWidth / 2 || qn.classList.contains('qn-min')))
        bottom = Math.min(bottom, r.top);
    }
    nav.style.boxSizing = 'border-box';
    nav.style.maxHeight = Math.max(160, Math.ceil(bottom - top) + 2) + 'px';  // tuck 2px under the bar: no gap
  }
  d.addEventListener('toggle', fit);
  window.addEventListener('resize', fit);
  window.addEventListener('qn-change', fit);
})();
// quick bar (블로그 · 톡톡상담 · 전화): fold / unfold, remembered on this device while browsing
(function () {
  var qn = document.querySelector('.qn'), tg = qn && qn.querySelector('.qn-tg');
  if (!tg) return;
  var KEY = 'galclinic-qn-min', txt = tg.querySelector('.qn-tg-txt');
  function set(min, save) {
    qn.classList.toggle('qn-min', min);
    tg.setAttribute('aria-expanded', String(!min));
    tg.setAttribute('aria-label', min ? '바로가기 펼치기' : '바로가기 접기');
    if (txt) txt.textContent = min ? '펼치기' : '접기';
    if (save) { try { if (min) localStorage.setItem(KEY, '1'); else localStorage.removeItem(KEY); } catch (e) {} }
    window.dispatchEvent(new Event('qn-change'));
  }
  var min = false;
  try { min = localStorage.getItem(KEY) === '1'; } catch (e) {}
  if (min) set(true, false);
  tg.addEventListener('click', function () { set(!qn.classList.contains('qn-min'), true); });
})();
</script>'''

MAP_JS = f'''<script>
(function () {{
  // the Naver map script (~300 KB) loads only when a map box comes near the screen
  var boxes = document.querySelectorAll('[data-naver-map]');
  if (!boxes.length) return;
  window.navermap_authFailure = function () {{
    document.querySelectorAll('[data-naver-map] > .nmap').forEach(function (el) {{ el.remove(); }});
  }};
  var started = false;
  function load() {{
    if (started) return;
    started = true;
    var s = document.createElement('script');
    s.src = 'https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId={NAVER_KEY}';
    s.async = true;
    s.onload = init;
    document.body.appendChild(s);
  }}
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function (es) {{
      if (es.some(function (e) {{ return e.isIntersecting; }})) {{ io.disconnect(); load(); }}
    }}, {{ rootMargin: '400px 0px' }});
    boxes.forEach(function (b) {{ io.observe(b); }});
  }} else {{
    load();
  }}
  function init() {{
  if (!window.naver || !naver.maps) return;
  var pin = '<div style="transform:translate(-50%,calc(-100% - 8px));display:flex;flex-direction:column;align-items:center">'
    + '<div style="white-space:nowrap;padding:8px 14px;border-radius:999px;background:#2f5241;color:#ffffff;font:700 13px Pretendard,sans-serif;box-shadow:0 6px 16px rgba(36,48,42,.25)">갈창림 한의원</div>'
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
  }}
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
    # drop notices whose end date (data-until, Korean time) has passed, so stale notices don't sit in the page source
    _today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date().isoformat()
    for _m in list(re.finditer(r'<div class="pop" [^>]*data-until="(\d{4}-\d{2}-\d{2})"', layer)):
        if _m.group(1) < _today:
            _old = balanced_div(layer, layer.index(_m.group(0)))
            layer = layer.replace(_old, '', 1)
    POPUP_HTML = ('<div class="pop-overlay" id="site-popups" hidden>\n' + blobs(fix_links(layer)) + '\n</div>')
    pcss = re.search(r'<style>(.*?)</style>', psrc, re.S).group(1)
    keep = [l for l in pcss.strip().splitlines()
            if not l.startswith(('@font-face', 'body{', '.pop-stage{'))]
    POPUP_CSS = '\n'.join(keep) + '''
.pop-overlay{position:fixed;top:0;left:0;right:0;bottom:0;z-index:100;display:flex;justify-content:center;align-items:flex-start;padding:110px 20px 40px;box-sizing:border-box;overflow-y:auto;background:rgba(36,48,42,.55);font-family:'Pretendard','Pretendard Variable',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;color:#24302a;line-height:1.6}
.pop-overlay[hidden]{display:none}
@media (max-width:640px){.pop-overlay{align-items:flex-start;padding:16px 16px 76px}.pop-layer{width:100%;margin:auto 0}.pop-cal td{height:36px}.pop-body{gap:12px}.pop-reasons li{padding:9px 14px}.pop-open{padding:11px 14px}.pop{flex:0 1 auto;width:100%;max-width:380px}.pop-body{padding:24px 22px 20px}.pop-date{font-size:30px}.pop-title{font-size:20px!important}}'''

NOTICE_BAR = ('<div class="notice-bar" id="site-notice" role="region" aria-label="공지" hidden>'
              '<button type="button" class="nb-open"><span class="nb-tag">공지</span><span class="nb-text"></span><span class="nb-more">보기 ›</span></button>'
              '<button type="button" class="nb-x" aria-label="공지 24시간 동안 닫기">×</button></div>\n')
POPUP_CSS += '''
.notice-bar{display:none}
.notice-bar:not([hidden]){display:flex;align-items:stretch;background:#2f5241;color:#ffffff;font-family:'Pretendard','Pretendard Variable',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif}
.notice-bar button{border:0;background:transparent;color:inherit;font:inherit;cursor:pointer}
.nb-open{flex:1 1 auto;min-width:0;display:flex;align-items:center;gap:8px;min-height:42px;padding:0 4px 0 16px;text-align:left;font-size:13px;font-weight:600}
.nb-tag{flex:0 0 auto;padding:2px 8px;border-radius:999px;background:#d7c9a7;color:#24302a;font-size:11px;font-weight:700}
.nb-text{flex:1 1 auto;min-width:0;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.nb-more{flex:0 0 auto;font-size:12px;color:#d7c9a7}
.nb-x{flex:0 0 44px;font-size:20px!important;line-height:1}
.notice-bar button:focus-visible{outline:2px solid #d7c9a7;outline-offset:-2px}
@media (min-width:641px){.nb-open{padding-left:max(16px,calc((100vw - 1240px) / 2 + 24px));font-size:14px}.nb-x{margin-right:max(0px,calc((100vw - 1240px) / 2))}}'''

POPUP_JS = '''<script>
(function () {
  var overlay = document.getElementById('site-popups');
  if (!overlay) return;
  var layer = overlay.querySelector('.pop-layer');
  var bar = document.getElementById('site-notice');
  var KEY = 'galclinic-popup-hide-', BARKEY = 'galclinic-notice-hide';
  var DAY = 24 * 60 * 60 * 1000;
  var now = Date.now();
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  // notices outside their dates (data-from / data-until, Korean time) are not shown
  var all = [].slice.call(overlay.querySelectorAll('.pop')).filter(function (p) {
    var from = p.getAttribute('data-from'), until = p.getAttribute('data-until');
    var early = from && now < new Date(from + 'T00:00:00+09:00').getTime();
    var expired = until && now > new Date(until + 'T23:59:59+09:00').getTime();
    if (early || expired) { p.parentNode.removeChild(p); return false; }
    return true;
  });
  var mq = window.matchMedia('(max-width: 640px)');
  var open = [];
  function layout() {
    all.forEach(function (p) { p.style.display = 'none'; });
    open.forEach(function (p, i) { p.style.display = (!mq.matches || i === 0) ? '' : 'none'; });
    overlay.hidden = open.length === 0;
    document.documentElement.style.overflow = open.length ? 'hidden' : '';
  }
  function show(list) {
    open = list.slice(); layout();
    if (open.length) { var c = open[0].querySelector('.pop-close'); if (c) c.focus({ preventScroll: true }); }
  }
  function closePop(p, remember) {
    if (remember) save(KEY + p.getAttribute('data-pop'), String(Date.now() + DAY));
    open = open.filter(function (x) { return x !== p; });
    layout();
    if (!open.length && bar && !bar.hidden) bar.querySelector('.nb-open').focus({ preventScroll: true });
  }
  all.forEach(function (p) {
    p.querySelector('.pop-close').addEventListener('click', function () {
      closePop(p, p.querySelector('.pop-check input').checked);
    });
  });
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay || e.target === layer) open.slice().forEach(function (p) { closePop(p, false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && open.length) closePop(open[0], false);
  });
  if (mq.addEventListener) mq.addEventListener('change', layout);
  // a thin notice bar on every device instead of popups covering the page (Google's intrusive-interstitial
  // guideline); tapping it opens the notices
  if (bar) {
    var labels = all.map(function (p) { return p.getAttribute('data-label') || ''; }).filter(Boolean);
    bar.querySelector('.nb-text').textContent = labels.join(' · ');
    bar.hidden = !all.length || Number(load(BARKEY) || 0) > now;
    bar.querySelector('.nb-open').addEventListener('click', function () { show(all); });
    bar.querySelector('.nb-x').addEventListener('click', function () {
      save(BARKEY, String(Date.now() + DAY)); bar.hidden = true;
    });
  }
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

# 원장 칼럼 list pages (column.html, column-<category>.html): "더 보기" paging + full-text search.
# The search index (column-search.json) is fetched on the first search; ?q=단어 opens with results.
COLUMN_JS = r"""<script>
(function () {
  var box = document.querySelector('[data-column-list]');
  if (!box) return;
  var on = document.querySelector('.col-chips .on');   // keep the current category chip in view on phones
  if (on) {
    var nav = on.parentNode;
    nav.scrollLeft += on.getBoundingClientRect().left - nav.getBoundingClientRect().left - (nav.clientWidth - on.offsetWidth) / 2;
  }
  var list = box.querySelector('.col-list'), res = box.querySelector('.col-results');
  var moreWrap = box.querySelector('.col-more-wrap'), more = box.querySelector('.col-more');
  var form = document.querySelector('.col-search'), q = form && form.querySelector('input');
  var items = [].slice.call(list.querySelectorAll('.col-item'));
  var PAGE = 10, shown = PAGE;
  function paging() {
    items.forEach(function (it, i) { it.hidden = i >= shown; });
    moreWrap.hidden = items.length <= shown;
    more.textContent = '칼럼 더 보기 (' + Math.max(0, items.length - shown) + ')';
  }
  more.addEventListener('click', function () {
    var first = items[shown];
    shown += PAGE; paging();
    var a = first && first.querySelector('a');
    if (a) a.focus({ preventScroll: true });
  });
  paging();
  if (!q) return;

  function norm(s) { return (s || '').toLowerCase().replace(/\s+/g, ''); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function hl(s, re) {
    var out = '', last = 0;
    s.replace(re, function (m, off) { out += esc(s.slice(last, off)) + '<mark>' + esc(m) + '</mark>'; last = off + m.length; return m; });
    return out + esc(s.slice(last));
  }
  var idx = null, wait = null;
  function load() {
    if (!wait) wait = fetch('column-search.json').then(function (r) { if (!r.ok) throw r.status; return r.json(); })
      .catch(function () {          // index unreachable: search the titles and summaries on this page
        return items.map(function (it) {
          return { u: it.querySelector('a').getAttribute('href'), t: it.querySelector('h2').textContent,
                   c: it.querySelector('.col-tag').textContent, d: it.querySelector('.col-date').textContent.split(' ')[0],
                   s: it.querySelector('p').textContent, x: '' };
        });
      })
      .then(function (d) {
        idx = d.map(function (p) { p.n = [norm(p.t), norm(p.c), norm(p.s), norm(p.x)]; return p; });
      });
    return wait;
  }
  function snippet(p, terms) {        // a piece of the summary (or else the body) around the first word found
    var src = [p.s, p.x];
    for (var k = 0; k < 2; k++) {
      var s = src[k], ls = s.toLowerCase(), at = -1;
      for (var i = 0; i < terms.length && at < 0; i++) at = ls.indexOf(terms[i]);
      if (at < 0) continue;
      if (at < 50) return k ? s.slice(0, 150) + (s.length > 150 ? ' …' : '') : s;
      var st = at - 24, sp = s.indexOf(' ', st);
      if (sp > -1 && sp < at) st = sp + 1;
      return '… ' + s.slice(st, st + 150) + (st + 150 < s.length ? ' …' : '');
    }
    return p.s;
  }
  function render(v) {
    var terms = v.toLowerCase().split(/\s+/).filter(Boolean);
    var re = new RegExp(terms.map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|'), 'gi');
    var hits = [];
    idx.forEach(function (p, i) {
      var sc = 0;
      for (var j = 0; j < terms.length; j++) {
        var f = p.n.map(function (n) { return n.indexOf(terms[j]) > -1; });
        if (!(f[0] || f[1] || f[2] || f[3])) return;      // every word has to appear somewhere in the post
        sc += (f[0] ? 8 : 0) + (f[1] ? 4 : 0) + (f[2] ? 2 : 0) + (f[3] ? 1 : 0);
      }
      hits.push({ p: p, sc: sc, i: i });
    });
    hits.sort(function (a, b) { return b.sc - a.sc || a.i - b.i; });
    var scope = /column-/.test(location.pathname) ? '전체 칼럼에서 ' : '';
    var h = '<p class="col-count"><span>' + scope + '‘' + esc(v) + '’ 검색 결과 <strong>' + hits.length + '</strong>건</span>'
          + '<button type="button" class="col-btn col-clear">검색 지우기</button></p>';
    if (hits.length) {
      h += '<div class="col-list">' + hits.map(function (x) {
        var p = x.p;
        return '<article class="col-item"><a href="' + esc(p.u) + '"><span class="col-tag">' + esc(p.c) + '</span>'
             + '<h2>' + hl(p.t, re) + '</h2><p class="col-snip">' + hl(snippet(p, terms), re) + '</p>'
             + '<span class="col-date">' + esc(p.d) + ' · 갈창림 대표원장</span></a></article>';
      }).join('') + '</div>';
    } else {
      h += '<p class="col-empty">‘' + esc(v) + '’에 대한 칼럼은 아직 없습니다. 다른 단어로 찾아보시거나, 전화·네이버상담으로 물어보시면 답해 드립니다.</p>';
    }
    res.innerHTML = h;
    res.hidden = false; list.hidden = true; moreWrap.hidden = true;
  }
  function reset() { res.hidden = true; res.innerHTML = ''; list.hidden = false; paging(); }
  function sync(v) { try { history.replaceState(null, '', v ? '?q=' + encodeURIComponent(v) : location.pathname); } catch (e) {} }
  var timer = 0;
  function run(now) {
    clearTimeout(timer);
    timer = setTimeout(function () {
      var v = q.value.trim();
      sync(v);
      if (!v) return reset();
      load().then(function () { if (q.value.trim() === v) render(v); });
    }, now ? 0 : 150);
  }
  q.addEventListener('input', function () { run(false); });
  form.addEventListener('submit', function (e) { e.preventDefault(); run(true); q.blur(); });
  res.addEventListener('click', function (e) {
    if (e.target.closest('.col-clear')) { q.value = ''; run(true); q.focus(); }
  });
  var start = new URLSearchParams(location.search).get('q');
  if (start) { q.value = start; run(true); }
})();
</script>"""

report = []

# Per-page "last changed" date for sitemap lastmod and dateModified: only moves when the page's own
# content (<main>) changes, so a rebuild doesn't make every page look new to search engines.
import hashlib
LASTMOD_DB = f'{G}/lastmod.json'
_db_new = not os.path.exists(LASTMOD_DB)
PAGE_DB = {} if _db_new else json.load(open(LASTMOD_DB, encoding='utf-8'))
PAGE_DATE = {}
SEED_DATE = '2026-10-14'      # first run: the last day the whole site really changed


def page_date(out, body):
    m = re.search(r'<main>(.*)</main>', body, re.S)
    h = hashlib.sha1(re.sub(r'\s+', ' ', m.group(1) if m else body).encode('utf-8')).hexdigest()[:16]
    old = PAGE_DB.get(out)
    if old and old['h'] == h:
        d = old['d']
    elif out in POST_META:
        d = max(POST_META[out]['date'], POST_META[out]['reviewed'])
    elif not old and _db_new:
        rv = re.search(r'최종 검토 (\d{4})년 (\d{1,2})월 (\d{1,2})일', body)
        d = f'{rv.group(1)}-{int(rv.group(2)):02d}-{int(rv.group(3)):02d}' if rv else SEED_DATE
    else:
        d = LASTMOD
    PAGE_DB[out] = {'h': h, 'd': d}
    PAGE_DATE[out] = d
    return d


def build_page(f, out=None, transform=None, seo=None):
    out = out or SLUG[f]
    src = open(f'{G}/project/{f}', encoding='utf-8').read()
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    # extra helmet styles (e.g. Privacy/Terms media rule) live in the same <style>; also keep any 2nd style block
    extra = re.findall(r'<style>(.*?)</style>', src.split('</helmet>')[0], re.S)[1:]
    is_home = f == 'Main.dc.html'
    style = blobs('\n'.join([style] + extra + ([POPUP_CSS] if is_home and POPUP_HTML else [])))
    body = src.split('</helmet>', 1)[1].split('</x-dc>', 1)[0]
    if transform:
        body = transform(body)
    body = col_links(fix_links(body))
    body = body.replace('onClick="{{ prev }}"', 'onclick="slide(this,-1)"').replace('onClick="{{ next }}"', 'onclick="slide(this,1)"')
    body = img_attrs(blobs(body))
    has_map = 'data-naver-map' in body
    if has_map:
        body = body.replace('<span style="font-size: 13px; color: #5d655f">실제 홈페이지에서 지도가 표시됩니다</span>', FALLBACK)
    assert '{{' not in body and '/_blob/' not in body and '.dc.html' not in body, f

    raw = re.sub(r'^\d+\s*', '', canvas['boards'][f]['title'])
    page = raw.split(' · ')[-1]
    title, desc = seo or SEO.get(out, (f'{page} | 갈창림 한의원', f'{raw} — 경산 하양 갈창림 한의원'))
    url = SITE + '/' + ('' if out == 'index.html' else out)
    extra_head = ''
    if is_home:
        for v in ([NAVER_VERIFY] if isinstance(NAVER_VERIFY, str) else NAVER_VERIFY):
            extra_head += f'<meta name="naver-site-verification" content="{v}">\n'
        if GOOGLE_VERIFY:
            extra_head += f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">\n'
    page_date(out, body)
    make_og(out, f, body)
    ld, n_faq = page_ld(out, title, desc, url, body)
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
<meta property="og:site_name" content="갈창림 한의원">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{OG_IMG.get(out, 'assets/og-image.png')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="갈창림 한의원 원장 칼럼" href="{SITE}/rss.xml">
{extra_head}<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<link rel="preload" href="assets/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin>
<style>
{style.strip()}
img[width][height]{{height:auto}}
</style>
</head>
<body>
{NOTICE_BAR if is_home and POPUP_HTML else ''}{body.strip()}
{POPUP_HTML if is_home else ''}
{BASE_JS}
{POPUP_JS if is_home and POPUP_HTML else ''}
{MAP_JS if has_map else ''}
{COLUMN_JS if out in COL_LISTS else ''}
</body>
</html>
'''
    open(f'{OUT}/{out}', 'w', encoding='utf-8').write(html)
    report.append((out, len(html) // 1024, has_map, n_faq))


POST_LINK, CAT_LINK = (lambda p: p['file']), columns.cat_file


def list_transform(key):
    return lambda b: columns.fill(b, columns.list_regions(POSTS, key, POST_LINK, CAT_LINK))


for f in pages:
    build_page(f, transform=list_transform('all') if f == 'Column.dc.html' else None)
for k, n in CATS:                                     # one list page per category: column-skin.html …
    build_page('Column.dc.html', out=columns.cat_file(k), transform=list_transform(k))
for p in POSTS:
    build_page('ColumnPost.dc.html', out=p['file'],
               transform=lambda b, p=p: columns.fill(b, columns.regions(p, POSTS, lambda h: h, POST_LINK, CAT_LINK)),
               seo=(f"{p.get('seo_title') or p['title']} | 갈창림 한의원", p['description']))
json.dump(columns.search_index(POSTS), open(f'{OUT}/column-search.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'))

# rss.xml — 원장 칼럼 (newest first), for Naver Search Advisor
import email.utils
def rfc822(day):
    dt = datetime.datetime.fromisoformat(day + 'T09:40:00+09:00')
    return email.utils.format_datetime(dt)
esc = lambda t: htmlmod.escape(t, quote=False)
items = ''.join(
    f"<item>\n<title>{esc(p['title'])}</title>\n<link>{SITE}/{p['file']}</link>\n<guid isPermaLink=\"true\">{SITE}/{p['file']}</guid>\n"
    f"<category>{esc(p['category'])}</category>\n<pubDate>{rfc822(p['date'])}</pubDate>\n<description>{esc(p['summary'])}</description>\n</item>\n"
    for p in sorted(POSTS, key=lambda q: q['date'], reverse=True))
rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
       f'<title>갈창림 한의원 원장 칼럼</title>\n<link>{SITE}/column.html</link>\n'
       f'<atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>\n'
       f'<description>{esc(columns.CAT_INTRO["all"])}</description>\n<language>ko</language>\n'
       f'<lastBuildDate>{rfc822(max(p["date"] for p in POSTS))}</lastBuildDate>\n{items}</channel>\n</rss>\n')
open(f'{OUT}/rss.xml', 'w', encoding='utf-8').write(rss)

# sitemap.xml + robots.txt for Naver Search Advisor / Google Search Console
urls = [(SITE + '/' + ('' if SLUG[f] == 'index.html' else SLUG[f]), PAGE_DATE[SLUG[f]]) for f in pages
        if SLUG[f] not in ('privacy.html', 'terms.html')]
json.dump({k: PAGE_DB[k] for k in sorted(PAGE_DB)}, open(LASTMOD_DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
urls += [(f'{SITE}/{columns.cat_file(k)}', PAGE_DATE[columns.cat_file(k)]) for k, _ in CATS]
urls += [(f"{SITE}/{p['file']}", PAGE_DATE[p['file']]) for p in POSTS]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, lm in urls:
    sm.append(f'  <url><loc>{u}</loc><lastmod>{lm}</lastmod></url>')
sm.append('</urlset>')
open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
AI_BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
           'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot', 'Applebot-Extended',
           'Bingbot', 'Googlebot', 'Yeti', 'Daumoa']
robots = ('User-agent: *\nAllow: /\nDisallow: /column-search.json\n\n'
          '# Search engines and AI search / answer services are welcome to read this site\n'
          + ''.join(f'User-agent: {b}\n' for b in AI_BOTS) + 'Allow: /\nDisallow: /column-search.json\n\n'
          f'Sitemap: {SITE}/sitemap.xml\n')
open(f'{OUT}/robots.txt', 'w', encoding='utf-8').write(robots)
open(f'{OUT}/{INDEXNOW_KEY}.txt', 'w', encoding='utf-8').write(INDEXNOW_KEY)
open(f'{OUT}/CNAME', 'w', encoding='utf-8').write(DOMAIN + '\n')   # GitHub Pages custom domain

# llms.txt — plain-language summary for AI assistants (https://llmstxt.org)
GROUPS = [('병원 안내', ['about.html', 'doctors.html', 'equipment.html', 'schedule.html', 'price.html']),
          ('피부미용', ['skin.html', 'hair-removal.html', 'design-lifting.html', 'thread-lifting.html',
                    'booster-pdrn.html', 'booster-plla.html', 'booster-keratin.html', 'booster-altcore.html',
                    'booster-ecm.html', 'pigment.html', 'mole.html', 'acne.html', 'acne-red.html',
                    'acne-scar.html', 'pore.html']),
          ('교통사고 · 통증', ['traffic.html', 'traffic-process.html', 'traffic-treat.html', 'pain-spine.html',
                         'pain-joint.html']),
          ('내과 질환', ['internal-digestive.html', 'internal-neuro.html', 'internal-sleep.html', 'internal-rhinitis.html']),
          ('다이어트 · 소아 · 여성', ['diet.html', 'growth.html', 'women.html']),
          ('원장 칼럼', ['column.html'] + [columns.cat_file(k) for k, _ in CATS] + [p['file'] for p in POSTS])]
grouped = {s for _, ss in GROUPS for s in ss}
assert set(SLUG.values()) <= grouped | {'index.html', 'privacy.html', 'terms.html'}, set(SLUG.values()) - grouped
seo_of = lambda s: (POST_META[s]['title'] + ' | ', POST_META[s]['description']) if s in POST_META else SEO.get(s, (s, ''))
llms = ['# 갈창림 한의원', '',
        '> 경상북도 경산시 하양읍 동서2길 43, 3층에 있는 한의원입니다. 평일(월~금) 08:30–18:30(점심 13:00–14:00), '
        '토·일요일 08:30–14:00(점심시간 없음) 진료하며 공휴일은 휴진합니다. 전화 053-851-0122.', '',
        '대표원장 갈창림(대구한의대학교 한의과대학 졸업)이 직접 진찰하고 치료합니다. 레이저제모·리프팅·색소·여드름·모공·스킨부스터 등 '
        '피부미용, 교통사고 후유증(자동차보험 진료), 척추·관절 통증, 소화불량·두통·불면·비염 같은 내과 질환, 다이어트, 소아 성장, 여성 질환을 진료합니다. '
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

# 404.html — GitHub Pages serves it for any unknown address, at that address, so every path is absolute
NOT_FOUND = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{GA_HEAD}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지를 찾을 수 없습니다 | 갈창림 한의원</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<style>
@font-face{{font-family:'Pretendard';src:url('/assets/PretendardVariable.woff2') format('woff2');font-weight:400 800;font-display:swap}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:flex;flex-direction:column;background:#faf7f0;color:#24302a;font-family:'Pretendard',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;line-height:1.6;word-break:keep-all;-webkit-text-size-adjust:100%}}
header{{border-bottom:1px solid #e2dccd}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 24px}}
header .wrap{{height:72px;display:flex;align-items:center}}
header img{{height:40px;width:auto;display:block}}
main{{flex:1;display:flex;align-items:center}}
.box{{max-width:560px;padding:72px 0}}
.code{{margin:0;font-size:14px;font-weight:700;letter-spacing:.06em;color:#7a6b42}}
h1{{margin:10px 0 12px;font-size:34px;line-height:1.3;letter-spacing:-.02em}}
p.lead{{margin:0;font-size:17px;color:#4d554f}}
.btns{{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px}}
.btns a{{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;border-radius:999px;border:1px solid #2f5241;color:#2f5241;background:#fff;font-weight:600;text-decoration:none}}
.btns a.primary{{background:#2f5241;color:#fff}}
.btns a:hover{{background:#f1ede3}}
.btns a.primary:hover{{background:#24402f}}
.btns a:focus-visible{{outline:2px solid #2f5241;outline-offset:2px}}
footer{{background:#24302a;color:#c9cfc6;font-size:14px}}
footer .wrap{{padding:28px 24px}}
footer a{{color:#fff;text-decoration:none;white-space:nowrap}}
@media (max-width:640px){{h1{{font-size:27px}}.box{{padding:56px 0}}.btns a{{flex:1 1 calc(50% - 5px);justify-content:center;padding:0 12px}}}}
</style>
</head>
<body>
<header><div class="wrap"><a href="/" aria-label="갈창림 한의원 홈"><img src="/assets/logo-horizontal.webp" alt="갈창림 한의원" width="190" height="40"></a></div></header>
<main><div class="wrap"><div class="box">
<p class="code">404</p>
<h1>페이지를 찾을 수 없어요</h1>
<p class="lead">주소가 바뀌었거나 잘못 입력되었을 수 있어요. 아래에서 원하시는 곳으로 이동해 주세요.</p>
<nav class="btns" aria-label="바로가기">
<a class="primary" href="/">홈으로</a>
<a href="/schedule.html">진료시간·오시는길</a>
<a href="/price.html">가격표</a>
<a href="tel:053-851-0122">전화 053-851-0122</a>
</nav>
</div></div></main>
<footer><div class="wrap">갈창림 한의원 · 경상북도 경산시 하양읍 동서2길 43, 3층 · <a href="tel:053-851-0122">053-851-0122</a></div></footer>
</body>
</html>
'''
open(f'{OUT}/404.html', 'w', encoding='utf-8').write(NOT_FOUND)

# Font: keep only the characters the site uses (2 MB → ~0.2 MB). Rebuilt every time, so new text is always covered.
# The `brotli` module can't be pip-installed here; pyshim/brotli.py hands WOFF2 compression to Node's zlib.
import sys, glob
sys.path.insert(0, f'{S}/pyshim')
from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont
chars = set()
for fp in glob.glob(f'{OUT}/*.html'):
    chars |= set(open(fp, encoding='utf-8').read())
chars |= {chr(c) for c in range(0x20, 0x7f)} | set('‘’“”·–—…→←↑↓※✓•°×₩～⋅「」『』《》〈〉')
chars = {c for c in chars if ord(c) >= 0x20}
from fontTools.varLib import instancer
fopts = ftsubset.Options(); fopts.flavor = 'woff2'; fopts.notdef_outline = True
fopts.layout_features = fopts.layout_features + ['tnum']  # tabular numbers are used in price tables
# The site only uses weights 400-800, so the weight axis is trimmed to that range (smaller file).
ffont = TTFont(f'{S}/fonts/PretendardVariable.woff2')
fsub = ftsubset.Subsetter(fopts); fsub.populate(text=''.join(chars)); fsub.subset(ffont)
ffont = instancer.instantiateVariableFont(ffont, {'wght': (400, 800)})
ffont.flavor = 'woff2'; ffont.save(f'{OUT}/assets/PretendardVariable.woff2')
print('font subset:', len(chars), 'chars,', os.path.getsize(f'{OUT}/assets/PretendardVariable.woff2') // 1024, 'KB')

total = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(OUT) for x in fs)
for r in report:
    print(f'{r[0]:24s} {r[1]:4d} KB' + ('  [map]' if r[2] else '') + (f'  faq={r[3]}' if r[3] else ''))
print(len(report), 'pages,', len(os.listdir(f'{OUT}/assets')), 'assets, total', total // 1024, 'KB')
