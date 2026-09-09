# 후원주점 페이지 — 검토본

함께하는 시민행동 후원주점 페이지의 **검토용 시안**입니다. 실제 안내 페이지가 아니고,
글은 대부분 자리표시자입니다.

- 보기: https://bada17.github.io/fundraising-pub-preview/
- 원본: `fundraising-pub-page` 저장소 (여기서 고치지 않는다)

## 다시 굽기

원본 저장소 `site/` 안에서 빌드하고 서버를 띄운 뒤, 여기서 `bake.py` 를 돌린다.

```
npm run build
npx wrangler dev --config dist/server/wrangler.json --port 8987
```

```
python bake.py
git add docs && git commit -m "..." && git push
```

`docs/` 는 구운 결과라 손으로 고치지 않는다.
