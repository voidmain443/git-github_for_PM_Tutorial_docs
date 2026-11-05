#!/bin/zsh
# 온담F&B PM 특강 Day2 워크북 템플릿 빌드 스크립트
# 사용: cd 교재/템플릿/PM_Day2/src && ./build.sh
# 요구: tectonic (XeTeX), poppler(pdfunite), 폰트 Apple SD Gothic Neo·Menlo (macOS 기본)
set -e
cd "$(dirname "$0")"
OUT=..
for f in 0[6-9]_*_빈템플릿.tex 10_*_빈템플릿.tex 0[6-9]_*_완성예시.tex 10_*_완성예시.tex; do
  echo "== $f"
  tectonic --chatter minimal "$f" 2>&1 | grep -iv "accessing absolute\|^warning:   you may\|choose a different" || true
  mv -f "${f%.tex}.pdf" "$OUT/"
done
cd "$OUT"
pdfunite 06_*_빈템플릿.pdf 07_*_빈템플릿.pdf 08_*_빈템플릿.pdf 09_*_빈템플릿.pdf 10_*_빈템플릿.pdf 00_Day2_템플릿팩_빈양식.pdf
pdfunite 06_*_완성예시.pdf 07_*_완성예시.pdf 08_*_완성예시.pdf 09_*_완성예시.pdf 10_*_완성예시.pdf 00_Day2_템플릿팩_완성예시.pdf
ls -la *.pdf
