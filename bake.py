"""후원주점 페이지 검토본 굽기.

깃허브 페이지는 정적 파일만 올릴 수 있어서, 서버가 그려 주는 HTML 한 장을
받아 빌드 결과와 합친다. 이 저장소는 결과물만 담는다 — 원본은
fundraising-pub-page 저장소에 있고 거기서 고친다.

미리 해 둘 것 (원본 저장소 site/ 안에서):
    npm run build
    npx wrangler dev --config dist/server/wrangler.json --port 8987

그 다음:
    python bake.py
"""

import io
import os
import re
import shutil
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = r'C:\Users\dbqke\fundraising-pub-page\site\dist\client'
SERVER = 'http://localhost:8987/'
OUT = os.path.join(HERE, 'docs')

# 검토본임을 화면에 남긴다. 시민행동 이름이 붙은 채로 공개되는 자리라,
# 지금 글이 자리표시자라는 것을 보는 사람이 바로 알아야 한다.
BANNER = """
<style>
/* 띠를 화면 위에 붙이고, 그만큼 본문을 내린다. 머리글은 문서 맨 위를 기준으로
   자리를 잡아서 body 여백이 안 먹는다 — top 을 따로 밀어 준다. */
body { padding-top: 30px; }
.site-header { top: 30px !important; }
.preview-tag {
  position: fixed;
  z-index: 200;
  top: 0;
  right: 0;
  left: 0;
  display: flex;
  height: 30px;
  align-items: center;
  justify-content: center;
  background: #111413;
  color: #f3f3ed;
  font: 550 0.75rem/1 'Noto Sans KR Variable', sans-serif;
  letter-spacing: -0.02em;
  pointer-events: none;
}
@media (max-width: 420px) { .preview-tag { font-size: 0.6875rem; } }
</style>
<div class="preview-tag">검토용 시안 · 내용은 채우는 중입니다</div>
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(DIST, OUT)

    request = urllib.request.Request(SERVER, headers={'User-Agent': 'bake'})
    html = urllib.request.urlopen(request).read().decode('utf-8')

    # 프로젝트 페이지는 /저장소이름/ 아래에 놓여서, 절대 경로가 다 빗나간다.
    html = html.replace('"/_next/', '"_next/')
    html = html.replace('</body>', BANNER + '</body>')
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)

    css_dir = os.path.join(OUT, '_next', 'static', 'css')
    for name in os.listdir(css_dir):
        if not name.endswith('.css'):
            continue
        path = os.path.join(css_dir, name)
        text = io.open(path, encoding='utf-8').read()
        text = text.replace('url(/_next/static/media/', 'url(../media/')
        io.open(path, 'w', encoding='utf-8').write(text)

    # 밑줄로 시작하는 _next 를 지킬이 통째로 무시한다. 이 파일이 그것을 끈다.
    io.open(os.path.join(OUT, '.nojekyll'), 'w', encoding='utf-8').write('')

    left = re.findall(r'"/_next/', html)
    print('구운 곳:', OUT)
    print('남은 절대경로:', len(left))


if __name__ == '__main__':
    main()
