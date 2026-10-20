# '시술 정보' 제목 옆에 가격표 바로가기 (가격표 페이지의 해당 표로 이동)
import re, os
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'galch', 'project')
LINKS = {
 'HairRemoval': ('price-hair', '부위별 가격 보기'),
 'DesignLifting': ('price-lifting', '리프팅 가격 보기'),
 'ThreadLifting': ('price-lifting', '실리프팅 가격 보기'),
 'BoosterAltcore': ('price-booster', '스킨부스터 가격 보기'),
 'BoosterECM': ('price-booster', '스킨부스터 가격 보기'),
 'BoosterKeratin': ('price-booster', '스킨부스터 가격 보기'),
 'BoosterPDRN': ('price-booster', '스킨부스터 가격 보기'),
 'BoosterPLLA': ('price-booster', '스킨부스터 가격 보기'),
 'Pigment': ('price-pigment', '색소·토닝 가격 보기'),
 'AcneRed': ('price-pigment', '토닝 가격 보기'),
 'Mole': ('price-pigment', '점 제거 가격 보기'),
 'Acne': ('price-acne', '여드름 치료 가격 보기'),
 'AcneScar': ('price-acne', '흉터 치료 가격 보기'),
 'Pore': ('price-acne', '모공 치료 가격 보기'),
}
H2 = '<h2 style="margin: 0; font-size: 28px">시술 정보</h2>'
for b, (anchor, label) in LINKS.items():
    p = f'{G}/{b}.dc.html'
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'<div data-price-link="true"[^>]*>\n(<h2[^>]*>시술 정보</h2>)\n<a [^>]*>[^<]*</a>\n</div>', r'\1', t)   # idempotent
    assert t.count(H2) == 1, b
    new = (f'<div data-price-link="true" style="display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 24px">\n'
           f'{H2}\n<a href="Price.dc.html#{anchor}" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 16px; font-weight: 700; color: #2f5241; text-decoration: none">{label} →</a>\n</div>')
    t = t.replace(H2, new)
    open(p, 'w', encoding='utf-8').write(t)
    print(b, anchor)
