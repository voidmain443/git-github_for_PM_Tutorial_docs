#!/usr/bin/env python3
"""guide_check.py — '채우는 사람이 먼저 읽는 블록'(공통/03_서술규약.md) 린트.

사용법:  python3 build/readability/guide_check.py [Day1]
검사:
  (a) 글리프 — 폰트(Apple SD Gothic Neo)에 없는 글자: 이모지(📖·📄 제외), ☒ ✗ ☑ ▸ ⟶ ⚠ ✎, ㉑~㊿(PM 트랙)
  (b) '어디서 찾나 / 다시 볼 곳 / 펴게 할 곳' 열과 \\hint{} 안에 값(금액·%·날짜·인원·시간·건수)이 있는가
  (c) 개수 게이트 — 워크북 '#### 항목' 42 · ◆ 실습 입력 카드 5 · ★ 수업 중 과제 5 · 📖 48 (삭제 금지 확인)
  (d) 새 블록 밀도 — ○ ≤3문장·ID/§/숫자 없음, ● ≤4줄(≤340자), ▷ ≤3개, ⇒ 표 셀당 § ≤2
  (e) 금지 표현 — 'L123' 줄 번호 참조, '초보자'
  (f) 마크다운 표 — 모든 행의 열 수가 머리와 같은가
실패가 하나라도 있으면 exit 1.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DAY = sys.argv[1] if len(sys.argv) > 1 else 'Day1'
N = int(DAY[3:])
TRACK = 'PM트랙' if N <= 4 else 'Product트랙'
TP = 'PM' if N <= 4 else 'Product'

FILES_MD = [ROOT / TRACK / f'{DAY}_교재.md', ROOT / TRACK / f'{DAY}_워크북.md']
if N == 1:
    FILES_MD += [ROOT / '공통' / n for n in ('00_학습안내.md', '02_용어약어색인.md', '03_서술규약.md', '04_보조강사_응대표_Day1.md')]
FILES_TEX = sorted((ROOT / '템플릿' / f'{TP}_{DAY}' / 'src').glob('*_body.tex')) + [ROOT / TRACK / f'{DAY}_슬라이드_body.tex']

BAD_SYMBOLS = set('☒✗☑▸⟶⚠✎✔✘➜➔')
ALLOWED_EMOJI = {'\U0001F4D6', '\U0001F4C4'}   # 📖 📄 — book.lua 가 ▶ 로 치환
VALUE = re.compile(r'(\d{4}-\d{2}(-\d{2})?)|(\d[\d,.]*\s*(억|%|％|명|영업일|시간|건|개|주|점|대|만원|원|FP|h|TB))')
FIND_COLS = ('어디서 찾나', '다시 볼 곳', '펴게 할 곳', '값은 어디에 있나')
GATES = {'#### 항목': 42, '◆ 실습 입력 카드': 6, '★ 수업 중 과제': 11, '📖': 48}   # Day1 워크북 기준값(2026-09-14 개정 전 실측 — 본문 언급 포함)

fails, warns = [], []
def fail(f, ln, msg): fails.append(f'{f.name}:{ln}: {msg}')
def warn(f, ln, msg): warns.append(f'{f.name}:{ln}: {msg}')

def check_glyphs(f, text):
    for i, line in enumerate(text.splitlines(), 1):
        for ch in line:
            o = ord(ch)
            if ch in BAD_SYMBOLS:
                fail(f, i, f'폰트에 없는 기호 {ch!r} (U+{o:04X})')
            elif o >= 0x1F000 and ch not in ALLOWED_EMOJI:
                fail(f, i, f'이모지 {ch!r} (U+{o:04X}) — PDF에서 결자로 찍힌다')
            elif TP == 'PM' and (0x3251 <= o <= 0x325F or 0x32B1 <= o <= 0x32BF):
                fail(f, i, f'원문자 {ch!r} 는 PM 트랙 폰트에 없다')

def table_blocks(text):
    """md 표(인용문 안 포함)를 (시작 줄, [행 문자열]) 로 돌려준다."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].lstrip('> ').rstrip()
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\s*(>\s*)?\|?\s*:?-{2,}', lines[i + 1]):
            start = i; rows = []
            while i < len(lines) and lines[i].lstrip('> ').rstrip().startswith('|'):
                rows.append(lines[i].lstrip('> ').rstrip()); i += 1
            yield start + 1, rows
        else:
            i += 1

