#!/usr/bin/env bash
# =====================================================================
#  교재 전체 재빌드 스크립트 — PM 트랙 Day1~4 · Product 트랙 Day5~8
#  사용법:  ./build.sh [단계] [날]
#     단계:  all(기본) | figs | templates | slides | books
#     날:    all(기본) | Day1 | Day2 | …   (여러 날: "Day1 Day2" 처럼 따옴표로 묶어 전달)
#     예)   ./build.sh                 # 전부(그림 → 템플릿 → 슬라이드 → 책), 모든 날
#           ./build.sh books Day2      # Day2 책(교재·워크북)만
#           ./build.sh figs Day1       # Day1 그림만
#  날 목록은 자동 탐지: 그림/{PM,Product}_DayN, 템플릿/{PM,Product}_DayN, {PM,Product}트랙/DayN_*.md 가 있으면 그 날이 빌드 대상이다.
#  Day3 이후는 같은 이름 규칙으로 파일을 추가하면 이 스크립트를 고치지 않아도 잡힌다.
#  공통 사례 연구(공통/가상회사_온담F앤B.md)는 날이 all 또는 Day1 일 때 함께 만든다.
#  필요 도구: tectonic, pandoc, poppler(pdftoppm·pdfunite·pdfinfo), python3+matplotlib
#            폰트: Apple SD Gothic Neo, Menlo (macOS 기본)
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"
STEP="${1:-all}"
DAYSEL="${2:-all}"

# tectonic 출력에서 무해한 경고를 걸러 보여준다
quiet() { grep -v "accessing absolute path\|^note: downloading\|^warning:   you may\|choose a different\|Language .Korean. not available\|(fontspec)\|already defined\|warnings were issued" || true; }

# ── 날 목록 결정 ──────────────────────────────────────────────────────
#   all → 그림/PM_Day*, 템플릿/PM_Day*, PM트랙/Day*_교재.md 에서 DayN 을 모아 정렬
discover_days() {
  {
    for d in "$ROOT"/그림/PM_Day* "$ROOT"/템플릿/PM_Day* "$ROOT"/그림/Product_Day* "$ROOT"/템플릿/Product_Day*; do
      [ -d "$d" ] && basename "$d" | sed 's/^PM_//; s/^Product_//'
    done
    for f in "$ROOT"/PM트랙/Day*_교재.md "$ROOT"/PM트랙/Day*_워크북.md "$ROOT"/PM트랙/Day*_슬라이드.tex "$ROOT"/Product트랙/Day*_교재.md "$ROOT"/Product트랙/Day*_워크북.md "$ROOT"/Product트랙/Day*_슬라이드.tex; do
      [ -f "$f" ] && basename "$f" | sed 's/_.*//'
    done
  } 2>/dev/null | grep -E '^Day[0-9]+$' | sort -t y -k2,2n | uniq
}
if [ "$DAYSEL" = "all" ]; then
  DAYS="$(discover_days | tr '\n' ' ')"
else
  DAYS="$DAYSEL"
fi
daynum() { echo "${1#Day}"; }   # Day2 → 2
# Day1~4 = PM 트랙 (PM트랙/, 그림·템플릿 PM_DayN) · Day5~8 = Product 트랙 (Product트랙/, Product_DayN)
track_prefix() { [ "$(daynum "$1")" -ge 5 ] && echo "Product" || echo "PM"; }
track_dir()    { [ "$(daynum "$1")" -ge 5 ] && echo "Product트랙" || echo "PM트랙"; }
track_name()   { [ "$(daynum "$1")" -ge 5 ] && echo "Product 트랙" || echo "PM 트랙"; }
track_course() { [ "$(daynum "$1")" -ge 5 ] && echo "프로덕트 매니지먼트 4일 특강" || echo "프로젝트 매니지먼트 4일 특강"; }

