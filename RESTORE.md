# 갈창림한의원 홈페이지 빌드 도구 (백업)

이 브랜치는 홈페이지(main 브랜치)를 만드는 원본 파일입니다. 사이트에는 영향이 없습니다.

- `galch/project/` : 디자인 캔버스 원본(.dc.html 아트보드 + canvas.json)
  - 캔버스 아티팩트: https://claude.ai/code/artifact/2d7bfe82-57e3-4333-8ff9-3fab017ce7e7 (최신본은 캔버스에서 다시 읽을 것)
- `galch/img/` : 아트보드가 쓰는 이미지 원본 (measure.js 의 MAP: blob id → 파일)
- `fonts/` : Pretendard (OFL)
- `tools/build_site.py` : 아트보드 → 정적 사이트(/home/claude/site) 변환
  (SEO 제목·설명, 구조화 데이터, sitemap/robots/llms.txt, 네이버 지도, 팝업, GA4 G-J8PBY1YVS7)

## 새 환경에서 복구
1. 작업 폴더(S)에 `galch/`, `fonts/`, `tools/*.js`, `tools/build_site.py` 를 복사
2. `build_site.py` 의 `S = …` 와 `measure.js`/`sitecheck.js` 안의 경로를 새 작업 폴더로 바꾸기
3. `cp fonts/PretendardVariable.ttf /root/.fonts/` (공유 이미지 생성용)
4. `python3 build_site.py` → `/home/claude/site`
5. main 브랜치에 `/home/claude/site` 내용을 복사해 커밋·푸시 (작성자 gal0122 <gal0122@naver.com>). 사이트 주소: https://galclinic.co.kr (가비아 DNS → GitHub Pages, CNAME 파일)

## 글꼴 줄이기 (2026-10-07~)
- build_site.py 마지막에 fontTools로 Pretendard를 사이트에 쓰인 글자만 남겨 저장 (2MB → 약 0.2MB).
- 필요: `pip install fonttools` (이미 있으면 생략). brotli 모듈이 설치 안 되는 환경이면 `tools/pyshim/brotli.py`를 작업 폴더 `pyshim/`에 두면 Node의 zlib로 대신 압축함.

## 원장 칼럼 (2026-10-14~)
- 글 원본: `galch/columns/YYYY-MM-DD-<slug>.md` (머리말: title, slug, category, date, reviewed, description, summary, related).
  - category: 피부미용 / 교통사고 / 근골격계 통증 / 내과 질환 / 다이어트 / 소아·여성 (2026-10-15 세분화; 페이지 column-skin, -traffic, -pain, -internal, -diet, -kids-women). 여성 질환은 소아·여성, 아토피·원형 탈모는 피부미용. 글이 하나도 없는 분류는 메뉴·버튼·페이지가 자동으로 숨겨짐.
  - 본문 끝 `## 자주 묻는 질문` + `Q.` / `A.` 줄 → 접이식 FAQ와 FAQPage 구조화 데이터.
  - 의료 내용은 원장 확인 후 올리기. 최신·최고·유일·전문, 비교, 후기, 전후 사진 금지, 개인차 문구.
- `tools/columns.py`: 글 읽기·목록·분류 페이지·검색 색인. `tools/make_column_boards.py`: 캔버스 아트보드(Column, ColumnPost) 다시 만들기(글 추가 후 실행).
- 필요 패키지: `pip install markdown` (글 본문 변환).
- 빌드 결과: `column.html`(전체), `column-<분류>.html`(skin, traffic, pain, internal, diet, kids-women), `column-<slug>.html`(글), `column-search.json`(검색 색인; ?q=단어 로 검색 결과 열림).
- 글 추가 순서: md 작성 → `python3 make_column_boards.py` → `python3 build_site.py` → 캔버스 게시(Column/ColumnPost) → main 푸시.

## 페이지 날짜 (2026-10-15~)
- `galch/lastmod.json`: 페이지별 <main> 내용 해시와 마지막으로 바뀐 날짜. sitemap lastmod와 구조화 데이터 dateModified가 이 날짜를 씀.
- 내용이 바뀐 페이지만 빌드한 날짜로 갱신되고, 다시 빌드해도 그대로 유지됨 (매일 색인 요청 작업이 이 날짜로 '바뀐 페이지'를 고름). 복구할 때 이 파일도 같이 복사할 것.

