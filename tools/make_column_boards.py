"""Create (or refresh) the two 원장 칼럼 boards on the design canvas from the 가격표 board's header/footer.
Column.dc.html     – list page (sample list = current posts)
ColumnPost.dc.html – post template (sample = newest post)
Run again after editing posts to refresh the canvas samples. The site build does not depend on the samples."""
import re, sys, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/68b4eec7-1c3c-57e2-af39-86fe64cf79a4/scratchpad')
import columns

P = '/tmp/claude-0/-home-claude/68b4eec7-1c3c-57e2-af39-86fe64cf79a4/scratchpad/galch/project/'
C = '/tmp/claude-0/-home-claude/68b4eec7-1c3c-57e2-af39-86fe64cf79a4/scratchpad/galch/columns'
src = open(P + 'Price.dc.html', encoding='utf-8').read()

# header / footer from the price board, with "current page" moved to 원장 칼럼
head, rest = src.split('<main>', 1)
_, tail = rest.split('</main>', 1)
head = head.replace('<a href="Price.dc.html" aria-current="page" style="text-decoration: none; padding: 10px 0; color: #2f5241">가격표</a>',
                    '<a href="Price.dc.html" style="text-decoration: none; padding: 10px 0">가격표</a>')
head = head.replace('<a href="Column.dc.html" style="text-decoration: none; padding: 10px 0">원장 칼럼</a>',
                    '<a href="Column.dc.html" aria-current="page" style="text-decoration: none; padding: 10px 0; color: #2f5241">원장 칼럼</a>')
head = head.replace('<a href="Price.dc.html" aria-current="page" style="padding: 8px 0; text-decoration: none; color: #2f5241; font-weight: 700">전체 가격표</a>',
                    '<a href="Price.dc.html" style="padding: 8px 0; text-decoration: none">전체 가격표</a>')
head = head.replace('<a href="Column.dc.html" style="padding: 8px 0; text-decoration: none">전체 칼럼</a>',
                    '<a href="Column.dc.html" aria-current="page" style="padding: 8px 0; text-decoration: none; color: #2f5241; font-weight: 700">전체 칼럼</a>')
assert 'aria-current="page" style="text-decoration: none; padding: 10px 0; color: #2f5241">원장 칼럼' in head

