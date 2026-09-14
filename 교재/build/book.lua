-- book.lua — pandoc Lua 필터 (md 원문은 건드리지 않고 PDF 출력만 손질)
--  1) 첫 H1 → 문서 제목/부제(" — " 기준 분리), 본문에서 제거
--  2) "목차" 절(수동 목차) 제거 — pandoc --toc 가 쪽번호 있는 목차를 대신 생성
--  3) 그림 뒤에 오는 이탤릭 설명 문단("*그림 1-1. …*")을 그림 캡션으로 합쳐 중복 제거
--  4) 그림 .png 참조를 같은 이름의 .pdf(벡터)가 있으면 그것으로 교체
--  5) 본문 폰트에 없는 글자 치환: 📄 → ▶, − (U+2212) → –
--  6) 표: 열이 많은 표(6열 이상)는 \small, 8열 이상은 \footnotesize 로 축소, 10열 이상은 가로 쪽(열 너비 재배분)
--  7) 코드 블록 안의 선 문자 관계도는 줄바꿈 없이 들어가는 글자 크기(필요하면 가로 쪽)로

local utils = pandoc.utils

-- 한글·한자·전각 등 폭 1em 글자인가
local function is_wide_cp(cp)
  return (cp >= 0x1100 and cp <= 0x11FF) or (cp >= 0x2E80 and cp <= 0x9FFF)
      or (cp >= 0xAC00 and cp <= 0xD7A3) or (cp >= 0xF900 and cp <= 0xFAFF)
      or (cp >= 0xFF00 and cp <= 0xFF60) or (cp >= 0x3000 and cp <= 0x303F)
      or (cp >= 0x2460 and cp <= 0x24FF) or (cp >= 0x3200 and cp <= 0x33FF)
end

local function file_exists(p)
  local f = io.open(p, "rb")
  if f then f:close() return true end
  return false
end

-- 5) 글자 치환
local function fix_chars(s)
  s = s:gsub("\u{1F4C4}", "▶")   -- 📄
  s = s:gsub("\u{1F4D6}", "▶")   -- 📖
  s = s:gsub("\u{2212}", "–")    -- −
  s = s:gsub("\u{2714}", "\u{2713}")  -- ✔ → ✓ (Apple SD Gothic Neo 에 U+2714 없음)
  s = s:gsub("\u{2717}", "×")          -- ✗ (없음) → ×
  return s
end
local function fix_code_chars(s)
  s = fix_chars(s)
  s = s:gsub("\u{203B}", "*")    -- ※ (Menlo 에 없음)
  return s
end
function Str(el)
  local s = fix_chars(el.text)
  if s ~= el.text then return pandoc.Str(s) end
end
function Code(el)
  local s = fix_code_chars(el.text)
  if s ~= el.text then el.text = s return el end
end
-- 7) 코드 블록 안의 글상자 그림(─│┌└▶◀ 등 선 문자를 쓴 관계도): 줄바꿈하면 그림이 깨지므로
--    줄바꿈 없이 들어가는 글자 크기를 고른다(세로 small→scriptsize → 가로 small→scriptsize → tiny).
local function is_diagram(txt)
  for _, cp in utf8.codes(txt) do
    if (cp >= 0x2500 and cp <= 0x257F) or cp == 0x25B6 or cp == 0x25C0 or cp == 0x25B2 or cp == 0x25BC then return true end
  end
  return false
end
local function code_max_em(txt)     -- 고정폭(Menlo): 영문·선 문자 0.6em, 한글(CJKmonofont 대체) 실측 ≈0.75em
  local best = 0
  for line in (txt .. "\n"):gmatch("([^\n]*)\n") do
    local w = 0
    for _, cp in utf8.codes(line) do
      if is_wide_cp(cp) then w = w + 0.75 else w = w + 0.6 end
    end
    if w > best then best = w end
  end
  return best
