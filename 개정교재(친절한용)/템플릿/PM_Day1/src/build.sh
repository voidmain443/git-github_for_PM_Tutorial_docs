#!/bin/zsh
# 온담F&B PM 특강 Day1 워크북 템플릿 빌드 스크립트
# 사용: cd 교재/템플릿/PM_Day1/src && ./build.sh
# 요구: tectonic (XeTeX), poppler(pdfunite), 폰트 Apple SD Gothic Neo·Menlo (macOS 기본)
set -e
cd "$(dirname "$0")"
OUT=..
for f in 0[1-5]_*_빈템플릿.tex 0[1-5]_*_완성예시.tex; do
  echo "== $f"
  tectonic --chatter minimal "$f" 2>&1 | grep -iv "accessing absolute\|^warning:   you may\|choose a different" || true
  mv -f "${f%.tex}.pdf" "$OUT/"
done
cd "$OUT"
pdfunite 01_*_빈템플릿.pdf 02_*_빈템플릿.pdf 03_*_빈템플릿.pdf 04_*_빈템플릿.pdf 05_*_빈템플릿.pdf 00_Day1_템플릿팩_빈양식.pdf
pdfunite 01_*_완성예시.pdf 02_*_완성예시.pdf 03_*_완성예시.pdf 04_*_완성예시.pdf 05_*_완성예시.pdf 00_Day1_템플릿팩_완성예시.pdf
ls -la *.pdf
