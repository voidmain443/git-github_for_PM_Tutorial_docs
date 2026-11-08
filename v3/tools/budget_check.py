"""v3 예산 검사 — 학생이 읽는 글이 '사람의 하루'에 들어가는지 잰다.

사용법
    python3 v3/tools/budget_check.py v3/Day1/교재.md v3/Day1/워크북.md

무엇을 재나
    분량(어절), 코드(문서 ID·§ 번호), 숫자, 부정·금지 표현, 문장 길이, 표지 종류.
    파일 이름에 '교재' '워크북' '슬라이드' '사례카드' '자료카드'가 있으면 그 종류의 한도도 본다.
    v3 안의 학생 자료면 사례 카드와 그날까지의 자료 카드에 없는 숫자도 찾아 알려 준다
    (10 이하의 정수와 '▶ 더 읽기'의 문헌 연도는 뺀다).

한도를 바꾸려면 아래 LIMITS 표의 숫자만 고치면 된다. 다른 곳은 손대지 않아도 된다.
초과 항목이 하나라도 있으면 종료 코드 1을 돌려준다(빌드에서 경고로 쓸 수 있다).
"""

import re
import sys
from pathlib import Path

# ── 한도표 (v3 설계서 2장과 같은 숫자) ─────────────────────────────
LIMITS = {
    "codes_per_1k": 2,       # 1,000어절당 문서 ID·§ 번호
    "numbers_per_1k": 60,    # 1,000어절당 숫자 (본문: 읽으며 기억해야 하는 숫자)
    "negations_per_1k": 5,   # 1,000어절당 금지·방어 표현
    "avg_sentence": 15,      # 문장 평균 어절 수
}
NUMBER_LIMITS_BY_KIND = {    # 양식·완성 예시·자료의 숫자는 '찾아보는 숫자'라서 넓게 둔다
    "워크북": 100,
    "사례카드": 100,
    "자료카드": 100,
}
LENGTH_LIMITS = {            # 파일 하나의 분량(어절)
    "교재": 9000,            # 하루치
    "워크북": 5000,          # 하루치
    "사례카드": 700,         # 한 쪽
    "자료카드": 4000,        # 하루치 자료 묶음
}
CASE_DIR = Path(__file__).resolve().parents[1] / "사례"  # 사례 카드와 자료 카드가 사례 숫자의 정본
# 사례 사실은 아니지만 본문에 나오는 숫자(수업 시간 배분, 문서의 판 번호). 필요하면 여기에 더한다.
ALLOWED_EXTRA = "70분 25분 15분 1.0판"
SLIDE_LIMIT = 40             # 하루 슬라이드 장 수
ALLOWED_MARKS = "■◆★▶☐"     # v3에서 쓰는 표지(핵심·사례·실습·더 읽기·확인)
OLD_MARKS = ["○", "●", "⇒", "▷", "※", "[추가 설정]", "(심화)", "(과정 후)"]

# ── 세는 규칙 ──────────────────────────────────────────────────────
CODE_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z]{1,4}-?\d{1,6}[A-Z]?(?![A-Za-z0-9])|§\s?\d+(?:\.\d+)*")
NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
# 금지·방어형 문장 끝만 센다. "A가 아니라 B"(대조)나 "없다"(존재)는 세지 않는다.
NEGATION_RE = re.compile(
    r"(마세요|말아야|말고|금지|안 된다|안 됩니다|않습니다|않는다|않도록|아닙니다|아니다)"
)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?다요])\s+|\n+")


def plain_text(markdown: str) -> str:
    """표·링크·서식 기호를 걷어 내고 읽히는 글자만 남긴다."""
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)  # 저자 주석은 학생이 읽지 않는다
    text = re.sub(r"^\\.*$", " ", text, flags=re.M)      # 인쇄 설정 줄(\newpage 등)도 읽지 않는다
    text = re.sub(r"\A---\n.*?\n---\n", " ", text, flags=re.S)  # 파일 맨 위의 설정 블록
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#>*|`_\-]+", " ", text)
    return text


