K = 'https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn='
N = 'https://nikom.or.kr/nckm/module/practiceGuide/viewPDF.do?guide_idx='
S = 'https://www.snuh.org/health/nMedInfo/nView.do?category=DIS&medid='
P = '국가건강정보포털'; G = '한의표준임상진료지침'; SN = '서울대학교병원 N의학정보'
R = {
 'disc': (f'{P}: 추간판탈출증(디스크)', K + '3348'), 'lbp': (f'{P}: 요통', K + '3796'),
 'turtle': (f'{P}: 일자목(거북목)증후군', K + '5972'), 'stenosis': (f'{P}: 척추관 협착증', K + '4047'),
 'g_lumbar': (f'{G}: 요추 추간판 탈출증', N + '151'), 'g_neck': (f'{G}: 경항통', N + '148'),
 'frozen': (f'{P}: 오십견(동결견)', K + '1567'), 'g_shoulder': (f'{G}: 견비통', N + '141'),
 'rotator': (f'{SN}: 회전근개증후군', 'https://www.snuh.org/health/nMedInfo/nView.do?medid=AA001389'),
 'knee': (f'{P}: 퇴행슬관절염', K + '5540'), 'knee_ex': (f'{P}: 무릎관절염, 올바로 운동하기', K + '5969'),
 'g_knee': (f'{G}: 퇴행성 슬관절염', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=153'),
 'sprain': (f'{P}: 염좌', K + '5441'), 'g_ankle': (f'{G}: 족관절염좌', 'https://nikom.or.kr/board/boardFile/download/32/1485/1869.do'),
 'carpal': (f'{P}: 수근굴(수근관) 증후군', K + '6292'), 'tendon': (f'{P}: 건막염', K + '2367'),
 'plantar': (f'{P}: 족저근막염', K + '5975'),
 'dysp': (f'{P}: 소화불량', K + '6887'), 'g_dysp': (f'{G}: 기능성소화불량', N + '154'),
 'gerd': (f'{P}: 위식도역류질환', K + '2057'), 'ibs': (f'{P}: 과민성장증후군', K + '5250'), 'g_ibs': (f'{G}: 과민대장증후군', N + '226'),
 'headache': (f'{P}: 두통', K + '5830'), 'migraine': (f'{P}: 편두통', K + '6557'), 'g_tth': (f'{G}: 긴장성 두통', N + '236'),
 'palsy': (f'{P}: 얼굴마비(말초성 마비)', K + '3790'), 'g_palsy': (f'{G}: 안면신경마비', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=150'),
 'rhin': (f'{P}: 만성비염', K + '5703'), 'g_rhin': (f'{G}: 알레르기 비염', N + '167'),
 'insom': (f'{P}: 불면증', K + '641'), 'g_insom': (f'{G}: 불면장애', 'https://nikom.or.kr/board/boardFile/download/38/23083/27379.do'),
 'g_hwa': (f'{G}: 화병', 'https://nikom.or.kr/board/boardFile/download/38/1153/32105.do'),
 'g_cold': (f'{G}: 수족냉증', N + '155'), 'sciatica': (f'{P}: 좌골신경통', K + '3512'),
 'cfs': (f'{P}: 만성피로증후군', K + '6549'), 'g_cfs': (f'{G}: 만성 피로', N + '157'),
 'short': (f'{P}: 저신장', K + '5415'), 'g_dysmen': (f'{G}: 월경통', 'https://nikom.or.kr/cms/practiceGuide/download/168/6061.do'),
 'endo': (f'{P}: 자궁내막증', K + '6283'), 'meno': (f'{P}: 폐경기', K + '6687'),
 'g_traffic': (f'{G}: 교통사고 상해 증후군', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=143&menu_idx=14'),
 'melasma': (f'{SN}: 기미', S + 'AA000203'), 'freckle': (f'{SN}: 주근깨', S + 'AA000522'),
 'nevus': (f'{P}: 모반(점)', K + '5692'), 'skintag': (f'{SN}: 연성 섬유종', S + 'AA000521'),
 'milia': (f'{SN}: 비립종', S + 'AA000519'), 'cyst': (f'{SN}: 피지낭종', 'https://www.snuh.org/health/nMedInfo/nView.do?medid=AA001204'),
 'wart': (f'{P}: 사마귀', K + '6537'), 'wart2': (f'{SN}: 사마귀', 'https://snuh.org/health/nMedInfo/nView.do?medid=AA000219'),
 'hemang': (f'{P}: 혈관종', K + '6317'), 'atopic': (f'{P}: 아토피피부염', K + '6582'),
 'g_atopic': ('한의임상진료지침: 아토피 피부염', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=121&menu_idx=14'),
 'aa': (f'{P}: 원형탈모', K + '6700'), 'acne': (f'{P}: 여드름', K + '3947'),
}
COLS = {
 'lumbar-disc': ['disc', 'g_lumbar'], 'low-back-pain': ['lbp'], 'neck-disc': ['disc', 'turtle', 'g_neck'],
 'neck-shoulder-stiffness': ['g_neck'], 'frozen-shoulder': ['frozen', 'g_shoulder'], 'shoulder-pain': ['rotator', 'g_shoulder'],
 'knee-pain': ['knee', 'knee_ex', 'g_knee'], 'ankle-sprain': ['sprain', 'g_ankle'], 'carpal-tunnel': ['carpal'],
 'elbow-pain': ['tendon'], 'plantar-fasciitis': ['plantar'],
 'indigestion': ['dysp', 'g_dysp'], 'reflux': ['gerd'], 'ibs': ['ibs', 'g_ibs'], 'headache': ['headache', 'migraine', 'g_tth'],
 'facial-palsy': ['palsy', 'g_palsy'], 'rhinitis': ['rhin', 'g_rhin'], 'insomnia': ['insom', 'g_insom'], 'hwabyung': ['g_hwa'],
 'cold-hands-feet': ['g_cold'], 'numbness': ['carpal', 'sciatica'], 'chronic-fatigue': ['cfs', 'g_cfs'],
 'kids-growth-when-to-start': ['short'], 'dysmenorrhea': ['g_dysmen', 'endo'], 'menopause': ['meno'], 'traffic-delayed-pain': ['g_traffic'],
 'melasma': ['melasma'], 'freckles': ['freckle'], 'moles': ['nevus'], 'skin-tags': ['skintag'], 'milia': ['milia'],
 'epidermoid-cyst': ['cyst'], 'flat-warts': ['wart', 'wart2'], 'cherry-angioma': ['hemang'], 'spider-angioma': ['hemang'],
 'atopic-dermatitis': ['atopic', 'g_atopic'], 'alopecia-areata': ['aa'],
}
PAGES = {
 'PainSpine': ['disc', 'lbp', 'stenosis', 'g_lumbar', 'g_neck'], 'PainJoint': ['frozen', 'knee', 'sprain', 'g_shoulder', 'g_knee'],
 'Traffic': ['g_traffic'], 'TrafficProcess': ['g_traffic'], 'TrafficTreat': ['g_traffic'],
 'InternalDigestive': ['dysp', 'gerd', 'ibs', 'g_dysp', 'g_ibs'], 'InternalNeuro': ['headache', 'palsy', 'g_tth', 'g_palsy'],
 'InternalSleep': ['insom', 'cfs', 'g_insom', 'g_hwa', 'g_cfs'], 'InternalRhinitis': ['rhin', 'g_rhin', 'g_cold'],
 'Women': ['g_dysmen', 'meno'], 'Growth': ['short'], 'Acne': ['acne'], 'Pigment': ['melasma', 'freckle'],
 'Mole': ['nevus', 'skintag', 'wart'],
}

# 2차 추가 (2026-10-20): 대한피부과학회·서울아산병원·서울대병원·진료지침
D = '대한피부과학회'; A = '서울아산병원'
R.update({
 'd_abnom': (f'{D}: ABNOM(후천 양측 오타모반모양반점)', 'https://www.derma.or.kr/new/general/disease.php?uid=3349&mod=document'),
 'd_sk': (f'{D}: 지루각화증', 'https://www.derma.or.kr/new/general/disease.php?uid=591&mod=document'),
 'a_benign': (f'{A}: 피부의 양성 종양', 'https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31759'),
 'sebhyp': (f'{SN}: 피지샘증식증', 'https://www.snuh.org/health/nMedInfo/nView.do?medid=AA001338'),
 'd_poro': (f'{D}: 땀구멍각화증(한공각화증)', 'https://www.derma.or.kr/new/general/disease.php?uid=5201&mod=document'),
 'a_lentigo': (f'{A}: 흑색점(lentigo) 용어 설명', 'https://www.amc.seoul.kr/asan/healthinfo/easymediterm/easyMediTermDetail.do?dictId=4988'),
 'a_epid': (f'{A}: 표피낭종', 'https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=32521'),
 'a_spider': (f'{A}: 거미혈관종 용어 설명', 'https://www.amc.seoul.kr/asan/healthinfo/easymediterm/easyMediTermDetail.do?dictId=163'),
 's_hair': (f'{SN}: 레이저 제모술', 'https://www.snuh.org/health/nMedInfo/nView.do?medid=BB000029'),
 'd_laser': (f'{D}: 피부과적 치료법 - 레이저', 'https://www.derma.or.kr/new/general/treatment.php?uid=3318&mod=document'),
 'g_postpartum': (f'{G}: 산후풍', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=319&menu_idx=14'),
 'obesity': (f'{P}: 비만', K + '6694'),
 'g_obesity': (f'{G}: 비만', 'https://nikom.or.kr/nckm/module/practiceGuide/view.do?guide_idx=325&menu_idx=14'),
 'd_acne': (f'{D}: 보통여드름', 'https://www.derma.or.kr/new/general/disease.php?uid=994&mod=document'),
 'a_acne': (f'{A}: 여드름', 'https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=31543'),
})
COLS.update({
 'abnom': ['d_abnom'], 'seborrheic-keratosis': ['d_sk', 'a_benign'], 'sebaceous-hyperplasia': ['sebhyp'],
 'porokeratosis': ['d_poro'], 'lentigo': ['a_lentigo'], 'epidermoid-cyst': ['a_epid', 'cyst'],
 'steatocystoma': ['a_benign'], 'spider-angioma': ['hemang', 'a_spider'],
 'laser-hair-removal-sessions': ['s_hair'], 'sylfirm-x-guide': ['d_laser'], 'postpartum': ['g_postpartum'],
})
PAGES.update({
 'HairRemoval': ['s_hair', 'd_laser'], 'Pigment': ['melasma', 'freckle', 'd_laser'],
 'AcneRed': ['acne', 'd_acne'], 'AcneScar': ['acne', 'a_acne'], 'Acne': ['acne', 'd_acne', 'a_acne'],
 'Diet': ['obesity', 'g_obesity'],
})
