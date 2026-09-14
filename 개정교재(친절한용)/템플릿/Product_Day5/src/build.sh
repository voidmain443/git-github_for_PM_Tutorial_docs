#!/bin/zsh
# 딥게이지 Product 특강 Day5 워크북 템플릿 빌드 — 사용: cd 교재/템플릿/Product_Day5/src && ./build.sh
# 완성 예시 드라이버(NN_*_완성예시.tex)는 워크북 §X.5 확정 후 추가하면 함께 빌드된다.
set -e
setopt null_glob
cd "$(dirname "$0")"
OUT=..
for f in [0-9][0-9]_*_빈템플릿.tex [0-9][0-9]_*_완성예시.tex; do
  [ -f "$f" ] || continue
  echo "== $f"
  tectonic --chatter minimal "$f" 2>&1 | grep -iv "accessing absolute\|^warning:   you may\|choose a different" || true
  mv -f "${f%.tex}.pdf" "$OUT/"
done
cd "$OUT"
pdfunite 21_*_빈템플릿.pdf 22_*_빈템플릿.pdf 23_*_빈템플릿.pdf 24_*_빈템플릿.pdf 25_*_빈템플릿.pdf 00_Day5_템플릿팩_빈양식.pdf
ls [1-9][0-9]_*_완성예시.pdf >/dev/null 2>&1 && pdfunite [1-9][0-9]_*_완성예시.pdf 00_Day5_템플릿팩_완성예시.pdf || true
ls -la *.pdf