def split_row(row):
    cells = [c.strip() for c in row.strip().strip('|').split('|')]
    return cells

def check_tables(f, text):
    for start, rows in table_blocks(text):
        head = split_row(rows[0]); ncol = len(head)
        for k, r in enumerate(rows[2:], start + 2):
            if len(split_row(r)) != ncol:
                fail(f, k + 1, f'표 열 수 불일치 (머리 {ncol}, 이 행 {len(split_row(r))})')
        cols = [j for j, h in enumerate(head) if any(c in h for c in FIND_COLS)]
        for j in cols:
            for k, r in enumerate(rows[2:], start + 2):
                cells = split_row(r)
                if j < len(cells) and VALUE.search(cells[j]):
                    fail(f, k + 1, f'"{head[j]}" 열에 값이 있다: {cells[j][:60]!r} — §·표 ID·값의 이름만')
        # ⇒ 표 셀당 § ≤2
        if any('찾나' in h for h in head):
            for k, r in enumerate(rows[2:], start + 2):
                for c in split_row(r):
                    if c.count('§') > 2:
                        fail(f, k + 1, f'셀에 § {c.count("§")}개 (≤2): {c[:60]!r}')

def check_blocks(f, text):
    for i, line in enumerate(text.splitlines(), 1):
        s = line.lstrip('> ').strip()
        if s.startswith('**○ 한 줄 개념**'):
            body = s.split('—', 1)[-1]
            nsent = len(re.findall(r'[.!?]($|\s)', body))
            if nsent > 3: fail(f, i, f'○ 한 줄 개념 {nsent}문장 (≤3)')
            if re.search(r'§|\b[A-Z]{1,2}-\d{2}\b|\d', body): fail(f, i, '○ 한 줄 개념에 §·ID·숫자가 있다')
        elif s.startswith('**● 지금 여러분은**'):
            if len(s) > 340: fail(f, i, f'● 지금 여러분은 {len(s)}자 (≤340 ≈ 4줄)')
            if '§' not in s: fail(f, i, '● 지금 여러분은 에 출처 §가 없다')
        elif s.startswith('**▷ 틀리기 쉬운 것**'):
            n = len(s.split('—', 1)[-1].split(' · '))
            if n > 3: fail(f, i, f'▷ 틀리기 쉬운 것 {n}개 (≤3)')

def check_words(f, text, student_facing):
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r'(?<![A-Za-z])L\d{3,}\b', line):
            fail(f, i, "줄 번호 참조 'L123' — 절·항목·§로 가리킨다")
        if student_facing and '초보자' in line:
            fail(f, i, "'초보자' 표현 — 헌법 6조: 역할로 명명한다")

def check_hints(f, text):
    for i, line in enumerate(text.splitlines(), 1):
        m = re.search(r'\\hint\{(.*)\}\s*$', line)
        if m:
            body = m.group(1)
            if VALUE.search(body): fail(f, i, f'\\hint 에 값이 있다: {body[:60]!r}')
            if len(body) > 110: warn(f, i, f'\\hint 길이 {len(body)}자 (≤90 권장)')
            if body.count('§') > 2: fail(f, i, f'\\hint 에 § {body.count("§")}개 (≤2)')

def check_gates(f, text):
    for key, n in GATES.items():
        c = text.count(key)
        if c != n:
            fail(f, 0, f'개수 게이트: {key!r} {c}개 (기준 {n}) — 삭제 금지 항목이 사라졌거나 기준을 갱신해야 한다')

for f in FILES_MD:
    if not f.exists():
        warn(f, 0, '파일 없음'); continue
    t = f.read_text(encoding='utf-8')
    check_glyphs(f, t); check_tables(f, t); check_blocks(f, t)
    check_words(f, t, student_facing=(f.name not in ('03_서술규약.md', '04_보조강사_응대표_Day1.md')))
    if f.name == f'{DAY}_워크북.md' and N == 1:
        check_gates(f, t)
for f in FILES_TEX:
    if not f.exists():
        warn(f, 0, '파일 없음'); continue
    t = f.read_text(encoding='utf-8')
    check_glyphs(f, t); check_hints(f, t); check_words(f, t, student_facing=True)

for w in warns: print('warn ', w)
for x in fails: print('FAIL ', x)
print(f'guide_check {DAY}: {len(fails)} FAIL, {len(warns)} warn, 파일 {len(FILES_MD) + len(FILES_TEX)}')
sys.exit(1 if fails else 0)
