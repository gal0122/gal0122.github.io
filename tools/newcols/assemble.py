import sys, os, re, glob, importlib, datetime, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refs_data import R
ALL = []
for m in ['b1_hair','b2_lifting','b3_booster','b4_acne','b5_traffic','b6_pain','b7_diet','b8_kids_women']:
    ALL += importlib.import_module(m).COLS
assert len(ALL) == 35, len(ALL)
slugs = [c['slug'] for c in ALL]; assert len(set(slugs)) == 35
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
existing = {re.sub(r'^\d{4}-\d\d-\d\d[a-z]?-', '', os.path.basename(f))[:-3] for f in glob.glob(f'{SP}/galch/columns/*.md')}
pages = {os.path.basename(f) for f in glob.glob('/home/claude/site/*.html')}
ok = pages | {f'column-{s}.html' for s in existing | set(slugs)}
for c in ALL:
    for part in c['related'].split(';'):
        h = part.split('|')[0].strip().split('#')[0]
        assert h in ok, (c['slug'], h)
    for k in c['refs']: assert k in R, (c['slug'], k)
    assert '## 자주 묻는 질문' in c['body'] and '개인차' in (c['summary'] + c['body']), c['slug']
COND = {
 'beard-laser-hair-removal':'수염 레이저제모','philtrum-hair-removal':'인중 제모','armpit-hair-removal':'겨드랑이 제모','leg-hair-removal-timing':'팔·다리 제모',
 'folliculitis-after-hair-removal':'레이저제모','ultrasound-vs-rf-lifting':'리프팅','lifting-interval':'리프팅','lifting-volume-loss':'리프팅',
 'thread-lifting-duration':'실리프팅','jawline-double-chin':'턱선 리프팅','skin-booster-types':'스킨부스터','pdrn-booster-sessions':'PDRN 스킨부스터',
 'plla-booster':'PLLA 스킨부스터','exosome-booster':'엑소좀 스킨부스터','adult-jaw-acne':'성인 여드름','acne-scar-types':'여드름 흉터',
 'enlarged-pores':'모공','laser-toning-sessions':'레이저토닝','acne-red-marks':'여드름 자국',
 'traffic-headache-dizziness':'교통사고 후유증','traffic-at-fault':'교통사고 치료','pedestrian-bicycle-accident':'교통사고 치료',
 'traffic-accident-pregnancy':'교통사고 치료','traffic-herbal-medicine':'교통사고 한약','traffic-insomnia-anxiety':'교통사고 후유증',
 'forward-head-posture':'거북목','spinal-stenosis':'척추관협착증','trigger-finger':'방아쇠수지','chuna-insurance':'추나',
 'diet-herbal-side-effects':'다이어트 한약','postpartum-diet':'산후 다이어트','diet-yoyo':'다이어트','growth-plate-closure':'소아 성장',
 'kids-rhinitis-growth':'소아 비염·성장','irregular-periods':'생리불순'}
assert set(COND) == set(slugs)
# schedule: stars first, then round-robin by category; 3 per day from 11/11
def rr(lst):
    by = {}
    for c in lst: by.setdefault(c['cat'], []).append(c)
    out = []
    for grp in itertools.zip_longest(*by.values()):
        out += [g for g in grp if g]
    return out
order = rr([c for c in ALL if c.get('star')]) + rr([c for c in ALL if not c.get('star')])
d0 = datetime.date(2026, 10, 22)   # 기존 하루 2편에 더해 하루 2편씩
os.makedirs(f'{SP}/galch/drafts', exist_ok=True)
for f in glob.glob(f'{SP}/galch/drafts/*.md'): os.remove(f)
for i, c in enumerate(order):
    d = (d0 + datetime.timedelta(days=i // 2)).isoformat()
    suf = 'cd'[i % 2]
    refs = ' ; '.join(f'{R[k][0]} | {R[k][1]}' for k in c['refs'])
    fm = f"""---
title: {c['title']}
slug: {c['slug']}
category: {c['cat']}
date: {d}
reviewed: {d}
keyword: {'경산 ' + c['keyword'] if not c['keyword'].startswith('경산') else c['keyword']}
condition: {COND[c['slug']]}
description: {c['desc']}
summary: {c['summary']}
related: {c['related']}
refs: {refs}
---

"""
    open(f'{SP}/galch/drafts/{d}{suf}-{c["slug"]}.md', 'w').write(fm + c['body'].strip() + '\n')
    print(d, suf, '★' if c.get('star') else ' ', c['cat'], c['slug'])
