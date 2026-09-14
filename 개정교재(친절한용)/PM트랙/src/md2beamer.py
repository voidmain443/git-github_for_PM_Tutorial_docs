#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day1_슬라이드.md  →  Day1_슬라이드_body.tex  (Beamer/metropolis 본문)

사용:  python3 md2beamer.py ../Day1_슬라이드.md ../Day1_슬라이드_body.tex
설정:  slide_config.py (슬라이드 제목별 글꼴 크기 · 그림 삽입 · 강제 페이지 나눔)
규칙:  md의 '---' → frame, '# ' → \\section, '## ' → frame 제목, 불릿 → itemize,
       표 → tabular(booktabs), '> **강사 노트**' → \\note, 코드블록 → 설정된 그림/TikZ로 치환.
       내용은 바꾸지 않는다(이스케이프·기호 치환만).
"""
import re, sys, os, importlib.util

# ---------------------------------------------------------------- inline
_CODE_RE = re.compile(r'`([^`]+)`')
_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')

_SYM = [
    ('→', r'$\rightarrow$'), ('←', r'$\leftarrow$'), ('−', r'$-$'),
    ('≈', r'$\approx$'), ('≠', r'$\neq$'), ('×', r'$\times$'), ('±', r'$\pm$'),
    ('÷', r'$\div$'), ('≥', r'$\geq$'), ('≤', r'$\leq$'),
    ('[ ]', r'$\square$~'),
]

def _esc(s):
    s = s.replace('\\', r'\textbackslash{}')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('$', r'\$'),
                 ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'),
                 ('^', r'\^{}')]:
        s = s.replace(a, b)
    return s

def inl(s):
    """마크다운 인라인 → LaTeX"""
    codes = []
    def _keep(m):
        codes.append(m.group(1)); return '\x00%d\x00' % (len(codes) - 1)
    s = _CODE_RE.sub(_keep, s)
    s = _esc(s)
    for a, b in _SYM:
        s = s.replace(a, b)
    s = _BOLD_RE.sub(lambda m: r'\textbf{' + m.group(1) + '}', s)
    def _restore(m):
        c = codes[int(m.group(1))]
        e = _esc(c)
        if all(ord(ch) < 128 for ch in c):
            return r'\texttt{' + e + '}'
        return r'\textsf{' + e + '}'
    s = re.sub('\x00(\\d+)\x00', _restore, s)
    return s

# ---------------------------------------------------------------- tables
def _cellw(c):
    w = 0.0
    for ch in c:
        w += 1.0 if ord(ch) > 0x2E80 else 0.55
    return w

def table_tex(rows, font=None, widths=None, split=None):
    rows = [r for r in rows if not re.match(r'^\|?\s*:?-{2,}', r.strip('| ').strip())]
    cells = []
    for r in rows:
        r = r.strip()
        if r.startswith('|'): r = r[1:]
        if r.endswith('|'): r = r[:-1]
        cells.append([c.strip() for c in r.split('|')])
    n = max(len(r) for r in cells)
    cells = [r + [''] * (n - len(r)) for r in cells]
    if font is None:
        tot_w = sum(_cellw(c) for r in cells for c in r)
        if tot_w < 200 and n <= 4:
            font = r'\small'
        elif tot_w < 520:
            font = r'\footnotesize'
        else:
            font = r'\scriptsize'
    units_per_line = {r'\small': 40.0, r'\footnotesize': 50.0, r'\scriptsize': 57.0, r'\tiny': 70.0}.get(font, 50.0)
    if widths is None:
        # 열 폭: 가장 긴 셀 기준 + 평균, 최소 폭은 가장 긴 라틴 단어(줄바꿈 불가)로 보장
        score, minw = [], []
        for j in range(n):
            col = [_cellw(r[j]) for r in cells]
            score.append(max(6.0, 0.6 * max(col) + 0.4 * (sum(col) / len(col))))
            longest = 0.0
            for r in cells:
                for tok in re.split(r'[\s/·→]+', re.sub(r'\*\*', '', r[j])):
                    if tok and all(ord(ch) < 0x2E80 for ch in tok):
                        longest = max(longest, _cellw(tok))
            minw.append(longest / units_per_line + 0.015)
        tot = sum(score)
        widths = [max(0.07, sc / tot) for sc in score]
        # 최소 폭 보장 후 나머지를 비례 배분
        fixed = [max(w, m) for w, m in zip(widths, minw)]
        excess = sum(fixed) - 1.0
        if excess > 0:
            flex = [f - m for f, m in zip(fixed, minw)]
            fs = sum(flex)
            fixed = [f - excess * (fl / fs) if fs > 0 else f for f, fl in zip(fixed, flex)]
        widths = fixed
        tot = sum(widths)
        widths = [w / tot for w in widths]
    avail = 0.985
    widths = [w * avail for w in widths]
    colspec = ''.join(r'>{\raggedright\arraybackslash}p{%.3f\textwidth}' % w for w in widths)
    header, body = cells[0], cells[1:]
    chunks = [body]
    if split:
        chunks = [body[i:i + split] for i in range(0, len(body), split)]
    out = []
    for k, chunk in enumerate(chunks):
        if k > 0:
            out.append(r'\framebreak')
        out.append(r'{\usebeamercolor[fg]{normal text}%s\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.12}' % font)
        out.append(r'\begin{tabular}{@{}%s@{}}' % colspec)
        out.append(r'\toprule')
        out.append(' & '.join(r'\textbf{' + inl(c) + '}' if c else '' for c in header) + r' \\')
        out.append(r'\midrule')
        for r in chunk:
            out.append(' & '.join(inl(c) for c in r) + r' \\')
        out.append(r'\bottomrule')
        out.append(r'\end{tabular}}')
        out.append(r'\par\smallskip')
    return '\n'.join(out)

# ---------------------------------------------------------------- figures
FIGDIR = '../그림/PM_Day1/'

def fig_tex(spec):
    files = spec['file'] if isinstance(spec['file'], list) else [spec['file']]
    h = spec.get('height', 0.72 if spec.get('mode') == 'top' else 0.5)
    w = spec.get('width', 1.0)
    parts = []
    for f in files:
        parts.append(r'\includegraphics[width=%.2f\textwidth,height=%.2f\textheight,keepaspectratio]{%s%s.pdf}'
                     % (w / len(files) - (0.02 if len(files) > 1 else 0), h, FIGDIR, f))
    body = '\n\\hfill\n'.join(parts)
    cap = spec.get('caption')
    out = [r'\begin{center}\usebeamercolor[fg]{normal text}', body]
    if cap:
        out.append(r'\par\nobreak\vspace{1pt}{\scriptsize\color{mDarkTeal!70}' + inl(cap) + r'\par}')
    out.append(r'\end{center}')
    return '\n'.join(out)

# ---------------------------------------------------------------- body parser
def body_tex(lines, cfg):
    out = []
    stack = []          # list of (indent, envname)
    table = []
    code = None
    codeidx = 0
    breaks = cfg.get('breaks', [])
    figs = cfg.get('figs', [])
    code_figs = [f for f in figs if f.get('mode') == 'code']
    beside = [f for f in figs if f.get('mode') == 'besidetable']
    tab_font = cfg.get('table_font')
    tab_split = cfg.get('table_split')
    tab_widths = cfg.get('table_widths')
    tables_seen = 0
    para_open = False

    def close_lists(to_indent=-1):
        while stack and stack[-1][0] > to_indent:
            out.append(r'\end{%s}' % stack.pop()[1])

    def flush_table():
        nonlocal table, tables_seen
        if table:
            close_lists()
            t = table_tex(table, font=tab_font, widths=tab_widths, split=tab_split)
            if tables_seen == 0 and beside:
                spec = beside[0]
                lw = spec.get('leftwidth', 0.42)
                out.append(r'\begin{columns}[T,onlytextwidth]')
                out.append(r'\begin{column}{%.2f\textwidth}' % lw)
                out.append(t.replace(r'\textwidth}', r'\linewidth}'))
                out.append(r'\end{column}\begin{column}{%.2f\textwidth}' % (0.98 - lw))
                out.append(r'\includegraphics[width=\linewidth,height=0.8\textheight,keepaspectratio]{%s%s.pdf}'
                           % (FIGDIR, spec['file']))
                out.append(r'\end{column}\end{columns}')
            else:
                out.append(t)
            tables_seen += 1
            table = []

    for raw in lines:
        line = raw.rstrip('\n')
        # 강제 나눔
        for b in breaks:
            if line.strip().startswith(b):
                flush_table(); close_lists()
                out.append(r'\framebreak')
        if code is not None:
            if line.strip().startswith('```'):
                # 코드블록 종료 → 그림 또는 커스텀 tex로 치환
                close_lists()
                if codeidx < len(code_figs):
                    spec = code_figs[codeidx]
                    if 'tex' in spec:
                        out.append(r'{\usebeamercolor[fg]{normal text}' + spec['tex'] + '}')
                    else:
                        out.append(fig_tex(spec))
                else:
                    out.append(r'\begin{itemize}\scriptsize')
                    for cl in code:
                        out.append(r'\item\relax ' + inl(cl))
                    out.append(r'\end{itemize}')
                codeidx += 1
                code = None
            else:
                code.append(line)
            continue
        if line.strip().startswith('```'):
            flush_table(); close_lists()
            code = []
            continue
        if line.strip().startswith('|'):
            close_lists()
            table.append(line)
            continue
        flush_table()
        if not line.strip():
            close_lists()
            continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', line)
        if m:
            indent = len(m.group(1))
            env = 'enumerate' if m.group(2)[0].isdigit() else 'itemize'
            close_lists(indent)
            if not stack or stack[-1][0] < indent:
                if stack:
                    out.append(r'\par\nobreak')   # 상위 항목과 첫 하위 항목을 떼지 않는다
                out.append(r'\begin{%s}' % env)
                stack.append((indent, env))
            elif stack[-1][1] != env:
                out.append(r'\end{%s}' % stack.pop()[1])
                out.append(r'\begin{%s}' % env)
                stack.append((indent, env))
            txt = m.group(3)
            if txt.startswith('[ ]'):
                out.append(r'\item[$\square$]\relax ' + inl(txt[3:].strip()))
            else:
                out.append(r'\item\relax ' + inl(txt))
            continue
        # 일반 문단(소제목)
        close_lists()
        out.append(r'\par\smallskip\noindent{\usebeamercolor[fg]{normal text}' + inl(line.strip()) + r'\par}\nobreak')
    flush_table(); close_lists()
    return '\n'.join(out)

# ---------------------------------------------------------------- slides
def parse_slides(md):
    chunks = re.split(r'^---\s*$', md, flags=re.M)
    slides = []
    for ci, ch in enumerate(chunks):
        if ci == 0:
            continue   # 문서 머리말(제목·사용 안내)은 슬라이드가 아니다
        lines = ch.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        if not lines:
            continue
        first = lines[0]
        if first.startswith('# ') and not first.startswith('## '):
            slides.append({'kind': 'section', 'title': first[2:].strip()})
            continue
        if not first.startswith('## '):
            # 문서 머리말(> 블록) 등은 건너뜀
            continue
        title = first[3:].strip()
        body, note = [], []
        in_note = False
        for l in lines[1:]:
            if l.startswith('>'):
                in_note = True
                t = l.lstrip('>').strip()
                t = re.sub(r'^\*\*강사 노트\*\*\s*:\s*', '', t)
                if t: note.append(t)
            elif in_note and not l.strip():
                continue
            else:
                body.append(l)
        slides.append({'kind': 'frame', 'title': title, 'body': body, 'note': ' '.join(note)})
    return slides

def frame_tex(sl, cfg):
    title = inl(sl['title'])
    size = cfg.get('size', r'\small')
    opts = 'allowframebreaks=1.0' if cfg.get('breakable', True) else ''
    if 't' in cfg.get('extra_opts', ''):
        opts += ',t'
    out = [r'\begin{frame}[%s]{%s}' % (opts, title), size]
    figs = cfg.get('figs', [])
    for f in figs:
        if f.get('mode') == 'top':
            out.append(fig_tex(f))
            if f.get('break_after', True):
                out.append(r'\framebreak')
    if cfg.get('pre'):
        out.append(cfg['pre'])
    out.append(body_tex(sl['body'], cfg))
    for f in figs:
        if f.get('mode') == 'end':
            out.append(r'\framebreak' if f.get('break_before', True) else '')
            out.append(fig_tex(f))
    if sl['note']:
        out.append(r'\note{' + inl(sl['note']) + '}')
    out.append(r'\end{frame}')
    return '\n'.join(out)

def main():
    src, dst = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('slide_config', os.path.join(here, 'slide_config.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    CONFIG = mod.CONFIG
    md = open(src, encoding='utf-8').read()
    slides = parse_slides(md)
    out = ['% 자동 생성: python3 src/md2beamer.py Day1_슬라이드.md Day1_슬라이드_body.tex  (직접 고치려면 src/slide_config.py 또는 이 파일)',
           '']
    nframes = nsections = 0
    unused = set(CONFIG.keys())
    for i, sl in enumerate(slides):
        if sl['kind'] == 'section':
            out.append('')
            out.append(r'\section{%s}' % inl(sl['title']))
            nsections += 1
            continue
        cfg = CONFIG.get(sl['title'], {})
        unused.discard(sl['title'])
        out.append('')
        out.append('%% ---- md slide %d: %s' % (nframes + 1, sl['title']))
        out.append(frame_tex(sl, cfg))
        nframes += 1
    open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    sys.stderr.write('frames=%d sections=%d\n' % (nframes, nsections))
    if unused:
        sys.stderr.write('WARNING unused config keys: %s\n' % unused)
    # 슬라이드 밀도 보고 (MD2BEAMER_VERBOSE=1 일 때만)
    if not os.environ.get('MD2BEAMER_VERBOSE'):
        return
    for i, sl in enumerate([s for s in slides if s['kind'] == 'frame']):
        n = sum(len(l) for l in sl['body'])
        sys.stderr.write('%3d %5d %s\n' % (i + 1, n, sl['title'][:50]))

if __name__ == '__main__':
    main()
