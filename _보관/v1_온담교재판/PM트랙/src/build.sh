#!/bin/sh
# DayN 슬라이드 재빌드: body.tex(정본) → 슬라이드 PDF + 노트판 PDF → md 텍스트 미러
#   cd 교재/PM트랙 && sh src/build.sh        (Day1)
#   cd 교재/PM트랙 && sh src/build.sh 2      (Day2)
# 필요: python3, tectonic(XeTeX), Apple SD Gothic Neo / Menlo 폰트. 그림은 ../그림/PM_DayN/*.pdf
set -e
cd "$(dirname "$0")/.."
D=${1:-1}
tectonic --chatter minimal Day${D}_슬라이드.tex
tectonic --chatter minimal Day${D}_슬라이드_노트.tex
python3 src/beamer2md.py Day${D}_슬라이드_body.tex Day${D}_슬라이드.md
pdfinfo Day${D}_슬라이드.pdf | grep Pages
pdfinfo Day${D}_슬라이드_노트.pdf | grep Pages
