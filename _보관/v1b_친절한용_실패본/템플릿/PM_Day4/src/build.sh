#!/bin/zsh
# 온담F&B PM 특강 Day4 워크북 템플릿 빌드 스크립트
# 사용: cd 교재/템플릿/PM_Day4/src && ./build.sh            (전체)
#       ./build.sh 17                                        (산출물 ⑰만)
# 요구: tectonic (XeTeX), poppler(pdfunite), 폰트 Apple SD Gothic Neo·Menlo (macOS 기본)
set -e
cd "$(dirname "$0")"
OUT=..
if [[ -n "$1" ]]; then FILES=(${1}_*_빈템플릿.tex ${1}_*_완성예시.tex); else FILES=(1[6-9]_*_빈템플릿.tex 20_*_빈템플릿.tex 1[6-9]_*_완성예시.tex 20_*_완성예시.tex); fi
for f in $FILES; do
  echo "== $f"
  tectonic --chatter minimal "$f" 2>&1 | grep -iv "accessing absolute\|^warning:   you may\|choose a different" || true
  mv -f "${f%.tex}.pdf" "$OUT/"
done
cd "$OUT"
[[ -n "$1" ]] && { ls -la ${1}_*.pdf; exit 0; }
pdfunite 16_*_빈템플릿.pdf 17_*_빈템플릿.pdf 18_*_빈템플릿.pdf 19_*_빈템플릿.pdf 20_*_빈템플릿.pdf 00_Day4_템플릿팩_빈양식.pdf
pdfunite 16_*_완성예시.pdf 17_*_완성예시.pdf 18_*_완성예시.pdf 19_*_완성예시.pdf 20_*_완성예시.pdf 00_Day4_템플릿팩_완성예시.pdf
ls -la *.pdf