COL_CSS = '''
.faq summary{list-style:none;cursor:pointer}
.faq summary::-webkit-details-marker{display:none}
.faq details[open] .faq-icon{transform:rotate(45deg)}
.col-wrap{max-width:880px;margin:0 auto;box-sizing:border-box}
.col-tag{display:inline-block;align-self:flex-start;padding:3px 10px;border-radius:999px;background:#e4ece6;color:#2f5241;font-size:13px;font-weight:700;line-height:1.6}
.col-tools{display:flex;flex-direction:column;gap:16px}
.col-chips{display:flex;gap:8px;overflow-x:auto;white-space:nowrap;padding-bottom:4px}
.col-chips a{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:0 16px;box-sizing:border-box;border:1px solid #d9d2c1;border-radius:999px;background:#ffffff;color:#4d554f;font-size:15px;font-weight:600;text-decoration:none}
.col-chips a:hover{border-color:#2f5241;color:#2f5241}
.col-chips a.on{background:#2f5241;border-color:#2f5241;color:#ffffff}
.col-n{font-size:13px;font-weight:500;opacity:.75}
.col-chips a:focus-visible,.col-search input:focus-visible,.col-btn:focus-visible{outline:2px solid #2f5241;outline-offset:2px}
.col-search{position:relative;display:block;max-width:520px;margin:0}
.col-search svg{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:#5d655f;pointer-events:none}
.col-search input{width:100%;box-sizing:border-box;min-height:48px;padding:0 16px 0 46px;border:1px solid #d9d2c1;border-radius:999px;background:#ffffff;color:#24302a;font:inherit;font-size:16px}
.col-list{border-top:1px solid #2f5241}
.col-item{border-bottom:1px solid #e2dccd}
.col-item a{display:flex;flex-direction:column;gap:8px;padding:26px 4px;color:inherit;text-decoration:none}
.col-item h2{margin:0;font-size:22px;line-height:1.45}
.col-item p{margin:0;max-width:820px;color:#4d554f;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.col-date{font-size:14px;color:#5d655f}
.col-item a:hover h2{color:#2f5241;text-decoration:underline}
.col-empty{margin:0;padding:40px 0;text-align:center;color:#5d655f}
.col-count{margin:0 0 14px;display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;color:#4d554f}
.col-count strong{color:#2f5241}
.col-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 22px;border:1px solid #2f5241;border-radius:999px;background:#ffffff;color:#2f5241;font:inherit;font-size:15px;font-weight:600;cursor:pointer}
.col-count .col-btn{min-height:36px;padding:0 14px;font-size:14px}
.col-more-wrap{display:flex;justify-content:center;padding-top:28px}
.col-more-wrap[hidden],.col-results[hidden],.col-list[hidden]{display:none}
.col-item p.col-snip{font-size:15px;-webkit-line-clamp:3}
mark{background:#fbe9a8;color:inherit;border-radius:2px;padding:0 1px}
.col-summary{margin:0;padding:22px 26px;border-left:4px solid #2f5241;border-radius:0 14px 14px 0;background:#ffffff;font-size:17px;line-height:1.8}
.col-summary strong{display:block;margin-bottom:6px;font-size:14px;color:#2f5241;letter-spacing:.02em}
.col-article{font-size:17px;line-height:1.85;color:#24302a;word-break:keep-all}
.col-article>:first-child{margin-top:0}
.col-article h2{margin:44px 0 14px;font-size:24px;line-height:1.45}
.col-article h3{margin:28px 0 10px;font-size:19px}
.col-article p{margin:0 0 16px}
.col-article ul,.col-article ol{margin:0 0 16px;padding-left:22px}
.col-article li{margin:6px 0}
.col-article a{color:#2f5241;font-weight:600}
.col-article table{width:100%;margin:8px 0 20px;border-collapse:collapse;font-size:15px;line-height:1.6}
.col-article th,.col-article td{padding:12px 10px;border-bottom:1px solid #e2dccd;text-align:left;vertical-align:top}
.col-article thead th{border-bottom:2px solid #2f5241;font-size:14px;color:#5d655f}
.col-related h2{margin:0 0 12px;font-size:20px}
.col-related ul{margin:0;padding:0;list-style:none;border-top:1px solid #e2dccd}
.col-related li{border-bottom:1px solid #e2dccd}
.col-related a{display:block;padding:16px 4px;color:#2f5241;font-weight:600;text-decoration:none}
.col-related a:hover{text-decoration:underline}
.col-next h2{margin:0 0 12px;font-size:20px}
.col-next ul{margin:0;padding:0;list-style:none;border-top:1px solid #e2dccd}
.col-next li{border-bottom:1px solid #e2dccd}
.col-next a{display:flex;flex-direction:column;gap:6px;padding:16px 4px;color:#24302a;text-decoration:none}
.col-next-t{font-weight:600;line-height:1.5}
.col-next a:hover .col-next-t{color:#2f5241;text-decoration:underline}
a.col-tag{text-decoration:none}
a.col-tag:hover{background:#d5e2d9}
@media (max-width:640px){
.col-wrap{padding-left:16px!important;padding-right:16px!important}
.col-item h2{font-size:19px}
.col-article{font-size:16px}
.col-article h2{font-size:21px;margin-top:36px}
.col-summary{padding:18px 18px;font-size:16px}
}
'''
head = head.replace('</style>\n</helmet>', COL_CSS.lstrip('\n') + '</style>\n</helmet>', 1)

CRUMB = '<p style="margin: 0; font-size: 14px; color: #5d655f">'
SEARCH_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>')
CTA = '''<section style="background: #f1ede3; border-top: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 72px 24px; display: flex; flex-direction: column; align-items: center; gap: 16px; text-align: center">
<h2 style="margin: 0; font-size: 28px">궁금한 점은 진료실에서 직접 물어보세요</h2>
<p style="margin: 0; color: #4d554f">경산 하양 갈창림한의원에서 지금 상태를 확인하고 알맞은 진료를 안내해 드립니다. 토·일요일에도 진료합니다.</p>
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 8px">
<a href="https://talk.naver.com/W4F2TI" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; min-height: 48px; padding: 0 24px; border: 1px solid #2f5241; background: #ffffff; text-decoration: none; font-weight: 500">네이버상담</a>
<a href="tel:053-851-0122" style="display: inline-flex; align-items: center; min-height: 48px; padding: 0 24px; background: #2f5241; color: #ffffff; text-decoration: none; font-weight: 500">전화 상담</a>
</div>
</div>
</section>
'''

