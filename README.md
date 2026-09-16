# 후원주점 페이지 — 공개본

함께하는 시민행동 후원주점(27주년 창립행사) 안내 페이지의 **공개본**입니다.
이 저장소는 구운 결과만 담습니다 — 글과 화면은 `fundraising-pub-page` 에서 고칩니다.

- 주소: **https://event.action.or.kr** (2026-10-28 행사까지 씁니다)
- 원본: `fundraising-pub-page` 저장소 (여기서 고치지 않는다)

## 왜 여기서 내나

원본 저장소가 비공개라 깃허브 페이지가 안 나갑니다(무료 요금제는 공개만 됩니다).
그래서 검토본을 내던 이 공개 저장소를 그대로 공개본으로 씁니다 —
독상(`dok.action.or.kr`)·상담소(`pb.action.or.kr`)와 같은 길입니다.

- Pages 는 `master` 의 `docs/`, **브랜치 방식**입니다. 그래서 `docs/CNAME` 파일이
  사용자 지정 도메인을 정합니다(저장소 설정에 따로 저장되는 방식이 아닙니다).
- ⚠️ `bake.py` 는 `docs/` 를 통째로 지웠다 다시 채웁니다. 그래서 `CNAME` 을 **굽는
  쪽에서 매번 다시 씁니다.** 손으로 넣어 두면 다음 굽기에 사라져 도메인이 풀립니다.
- DNS 는 호스트코코아에 `event  CNAME  bada17.github.io`.
  ⚠️ `*.action.or.kr → action.or.kr` 와일드카드가 있어서 **레코드가 없어도 조회는
  됩니다.** "이미 붙었네" 로 오해하지 말고 값까지 볼 것.

## 다시 굽기

원본 저장소 `site/` 안에서 빌드하고 서버를 띄운 뒤, 여기서 `bake.py` 를 돌립니다.
두 저장소는 같은 상위 폴더에 나란히 둡니다 — `bake.py` 가 형제 폴더의
`fundraising-pub-page/site/dist/client` 를 찾습니다.

```
npm run build
npx wrangler dev --config dist/server/wrangler.json --port 8987
```

```
python bake.py
git add -A docs bake.py && git commit -m "..." && git push
```

- 원본이 형제 폴더에 없으면(옛 PC 의 원드라이브 폴더처럼) `PUB_DIST` 로 가리킵니다.
  안 그러면 **뒤처진 사본을 굽습니다.**
- 검토용 띠가 필요하면 `python bake.py --preview`. **기본은 띠 없는 공개본입니다.**
- `docs/` 는 구운 결과라 손으로 고치지 않습니다.