# ── 1) 그림 (TikZ .tex / matplotlib .py → PDF + PNG 200dpi) ─────────────
#   그림/PM_DayN/src/build.sh(이름 인수를 받는 개별 빌더)가 있으면 그것에 위임하고, 없으면 직접 돈다.
build_figs() {
  for day in $DAYS; do
    local tp; tp="$(track_prefix "$day")"
    local src="$ROOT/그림/${tp}_$day/src"
    echo "### [1/4] 그림: 그림/${tp}_$day/src"
    [ -d "$src" ] || { echo "  (건너뜀) $src 없음"; continue; }
    (
      cd "$src"
      local names=()
      for f in fig_*.tex fig_*.py; do [ -f "$f" ] && names+=("${f%.*}"); done
      [ ${#names[@]} -gt 0 ] || { echo "  (건너뜀) fig_*.tex/.py 없음"; exit 0; }
      if [ -f build.sh ]; then
        bash ./build.sh "${names[@]}" 2>&1 | quiet
      else
        for name in "${names[@]}"; do
          if [ -f "$name.tex" ]; then
            tectonic --chatter minimal "$name.tex" 2>&1 | quiet
            mv -f "$name.pdf" ../"$name.pdf"
            pdftoppm -png -r 200 -singlefile ../"$name.pdf" ../"$name"
            echo "  ok  $name (tex)"
          else
            python3 "$name.py"          # mplcommon.py 가 ../<name>.pdf/.png 로 저장
            echo "  ok  $name (py)"
          fi
        done
      fi
    )
  done
}

# ── 2) 워크북 템플릿 (빈 템플릿 5 + 완성 예시 5 + 통합본 2) ─────────────
#   템플릿/PM_DayN/src/build.sh 가 있으면 위임(개별 PDF + 00_DayN_템플릿팩_*.pdf 통합본까지 만든다).
#   없으면 NN_*_빈템플릿.tex / NN_*_완성예시.tex 를 번호순으로 직접 빌드하고 pdfunite 로 합친다.
build_templates() {
  for day in $DAYS; do
    local tp; tp="$(track_prefix "$day")"
    local src="$ROOT/템플릿/${tp}_$day/src"
    echo "### [2/4] 템플릿: 템플릿/${tp}_$day/src"
    [ -d "$src" ] || { echo "  (건너뜀) $src 없음"; continue; }
    (
      cd "$src"
      if [ -f build.sh ]; then
        bash ./build.sh 2>&1 | quiet | grep -v "^-rw\|^total " || true
        echo "  ok  템플릿/${tp}_$day/*.pdf (src/build.sh)"
      else
        local blanks=() fills=()
        for f in [0-9][0-9]_*_빈템플릿.tex; do [ -f "$f" ] && blanks+=("${f%.tex}"); done
        for f in [0-9][0-9]_*_완성예시.tex; do [ -f "$f" ] && fills+=("${f%.tex}"); done
        for name in "${blanks[@]}" "${fills[@]}"; do
          tectonic --chatter minimal "$name.tex" 2>&1 | quiet
          mv -f "$name.pdf" ../
          echo "  ok  $name"
        done
        cd ..
        [ ${#blanks[@]} -gt 0 ] && pdfunite "${blanks[@]/%/.pdf}" "00_${day}_템플릿팩_빈양식.pdf"
        [ ${#fills[@]}  -gt 0 ] && pdfunite "${fills[@]/%/.pdf}"  "00_${day}_템플릿팩_완성예시.pdf"
        echo "  ok  00_${day}_템플릿팩_빈양식.pdf / 00_${day}_템플릿팩_완성예시.pdf"
      fi
    )
  done
}

# ── 3) Beamer 슬라이드 (PM트랙/DayN_슬라이드.tex · _노트.tex) ──────────────
#   소스는 DayN_슬라이드_body.tex(손으로 쓴 정본) → tectonic 2회(슬라이드판·노트판)
#   → src/beamer2md.py 가 DayN_슬라이드.md(텍스트 미러)를 다시 만든다. md 를 고쳐도 슬라이드는 안 바뀐다.
build_slides() {
  for day in $DAYS; do
    local dir; dir="$ROOT/$(track_dir "$day")"
    echo "### [3/4] 슬라이드: $(track_dir "$day")/${day}_슬라이드*.tex"
    if [ -f "$dir/${day}_슬라이드.tex" ]; then
      (
        cd "$dir"
        for f in "${day}_슬라이드.tex" "${day}_슬라이드_노트.tex"; do
          [ -f "$f" ] || continue
          tectonic --chatter minimal "$f" 2>&1 | quiet
          echo "  ok  ${f%.tex}.pdf  ($(pdfinfo "${f%.tex}.pdf" | awk '/^Pages/{print $2}') 쪽)"
        done
        if [ -f src/beamer2md.py ] && [ -f "${day}_슬라이드_body.tex" ]; then
          python3 src/beamer2md.py "${day}_슬라이드_body.tex" "${day}_슬라이드.md"
          echo "  ok  ${day}_슬라이드.md (body.tex → md 텍스트 미러)"
        fi
      )
    else
      echo "  (건너뜀) $dir/${day}_슬라이드.tex 없음"
    fi
  done
}

# ── 4) md → PDF 책 (pandoc + tectonic) ──────────────────────────────────
#   공통 옵션. md 는 건드리지 않고 build/book.lua 필터와 build/header.tex 로 손질한다.
#   --number-sections 는 켜지 않는다: md 제목에 이미 "제1장", "1.2" 번호가 있다.
PANDOC_COMMON=(
  --pdf-engine=tectonic
  -V mainfont="Apple SD Gothic Neo" -V sansfont="Apple SD Gothic Neo" -V monofont="Menlo"
  -V CJKmainfont="Apple SD Gothic Neo" -V CJKmonofont="Apple SD Gothic Neo"   # 코드 안 한글도 출력
  -V geometry:a4paper -V geometry:margin=22mm -V fontsize=10.5pt -V linestretch=1.25
  -V colorlinks=true -V lang=ko-KR -V toc-title="목차" -V documentclass=report
  --toc --toc-depth=2
  --lua-filter="$ROOT/build/book.lua"
  -H "$ROOT/build/header.tex"
  -M date="$(date +%Y-%m-%d) 빌드"
)

# build_book <md 디렉터리> <md 파일명> <머리글 텍스트> <표지 상단 과정 표시> [추가 pandoc 옵션...]
#   머리글 파일 build/hdr_<md이름>.tex 는 여기서 매번 새로 쓴다(날마다 문구만 다르다).
build_book() {
  local dir="$1" md="$2" header="$3" tag="$4"; shift 4
  local pdf="${md%.md}.pdf"
  local hdr="$ROOT/build/hdr_${md%.md}.tex"
  [ -f "$ROOT/$dir/$md" ] || { echo "  (건너뜀) $dir/$md 없음"; return 0; }
  printf '%s\n' "\\renewcommand{\\bookheader}{$header}" "\\renewcommand{\\booktag}{$tag}" > "$hdr"
  (
    cd "$ROOT/$dir"      # 이미지·PDF 링크의 상대경로가 md 기준이므로 md 위치에서 실행
    local log="$ROOT/build/log_${md%.md}.txt"
    if pandoc "$md" -o "$pdf" "${PANDOC_COMMON[@]}" -H "$hdr" "$@" > "$log" 2>&1; then
      grep -v "accessing absolute\|^note: downloading\|Language 'Korean'\|^(fontspec)\|Object @page" "$log" || true
      echo "  ok  $dir/$pdf  ($(pdfinfo "$pdf" | awk '/^Pages/{print $2}') 쪽)"
    else
      cat "$log"
      echo "  FAIL  $dir/$md (전체 로그: $log)"
      exit 1
    fi
  )
}

# 날마다 다른 부제(표지 상단 과정 표시에 들어감). 새 날을 추가하면 여기에 한 줄 보탠다(없으면 "N일차"만 표시).
day_topic() {
  case "$1" in
    Day1) echo "착수" ;;
    Day2) echo "계획" ;;
    Day3) echo "실행·통제" ;;
    Day4) echo "종료·전환" ;;
    Day5) echo "프리시드" ;;
    Day6) echo "시드" ;;
    Day7) echo "PMF 추적" ;;
    Day8) echo "시리즈A·엔터프라이즈" ;;
    *)    echo "" ;;
  esac
}