def page(title, main, height):
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1)
    t = re.sub(r'"height":\d+', f'"height":{height}', tail, count=1)
    return h + '<main>\n' + main + '\n</main>' + t

posts = columns.load_posts(C)
_order = json.load(open(P + 'canvas.json', encoding='utf-8'))['order']
_rev = {('index.html' if b == 'Main.dc.html' else re.sub(r'(?<=[a-z])(?=[A-Z])', '-', b[:-8]).lower() + '.html'): b for b in _order}
dc = lambda slug: _rev[slug]

# ---- list board (the build also makes one page per category from it) ----
L = columns.mark(columns.list_regions(posts, 'all', lambda p: 'ColumnPost.dc.html', lambda k: 'Column.dc.html'))
list_main = f'''<section style="background: #f1ede3; border-bottom: 1px solid #e2dccd">
<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 44px; display: flex; flex-direction: column; gap: 12px">
{CRUMB}{L['lcrumb']}</p>
<h1 style="margin: 0; font-size: 40px; line-height: 1.3">{L['h1']}</h1>
<p style="margin: 0; max-width: 720px; font-size: 17px; color: #4d554f">{L['intro']}</p>
</div>
</section>

<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 40px 24px 96px; display: flex; flex-direction: column; gap: 28px">
<div class="col-tools">
<nav class="col-chips eq-track" aria-label="칼럼 분류">
{L['chips']}</nav>
<form class="col-search" role="search" action="Column.dc.html" method="get">{SEARCH_SVG}<input type="search" name="q" placeholder="궁금한 증상이나 시술을 검색해 보세요" aria-label="원장 칼럼 검색" autocomplete="off" enterkeyhint="search"></form>
</div>
<div data-column-list>
<div class="col-results" aria-live="polite" hidden></div>
<div class="col-list">
{L['list']}
</div>
<div class="col-more-wrap" hidden><button type="button" class="col-btn col-more">칼럼 더 보기</button></div>
</div>
</div>
</section>

{CTA}'''

# ---- post template board (sample = newest post) ----
v = columns.mark(columns.regions(posts[0], posts, dc, lambda p: 'ColumnPost.dc.html', lambda k: 'Column.dc.html'))
post_main = f'''<section style="background: #f1ede3; border-bottom: 1px solid #e2dccd">
<div class="col-wrap" style="padding: 56px 24px 40px; display: flex; flex-direction: column; gap: 14px">
{CRUMB}{v['crumb']}</p>
{v['cat']}
<h1 style="margin: 0; font-size: 36px; line-height: 1.35">{v['title']}</h1>
<p style="margin: 0; font-size: 15px; color: #5d655f">{v['meta']}</p>
</div>
</section>

<section>
<div class="col-wrap" style="padding: 44px 24px 72px; display: flex; flex-direction: column; gap: 44px">
<p class="col-summary"><strong>핵심 요약</strong>{v['summary']}</p>
<div class="col-article">
{v['body']}
</div>
{v['faq']}
{v['related']}
{v['next']}
<a href="Column.dc.html" style="align-self: flex-start; font-weight: 600; color: #2f5241; text-decoration: none">← 원장 칼럼 목록</a>
</div>
</section>

<section aria-label="작성 및 검토 정보">
<div class="reviewed" style="max-width: 1240px; margin: 0 auto; padding: 0 24px">
<p style="margin: 0; padding: 20px 0; border-top: 1px solid #e2dccd; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 12px; font-size: 14px; color: #5d655f"><span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 700; color: #2f5241"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"></path></svg>작성·검토</span><span><a href="Doctors.dc.html" style="color: #24302a; font-weight: 600; text-decoration: none">갈창림 대표원장</a> (한의사)</span><span>{v['reviewed']}</span></p>
</div>
</section>

{CTA}'''

open(P + 'Column.dc.html', 'w', encoding='utf-8').write(page('원장 칼럼', list_main, 1600))
open(P + 'ColumnPost.dc.html', 'w', encoding='utf-8').write(page('원장 칼럼 · 글', post_main, 4000))
print('boards written; posts:', [p['slug'] for p in posts])
