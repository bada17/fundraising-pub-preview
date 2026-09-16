"""후원주점 페이지 굽기.

깃허브 페이지는 정적 파일만 올릴 수 있어서, 서버가 그려 주는 HTML 한 장을
받아 빌드 결과와 합친다. 이 저장소는 결과물만 담는다 — 원본은
fundraising-pub-page 저장소에 있고 거기서 고친다.

⚠️ 2026-09-16 부터 이 저장소가 **정식 공개본**이다 — event.action.or.kr 이
   여기를 가리킨다. 그래서 검토용 띠는 이제 기본이 아니라 `--preview` 로만 붙는다.

미리 해 둘 것 (원본 저장소 site/ 안에서):
    npm run build
    npx wrangler dev --config dist/server/wrangler.json --port 8987

그 다음:
    python bake.py                          정식 공개본
    python bake.py --preview                검토용 띠를 붙여서
    python bake.py http://localhost:8991/   포트를 바꿨으면

⚠️ 굽는 재료는 나란히 받은 fundraising-pub-page 의 빌드 결과다. 옛 PC 처럼 원본이
   원드라이브에 따로 있으면 PUB_DIST 로 가리킨다 — 안 그러면 뒤처진 사본을 굽는다.
    PUB_DIST="C:/Users/dbqke/OneDrive/문서/ChatGPT/후원주점 페이지/site/dist/client" python bake.py
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
# 여러 PC에서 같은 구조로 쓸 수 있게, 이 저장소와 나란히 받은 원본 저장소를 찾는다.
DIST = os.environ.get('PUB_DIST') or os.path.join(
    os.path.dirname(HERE), 'fundraising-pub-page', 'site', 'dist', 'client')
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
PREVIEW = '--preview' in sys.argv
SERVER = ARGS[0] if ARGS else 'http://localhost:8987/'
OUT = os.path.join(HERE, 'docs')

# 사용자 지정 도메인. docs/ 를 통째로 지웠다 다시 채우므로 매번 다시 써야 한다 —
# 빠뜨리면 굽는 순간 도메인이 풀려 사이트가 bada17.github.io 로 돌아간다.
DOMAIN = 'event.action.or.kr'

# 검토본임을 화면에 남긴다. 시민행동 이름이 붙은 채로 공개되는 자리라,
# 지금 글이 자리표시자라는 것을 보는 사람이 바로 알아야 한다.
BANNER = """
<style>
/* 띠를 화면 위에 붙이고, 그만큼 본문을 내린다. 머리글은 문서 맨 위를 기준으로
   자리를 잡아서 body 여백이 안 먹는다 — top 을 따로 밀어 준다. */
body { padding-top: 30px; }
.site-header { top: 30px !important; }
/* 후원 버튼도 오른쪽 위에 붙박이라 띠와 닿는다. 그만큼 내려 준다. */
.floating-support { top: calc(30px + 0.75rem) !important; }
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
    if not os.path.isdir(DIST):
        sys.exit('빌드 결과가 없다: %s' % DIST)

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(DIST, OUT)

    request = urllib.request.Request(SERVER, headers={'User-Agent': 'bake'})
    html = urllib.request.urlopen(request).read().decode('utf-8')

    # 프로젝트 페이지는 /저장소이름/ 아래에 놓여서, 절대 경로가 다 빗나간다.
    # 도메인을 붙인 뒤에도 상대경로는 그대로 맞으므로 이 변환은 그냥 둔다.
    html = html.replace('"/_next/', '"_next/')
    if PREVIEW:
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
    # 깃허브가 스스로 쓰는 CNAME 에는 줄바꿈이 없다. 맞춰 두어야 설정 화면을
    # 만진 뒤에 구워도 쓸데없는 차이가 안 생긴다.
    io.open(os.path.join(OUT, 'CNAME'), 'w', encoding='utf-8').write(DOMAIN)

    left = re.findall(r'"/_next/', html)
    print('구운 곳:', OUT)
    print('재료:', DIST)
    print('검토용 띠:', '붙임' if PREVIEW else '없음')
    print('도메인:', DOMAIN)
    print('남은 절대경로:', len(left))


if __name__ == '__main__':
    main()