build_books() {
  echo "### [4/4] 책: pandoc → PDF"
  for day in $DAYS; do
    local n; n="$(daynum "$day")"
    local topic; topic="$(day_topic "$day")"
    local hdr_sfx=""; [ -n "$topic" ] && hdr_sfx=" · $topic"
    local td tn tc; td="$(track_dir "$day")"; tn="$(track_name "$day")"; tc="$(track_course "$day")"
    local dn; dn="$n"; [ "$n" -ge 5 ] && dn="$((n-4))"   # 트랙 안에서의 일차(Product Day5 = 1일차)
    # 교재: '# 제N장' 이 장(chapter), '## N.N' 이 절
    build_book "$td" "${day}_교재.md" "$tn Day $n 교재$hdr_sfx" \
      "$tc · $tn ${dn}일차 · 교재"
    # 워크북: '## N.' 이 최상위 단위이므로 한 단계 올려(-1) 장으로 만든다
    build_book "$td" "${day}_워크북.md" "$tn Day $n 워크북$hdr_sfx" \
      "$tc · $tn ${dn}일차 · 워크북" \
      --shift-heading-level-by=-1
  done
  # 공통 사례 연구는 날과 무관 — all 또는 Day1 을 지정했을 때 함께 만든다
  if [ "$DAYSEL" = "all" ] || [ "$DAYSEL" = "Day1" ]; then
    build_book "공통" "가상회사_온담F앤B.md" "사례 연구 · 온담F\\&B홀딩스" "프로젝트 매니지먼트 4일 특강 · 공통 사례 연구" \
      --shift-heading-level-by=-1
    # 안내·색인은 짧아서 '##' 을 장으로 올리지 않는다(장마다 새 쪽이 되어 쪽수만 늘어난다)
    build_book "공통" "00_학습안내.md" "학습 안내" "프로젝트 매니지먼트 4일 특강 · 수강생 안내"
    build_book "공통" "02_용어약어색인.md" "용어·약어·문서 ID 색인" "프로젝트 매니지먼트 4일 특강 · 공용 색인"
    # 사례 한 장(책받침): 단독 LaTeX → A4 가로 2쪽
    ( cd "$ROOT/공통/src" && tectonic --chatter minimal 01_사례_한장.tex > "$ROOT/build/log_01_사례_한장.txt" 2>&1 \
        && mv -f 01_사례_한장.pdf ../01_사례_한장.pdf && echo "  ok  공통/01_사례_한장.pdf (2 쪽)" \
        || { cat "$ROOT/build/log_01_사례_한장.txt"; echo "  FAIL 공통/src/01_사례_한장.tex"; exit 1; } )
  fi
  # Product 트랙 공통 문서 — all 또는 Day5 를 지정했을 때 함께 만든다
  if [ "$DAYSEL" = "all" ] || [ "$DAYSEL" = "Day5" ]; then
    build_book "공통" "가상회사_딥게이지.md" "사례 연구 · 딥게이지" "프로덕트 매니지먼트 4일 특강 · 공통 사례 연구" \
      --shift-heading-level-by=-1
    build_book "공통" "10_Product_학습안내.md" "학습 안내 · Product 트랙" "프로덕트 매니지먼트 4일 특강 · 수강생 안내"
    build_book "공통" "12_용어약어색인_Product.md" "용어·약어·문서 ID 색인 · Product 편" "프로덕트 매니지먼트 4일 특강 · 공용 색인"
    build_book "공통" "13_Product_4일계획.md" "Product 트랙 4일 계획" "프로덕트 매니지먼트 4일 특강 · 제작 계획(강사·저자용)"
    build_book "공통" "14_Product_제작노트.md" "Product 트랙 제작 노트" "프로덕트 매니지먼트 4일 특강 · 주의할 점(강사·저자용)"
    ( cd "$ROOT/공통/src" && tectonic --chatter minimal 11_사례_한장_딥게이지.tex > "$ROOT/build/log_11_사례_한장_딥게이지.txt" 2>&1 \
        && mv -f 11_사례_한장_딥게이지.pdf ../11_사례_한장_딥게이지.pdf && echo "  ok  공통/11_사례_한장_딥게이지.pdf (2 쪽)" \
        || { cat "$ROOT/build/log_11_사례_한장_딥게이지.txt"; echo "  FAIL 공통/src/11_사례_한장_딥게이지.tex"; exit 1; } )
  fi
}

usage() { echo "사용법: ./build.sh [all|figs|templates|slides|books] [all|Day1|Day2|…]"; exit 1; }
for d in $DAYS; do echo "$d" | grep -qE '^Day[0-9]+$' || usage; done
[ -n "$DAYS" ] || { echo "빌드할 날이 없다 (그림/PM_DayN, 템플릿/PM_DayN, PM트랙/DayN_*.md 를 찾지 못함)"; exit 1; }
echo "### 대상: 단계=$STEP  날=$DAYS"

case "$STEP" in
  figs)      build_figs ;;
  templates) build_templates ;;
  slides)    build_slides ;;
  books)     build_books ;;
  all)       build_figs; build_templates; build_slides; build_books ;;
  *) usage ;;
esac
echo "### 완료"