## 예약 발행 (2026-10-15~)
- 칼럼 md의 `date`가 오늘(한국 시간)보다 뒤면 그 글은 빌드에 들어가지 않음. 날짜가 되는 날 다시 빌드·푸시하면 그때 올라감.
- `galch/drafts/`: 원장 확인 전 초안. 확인이 끝나면 `galch/columns/`로 옮기면 날짜에 맞춰 발행됨.
- 빌드는 어느 폴더에서나 가능: 작업 폴더 W를 만들고 `cp -r galch fonts W/`, `cp tools/*.py tools/*.js W/`, `mkdir W/pyshim && cp tools/pyshim/brotli.py W/pyshim/` 후 `GAL_OUT=/어딘가/site python3 W/build_site.py` (작업 폴더는 build_site.py가 있는 곳으로 자동 인식, 또는 GAL_S로 지정). 필요 패키지: pillow fonttools markdown (brotli 없으면 pyshim이 node 사용). 공유 이미지용 글꼴: `cp fonts/PretendardVariable.ttf /root/.fonts/`.
- 날짜 기록 `galch/lastmod.json`은 빌드할 때 갱신되므로, 빌드 뒤 이 브랜치에 다시 커밋할 것.
- GAL_TODAY=YYYY-MM-DD 로 특정 날짜 기준 미리보기 가능 (이때는 lastmod.json을 커밋하지 말 것).

## 질환 칼럼 (2026-10-15~)
- 머리말에 `keyword: 경산 OO` 와 `condition: OO` 를 넣으면: 검색 제목이 "경산 OO | 글 제목 – 갈창림한의원"이 되고, 구조화 데이터에 about(MedicalCondition)·keywords가 붙고, 글 끝에 "경산·하양에서 OO 진료를 찾으신다면" 안내 칸(주소·진료시간·전화, columns.py의 regions에서 한 곳만 고치면 됨)이 자동으로 붙음.
- 질환 칼럼 27편(원장 확인 완료, 턱관절·어지럼증 제외): 허리통증 10-15 발행, 나머지 26편은 10-16 ~ 11-10 하루 한 편씩 예약(피부미용 칼럼과 별도라 10-16 ~ 10-29는 하루 두 편). 원장 확인용 한 장짜리 HTML: `python3 tools/make_review.py` (작업 폴더의 prev/ 에 저장, 색소칼럼 검토본의 CSS를 씀).

## 내과 질환 페이지 (2026-10-15~)
- 아트보드 InternalDigestive(소화기 질환) · InternalNeuro(두통·신경 질환) · InternalSleep(불면·스트레스) · InternalRhinitis(비염·수족냉증) → internal-*.html. 메뉴 '내과 질환'(통증 다음), 홈 진료 분야 카드.
- 만들기: `python3 tools/make_internal_pages.py` (내용은 tools/internal_content.py, 머리·꼬리는 PainSpine 아트보드에서 가져옴). 그림: `python3 tools/internal_svgs.py` → galch/img/*.svg (캔버스 자산으로 올린 blob id는 measure.js MAP).
- 치료 방법은 원장님이 정해 준 것만: 소화기·불면·화병·만성피로·비염·안면마비 = 침·뜸·한약 / 두통 = 침·뜸·부항·약침·추나·한약 / 손발 저림 = 침·뜸·약침·한약 / 수족냉증 = 침·뜸·부항·한약.
- 질환 카드의 "원장 칼럼에서 자세히 보기" 링크(<a data-col="slug">)는 그 칼럼이 발행된 날부터 자동으로 보임 (build_site.py col_links).
- 961~1060px 화면에서는 메뉴 글자를 15px, 간격을 16px로 줄여 한 줄에 들어가게 함 (모든 아트보드 style).

## 홈 팝업 날짜 (2026-10-15~)
- Popup 아트보드의 각 팝업에 data-from / data-until (YYYY-MM-DD, 한국 시간)을 넣으면 그 기간에만 보임. 예: 11월 1일 휴진 팝업 data-from="2026-10-19" data-until="2026-11-01".