end
local DIAGRAM_FITS = {      -- {가로 여부, 글자 크기, 들어가는 폭(em)}: 세로 470pt·가로 717pt, 틀 여백 감안 0.97
  {false, "\\small",        470 / 9   * 0.97},
  {false, "\\footnotesize", 470 / 8   * 0.97},
  {false, "\\scriptsize",   470 / 7   * 0.97},
  {true,  "\\small",        717 / 9   * 0.97},
  {true,  "\\footnotesize", 717 / 8   * 0.97},
  {true,  "\\scriptsize",   717 / 7   * 0.97},
  {false, "\\tiny",         470 / 5   * 0.97},
  {true,  "\\tiny",         717 / 5   * 0.97},
}
function CodeBlock(el)
  local s = fix_code_chars(el.text)
  if is_diagram(s) then
    local w = code_max_em(s) * 1.02
    if w > DIAGRAM_FITS[1][3] and not s:find("\\end{Verbatim}", 1, true) then
      local pick = DIAGRAM_FITS[#DIAGRAM_FITS]
      for _, f in ipairs(DIAGRAM_FITS) do if w <= f[3] then pick = f break end end
      local opts = "fontsize=" .. pick[2] .. ",breaklines=false,frame=leftline,framerule=1.5pt,rulecolor=\\color{gray!60},framesep=8pt"
      local tex = "\\begin{Verbatim}[" .. opts .. "]\n" .. s .. "\n\\end{Verbatim}"
      if pick[1] then tex = "\\begin{landscape}\n" .. tex .. "\n\\end{landscape}" end
      return pandoc.RawBlock("latex", tex)
    end
  end
  if s ~= el.text then el.text = s return el end
end

-- 4) png → pdf
function Image(el)
  local src = el.src
  if src:match("%.png$") then
    local pdf = src:gsub("%.png$", ".pdf")
    if file_exists(pdf) then el.src = pdf return el end
  end
end

-- 3) 그림 + 이탤릭 설명 문단 병합
local function is_caption_para(blk)
  if blk.t ~= "Para" then return false end
  local c = blk.content
  if #c == 1 and c[1].t == "Emph" then
    local txt = utils.stringify(c[1])
    return txt:match("^그림%s*%d+[%-–]%d+") ~= nil
  end
  return false
end

local function merge_captions(blocks)
  local out = {}
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    local nxt = blocks[i+1]
    if b.t == "Figure" and nxt and is_caption_para(nxt) then
      local inl = nxt.content[1].content   -- Emph 내부 인라인
      b.caption = pandoc.Caption(pandoc.Plain(inl))
      table.insert(out, b)
      i = i + 2
    else
      table.insert(out, b)
      i = i + 1
    end
  end
  return out
end

-- 6) 표 열 너비/글자 크기 자동 조정
--    md 파이프 표는 구분선 길이가 모두 같아(|---|---|) pandoc 이 열을 균등 분할한다.
--    → 셀 내용의 폭(한글 1em, 영문 0.52em 추정)을 재서 열 너비를 비례 배분하고,
--      전체 폭이 본문 폭을 넘으면 \small / \footnotesize 로 줄인다.
-- 영문·숫자 폭: 기본은 한 글자 0.52em 일괄(세로표). 가로표는 글자 종류별(fine)로 잰다 —
-- Apple SD Gothic Neo 에서 숫자·대문자 ≈0.6em, 소문자 ≈0.5em, 공백·구두점 ≈0.3em.
local function narrow_em(cp, fine)
  if not fine then return 0.52 end
  if cp == 32 then return 0.28 end
  if (cp >= 48 and cp <= 57) or (cp >= 65 and cp <= 90) then return 0.6 end
  if cp >= 97 and cp <= 122 then return 0.5 end
  if cp < 48 or (cp >= 58 and cp <= 64) or (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126) then return 0.32 end
  return 0.5
end
local function text_em(str, fine)   -- 문자열 폭(em)
  local w = 0
  for _, cp in utf8.codes(str) do
    if is_wide_cp(cp) then w = w + 1.0 else w = w + narrow_em(cp, fine) end
  end
  return w
end
local function cell_em(cell, fine)  -- 셀의 가장 긴 줄 폭(em); 소프트브레이크 기준
  local txt = utils.stringify(cell)
  local best = 0
  for line in (txt .. "\n"):gmatch("([^\n]*)\n") do
    local w = text_em(line, fine)
    if w > best then best = w end
  end
  return best
end
local function rows_of(tbl)
  local rows = {}
  for _, r in ipairs(tbl.head.rows) do table.insert(rows, r) end
  for _, body in ipairs(tbl.bodies) do
    for _, r in ipairs(body.head) do table.insert(rows, r) end
    for _, r in ipairs(body.body) do table.insert(rows, r) end
  end
  for _, r in ipairs(tbl.foot.rows) do table.insert(rows, r) end
  return rows
