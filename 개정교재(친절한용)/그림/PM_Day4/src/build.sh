#!/bin/zsh
# 사용법: ./build.sh fig_1_4_ntcp   (확장자 제외) — .tex 또는 .py 자동 판별
set -e
cd "$(dirname "$0")"
OUT=..
for name in "$@"; do
  if [ -f "$name.tex" ]; then
    tectonic --chatter minimal "$name.tex" && mv "$name.pdf" "$OUT/$name.pdf"
    pdftoppm -png -r 200 -singlefile "$OUT/$name.pdf" "$OUT/$name"
    echo "OK tex $name"
  elif [ -f "$name.py" ]; then
    python3 "$name.py" && echo "OK py $name"
  else
    echo "no source for $name"; exit 1
  fi
done
