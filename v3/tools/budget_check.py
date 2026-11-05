"""v3 예산 검사 — 학생이 읽는 글이 '사람의 하루'에 들어가는지 잰다.

사용법
    python3 v3/tools/budget_check.py v3/Day1/교재.md v3/Day1/워크북.md

무엇을 재나
    분량(어절), 코드(문서 ID·§ 번호), 숫자, 부정·금지 표현, 문장 길이, 표지 종류.
    파일 이름에 '교재' '워크북' '슬라이드'가 있으면 그 종류의 분량 한도도 함께 본다.

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
NUMBER_LIMITS_BY_KIND = {    # 양식·완성 예시의 숫자는 '찾아보는 숫자'라서 워크북은 넓게 둔다
    "워크북": 100,
}
LENGTH_LIMITS = {            # 하루치 파일 하나의 분량(어절)
    "교재": 9000,
    "워크북": 5000,
}
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


def check(path: Path) -> bool:
    """파일 하나를 잰다. 교재와 워크북이 한 파일에 있으면 '# 워크북' 제목에서 나눠 잰다."""
    text = path.read_text(encoding="utf-8")
    kind = next((k for k in LENGTH_LIMITS if k in path.name), None)
    if kind is None and re.search(r"^# 워크북", text, flags=re.M):
        textbook, workbook = re.split(r"^(?=# 워크북)", text, maxsplit=1, flags=re.M)
        first = report(f"{path} — 교재 부분", textbook, "교재", path.name)
        second = report(f"{path} — 워크북 부분", workbook, "워크북", path.name)
        return first and second
    return report(str(path), text, kind, path.name)


def report(title: str, text: str, kind, filename: str) -> bool:
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