end
function Table(el)
  local ncol = #el.colspecs
  if ncol == 0 then return nil end
  local rows = rows_of(el)
  local maxw, sumw, cnt = {}, {}, {}
  for c = 1, ncol do maxw[c] = 0; sumw[c] = 0; cnt[c] = 0 end
  for _, r in ipairs(rows) do
    for c, cell in ipairs(r.cells) do
      if c <= ncol then
        local w = cell_em(cell)
        if w > maxw[c] then maxw[c] = w end
        sumw[c] = sumw[c] + w; cnt[c] = cnt[c] + 1
      end
    end
  end
  -- 본문 폭: A4 22mm 여백 → 약 166mm ≈ 47em(10.5pt 기준). 열 여백(2*tabcolsep) 포함해 추정
  local TEXT_EM = 47
  local total = 0
  local weight = {}
  for c = 1, ncol do
    local avg = cnt[c] > 0 and sumw[c] / cnt[c] or 0
    -- 최댓값과 평균의 혼합: 한 셀만 긴 열이 전체를 잡아먹지 않게
    weight[c] = math.max(3.8, 0.6 * math.min(maxw[c], 30) + 0.4 * avg)
    total = total + maxw[c] + 1.2
  end
  local size = nil
  local has_rel = false
  for _, cs in ipairs(el.colspecs) do if cs[2] ~= "ColWidthDefault" then has_rel = true end end
  if total > TEXT_EM or has_rel then
    -- 비례 배분 (하한 6%)
    local wsum = 0
    for c = 1, ncol do wsum = wsum + weight[c] end
    local fr = {}
    local fsum = 0
    for c = 1, ncol do fr[c] = weight[c] / wsum; fsum = fsum + fr[c] end
    for c = 1, ncol do
      el.colspecs[c] = { el.colspecs[c][1], fr[c] / fsum * 0.98 }
    end
    if total > TEXT_EM * 1.9 or ncol >= 8 then size = "\\footnotesize"
    elseif total > TEXT_EM * 1.15 or ncol >= 6 then size = "\\small" end
  end
  -- 열이 10개 이상이면 가로(landscape) 쪽에 놓는다 (이해관계자 등록부·RACI·RTM·CPM·리스크 등록부 등)
  --   가로 쪽에서는 열 너비를 다시 잰다: ID·날짜·숫자 같은 짧은 열(≤12em)은 제 폭을 그대로 주어
  --   줄바꿈이 생기지 않게 하고, 남는 폭을 긴 문장 열에 비례 배분한다.
  if ncol >= 10 then
    local sz = (ncol >= 14) and "\\scriptsize" or "\\footnotesize"
    local fs = (ncol >= 14) and 7 or 8                 -- scriptsize 7pt / footnotesize 8pt
    -- 가로 본문 폭 253mm (A4 landscape, 여백 22mm). pandoc 이 (\linewidth - 2n·tabcolsep) 을 기준으로
    -- 열 비율을 적용하므로 열 여백만큼(3pt×2×n) 빼고 em 으로 환산한다.
    local avail = TEXT_EM * (253 / 166) * (10.5 / fs) - ncol * (6 / fs)
    -- 가로표용으로 폭을 글자 종류별로 다시 잰다.
    --   need = 가장 긴 줄(줄바꿈 없이 다 들어가는 폭), minw = 가장 긴 낱말(낱말 중간 줄바꿈이 안 생기는 폭),
    --   sumw = 열의 글자 총량(줄바꿈 줄 수를 결정).
    local need, minw = {}, {}
    for c = 1, ncol do maxw[c] = 0; sumw[c] = 0; minw[c] = 0 end
    for _, r in ipairs(rows) do
      for c, cell in ipairs(r.cells) do
        if c <= ncol then
          local w = cell_em(cell, true)
          if w > maxw[c] then maxw[c] = w end
          sumw[c] = sumw[c] + w
          for tok in utils.stringify(cell):gmatch("%S+") do
            local tw = text_em(tok, true)
            if tw > minw[c] then minw[c] = tw end
          end
        end
      end
    end
    local width, sumneed = {}, 0
    for c = 1, ncol do
      need[c] = maxw[c] * 1.10 + 0.5
      local avg = (cnt[c] > 0) and sumw[c] / cnt[c] or 0
      minw[c] = math.min(minw[c], 9)                       -- 한글 낱말은 9em 까지만 보호(그 뒤는 글자 단위 줄바꿈 허용)
      if avg <= 8 then minw[c] = math.max(minw[c], avg) end -- 짧은 열(평균 8em 이하)은 보통 행이 한 줄에 들어가게
      minw[c] = math.min(need[c], minw[c] * 1.10 + 0.5)
      width[c] = minw[c]
      sumneed = sumneed + need[c]
    end
    if sumneed <= avail then
      -- 전부 들어간다: 남는 폭은 긴 열(12em 초과)에, 없으면 모두에 비례 배분
      local extra, longsum = avail - sumneed, 0
      for c = 1, ncol do if maxw[c] > 12 then longsum = longsum + maxw[c] end end
      for c = 1, ncol do
        if longsum > 0 then
          width[c] = need[c] + ((maxw[c] > 12) and extra * maxw[c] / longsum or 0)
        else
          width[c] = need[c] + extra * need[c] / sumneed
        end
      end
    else
      -- 1) 모든 열에 최소폭(가장 긴 낱말)을 주고, 2) 남는 폭을 글자 총량(sumw) 비례로 나누되
      --    need(가장 긴 줄) 를 넘는 열은 거기서 멈추고 나머지에 다시 나눈다(몇 차례 반복).
      local rem = avail
      for c = 1, ncol do rem = rem - width[c] end
      if rem < 0 then
        -- 최소폭 합이 이미 폭을 넘음(드묾): 전부 비례 축소
        local f = avail / (avail - rem)
        for c = 1, ncol do width[c] = width[c] * f end
      else
        for _ = 1, 6 do
          if rem <= 0.01 then break end
          local open, osum = {}, 0
          for c = 1, ncol do if width[c] < need[c] - 0.01 then open[c] = true; osum = osum + sumw[c] end end
          if osum <= 0 then break end
          local give = rem
          rem = 0
          for c = 1, ncol do
            if open[c] then
              local add = give * sumw[c] / osum
              if width[c] + add > need[c] then rem = rem + (width[c] + add - need[c]); width[c] = need[c]
              else width[c] = width[c] + add end
            end
          end
        end
      end
    end
    local wsum = 0
    for c = 1, ncol do wsum = wsum + width[c] end
    for c = 1, ncol do el.colspecs[c] = { el.colspecs[c][1], width[c] / wsum * 0.99 } end
    return { pandoc.RawBlock("latex", "\\begin{landscape}" .. sz .. "\\setlength{\\tabcolsep}{3pt}"),
             el, pandoc.RawBlock("latex", "\\end{landscape}") }
  end
  if size then
    return { pandoc.RawBlock("latex", "{" .. size), el, pandoc.RawBlock("latex", "}") }
  end
  return el
