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
  - category: 피부미용 / 교통사고·통증 / 다이어트 / 소아·여성 / 건강 상식. 글이 하나도 없는 분류는 메뉴·버튼·페이지가 자동으로 숨겨짐.
  - 본문 끝 `## 자주 묻는 질문` + `Q.` / `A.` 줄 → 접이식 FAQ와 FAQPage 구조화 데이터.
  - 의료 내용은 원장 확인 후 올리기. 최신·최고·유일·전문, 비교, 후기, 전후 사진 금지, 개인차 문구.
- `tools/columns.py`: 글 읽기·목록·분류 페이지·검색 색인. `tools/make_column_boards.py`: 캔버스 아트보드(Column, ColumnPost) 다시 만들기(글 추가 후 실행).
- 필요 패키지: `pip install markdown` (글 본문 변환).
- 빌드 결과: `column.html`(전체), `column-<분류>.html`(skin, traffic, diet, kids-women, health), `column-<slug>.html`(글), `column-search.json`(검색 색인; ?q=단어 로 검색 결과 열림).
- 글 추가 순서: md 작성 → `python3 make_column_boards.py` → `python3 build_site.py` → 캔버스 게시(Column/ColumnPost) → main 푸시.

## 페이지 날짜 (2026-10-15~)
- `galch/lastmod.json`: 페이지별 <main> 내용 해시와 마지막으로 바뀐 날짜. sitemap lastmod와 구조화 데이터 dateModified가 이 날짜를 씀.
- 내용이 바뀐 페이지만 빌드한 날짜로 갱신되고, 다시 빌드해도 그대로 유지됨 (매일 색인 요청 작업이 이 날짜로 '바뀐 페이지'를 고름). 복구할 때 이 파일도 같이 복사할 것.
