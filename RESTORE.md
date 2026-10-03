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
5. main 브랜치에 `/home/claude/site` 내용을 복사해 커밋·푸시 (작성자 gal0122 <gal0122@naver.com>)