end

-- 제목 " — " 분리: 부제는 표지에서 한 단계 작은 글자로(RawInline; pdftitle 메타에는 순수 문자열만 남음)
local function make_title(t, s)
  local inl = pandoc.Inlines({pandoc.Str(t)})
  if s then
    inl:insert(pandoc.RawInline("latex", "\\par\\vspace{14pt}{\\LARGE\\mdseries "))
    inl:insert(pandoc.Str(s))
    inl:insert(pandoc.RawInline("latex", "}"))
  end
  return pandoc.MetaInlines(inl)
end

-- 1), 2) 문서 수준 처리
function Pandoc(doc)
  if doc.meta.title and not doc.meta.subtitle then
    local full = utils.stringify(doc.meta.title)
    local t, s = full:match("^(.-)%s+—%s+(.+)$")
    if t then doc.meta.title = make_title(t, s) end
  end
  local blocks = doc.blocks
  local out = {}
  local title_done = false
  local skipping = false
  local skip_level = nil
  for _, b in ipairs(blocks) do
    if skipping then
      if b.t == "Header" and b.level <= skip_level then
        skipping = false
      else
        goto continue
      end
    end
    if not title_done and b.t == "Header" and b.level == 1 and not doc.meta.title then
      local full = utils.stringify(b)
      local t, s = full:match("^(.-)%s+—%s+(.+)$")
      if not doc.meta.title then
        doc.meta.title = make_title(t or full, s)
      end
      title_done = true
      goto continue
    end
    if b.t == "Header" and utils.stringify(b) == "목차" then
      skipping = true
      skip_level = b.level
      goto continue
    end
    table.insert(out, b)
    ::continue::
  end
  out = merge_captions(out)
  -- 1-b) 첫 장(level-1 Header) 이전의 머리말 블록은 목차 앞(include-before)으로 이동
  --     (--shift-heading-level-by 는 필터 뒤에 적용되므로, 장 수준 = 문서 안의 최소 헤더 레벨로 판정)
  local top = 99
  for _, b in ipairs(out) do
    if b.t == "Header" and b.level < top then top = b.level end
  end
  local preface, body = {}, {}
  local seen_chapter = false
  for _, b in ipairs(out) do
    if not seen_chapter and b.t == "Header" and b.level == top then seen_chapter = true end
    if seen_chapter then table.insert(body, b) else table.insert(preface, b) end
  end
  if seen_chapter and #preface > 0 then
    -- 머리말 끝의 구분선(---)은 제거
    while #preface > 0 and preface[#preface].t == "HorizontalRule" do table.remove(preface) end
    table.insert(preface, 1, pandoc.RawBlock("latex", "\\prefacestart"))
    table.insert(preface, pandoc.RawBlock("latex", "\\prefaceend"))
    doc.meta["include-before"] = pandoc.MetaBlocks(preface)
    doc.blocks = body
  else
    doc.blocks = out
  end
  return doc
end