def measure(markdown: str) -> dict:
    text = plain_text(markdown)
    words = text.split()
    n = max(len(words), 1)
    sentences = [s for s in SENTENCE_SPLIT.split(text) if len(s.split()) >= 3]
    reader_part = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    return {
        "eojeol": len(words),
        "codes_per_1k": round(1000 * len(CODE_RE.findall(reader_part)) / n, 1),
        "numbers_per_1k": round(1000 * len(NUMBER_RE.findall(text)) / n, 1),
        "negations_per_1k": round(1000 * len(NEGATION_RE.findall(text)) / n, 1),
        "avg_sentence": round(sum(len(s.split()) for s in sentences) / max(len(sentences), 1), 1),
        "slides": len(re.findall(r"^## ", markdown, flags=re.M)),
        "old_marks": [m for m in OLD_MARKS if m in reader_part],
    }


# 사례 자료와 대조: 날짜·시각은 값 하나로, 금액은 원으로 바꿔, 다른 숫자는 같은 단위끼리 맞춰 본다.
WON = {"원": 1, "만원": 10**4, "백만원": 10**6, "억원": 10**8}
READING = re.compile(r"^#{2,3} ▶.*?(?=^#{1,3} |\Z)", flags=re.S | re.M)  # '▶ 더 읽기'의 문헌 연도는 묻지 않는다
DATE_FULL = re.compile(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일|(\d{4})-(\d{2})-(\d{2})")
DATE_SHORT = re.compile(r"(?<![\d년-])(\d{1,2})월\s*(\d{1,2})일")
TIME = re.compile(r"(?<!\d)(\d{1,2}):(\d{2})(?!\d)")
UNITS = "%|백만원|만원|억원|원|영업일|개월|시간|분|일|월|년|건|명|곳|개|거래|판|장|쪽"
AMOUNT = re.compile(r"(\d[\d,]*(?:\.\d+)?)(" + UNITS + ")?")


def facts(text: str, with_short_dates: bool = False) -> set:
    """글에 나오는 숫자 사실을 (값, 단위) 묶음으로 뽑는다. 날짜는 ('2027-01-22', '날짜')처럼."""
    found = set()

    def full_date(m):
        y, mo, d = (m.group(1), m.group(2), m.group(3)) if m.group(1) else (m.group(4), m.group(5), m.group(6))
        found.add((f"{int(y)}-{int(mo):02}-{int(d):02}", "날짜"))
        if with_short_dates:  # 카드 쪽: 해를 빼고 적은 날짜('10월 8일')와도 맞도록
            found.add((f"{int(mo):02}-{int(d):02}", "날짜"))
        return " "

    text = DATE_FULL.sub(full_date, text)
    text = DATE_SHORT.sub(lambda m: found.add((f"{int(m.group(1)):02}-{int(m.group(2)):02}", "날짜")) or " ", text)
    text = TIME.sub(lambda m: found.add((f"{int(m.group(1)):02}:{m.group(2)}", "시각")) or " ", text)
    for number, unit in AMOUNT.findall(text):
        number = number.replace(",", "")
        if unit in WON:  # 132백만원과 132,000,000원을 같은 돈으로 본다
            won = float(number) * WON[unit]
            found.add((str(int(won)) if won == int(won) else str(won), "원"))
            continue
        value = str(float(number)) if "." in number else str(int(number))
        found.add((value, unit or ""))
    return found


def case_numbers(day=None) -> set:
    """사례 카드와 (그날까지의) 자료 카드에 있는 숫자 사실. 카드 주석의 검산값도 포함한다."""
    files = [CASE_DIR / "사례카드.md"]
    for card in sorted(CASE_DIR.glob("자료카드_Day*.md")):
        if day is None or int(re.search(r"Day(\d+)", card.name).group(1)) <= day:
            files.append(card)
    text = "\n".join(f.read_text(encoding="utf-8") for f in files if f.exists())
    text = re.sub(r"\A---\n.*?\n---\n", " ", text, flags=re.S)  # 맨 위 설정 블록
    text = re.sub(r"^\\.*$", " ", text, flags=re.M)            # 인쇄 설정 줄
    return facts(text + "\n" + ALLOWED_EXTRA, with_short_dates=True)


def unregistered(text: str, registry: set) -> list:
    """사례 자료에 없는 숫자 사실. 10 이하의 정수(목록 번호 등)는 묻지 않는다.
    단위가 없는 숫자(표의 칸)는 값만 같으면, 단위가 있으면 단위까지 같아야 통과한다."""
    values = {v for v, _ in registry}
    missing = []
    for value, unit in sorted(facts(plain_text(READING.sub(" ", text)))):
        if unit in ("날짜", "시각"):
            ok = (value, unit) in registry
        else:
            if "." not in value and int(value) <= 10:
                continue
            ok = (value, unit) in registry if unit else value in values
        if not ok:
            missing.append(readable(value, unit))
    return missing


def readable(value: str, unit: str) -> str:
    """보고할 때 사람이 읽기 쉬운 모양으로: 14800000000원 → 148억원."""
    if unit in ("날짜", "시각"):
        return value
    if unit == "원":
        won = float(value)
        for name, size in (("억원", 10**8), ("백만원", 10**6), ("만원", 10**4)):
            if won >= size and won % (size // 100 or 1) == 0:
                return f"{won / size:g}{name}"
        return f"{won:,.0f}원"
    return value + unit


def check(path: Path) -> bool:
    """파일 하나를 잰다. 교재와 워크북이 한 파일에 있으면 '# 워크북' 제목에서 나눠 잰다."""
    text = path.read_text(encoding="utf-8")
    kind = next((k for k in LENGTH_LIMITS if k in path.name), None)
    inside_v3 = CASE_DIR.parent in path.resolve().parents
    is_case_material = kind in ("사례카드", "자료카드")  # 카드는 정본이라 대조하지 않는다
    day = re.search(r"Day(\d+)", str(path))
    registry = case_numbers(int(day.group(1)) if day else None) if inside_v3 and not is_case_material else None
    if kind is None and re.search(r"^# 워크북", text, flags=re.M):
        textbook, workbook = re.split(r"^(?=# 워크북)", text, maxsplit=1, flags=re.M)
        first = report(f"{path} — 교재 부분", textbook, "교재", path.name, registry)
        second = report(f"{path} — 워크북 부분", workbook, "워크북", path.name, registry)
        return first and second
    return report(str(path), text, kind, path.name, registry)


def report(title: str, text: str, kind, filename: str, registry=None) -> bool:
    m = measure(text)
    rows = []
    if kind:
        rows.append(("분량(어절)", m["eojeol"], LENGTH_LIMITS[kind]))
    else:
        rows.append(("분량(어절)", m["eojeol"], None))
    if "슬라이드" in filename:
        rows.append(("슬라이드 장 수", m["slides"], SLIDE_LIMIT))
    number_limit = NUMBER_LIMITS_BY_KIND.get(kind, LIMITS["numbers_per_1k"])
    rows += [
        ("코드 / 1,000어절", m["codes_per_1k"], LIMITS["codes_per_1k"]),
        ("숫자 / 1,000어절", m["numbers_per_1k"], number_limit),
        ("부정·금지 / 1,000어절", m["negations_per_1k"], LIMITS["negations_per_1k"]),
        ("문장 평균 어절", m["avg_sentence"], LIMITS["avg_sentence"]),
    ]
    ok = True
    print(f"\n{title}")
    for label, value, limit in rows:
        if limit is None:
            print(f"  {label:<22} {value:>8}")
            continue
        passed = value <= limit
        ok = ok and passed
        print(f"  {label:<22} {value:>8}  한도 {limit:<6} {'통과' if passed else '초과'}")
    if m["old_marks"]:
        ok = False
        print(f"  v3에서 쓰지 않는 표지    {' '.join(m['old_marks'])}  (허용: {' '.join(ALLOWED_MARKS)})")
    if registry:
        missing = unregistered(text, registry)
        if missing:
            ok = False
            print(f"  사례 자료에 없는 숫자 {len(missing)}개  {' '.join(missing[:20])}")
            print("    → 사례 사실이면 그날의 자료 카드에 먼저 있어야 합니다. 수업 시간 배분 같은 숫자면 이 파일의 ALLOWED_EXTRA에 넣습니다")
        else:
            print("  사례 자료 대조            통과")
    return ok


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    results = [check(Path(p)) for p in sys.argv[1:]]
    print("\n결과:", "모두 통과" if all(results) else "초과 항목이 있습니다 — 더하지 말고 빼서 맞춥니다")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
