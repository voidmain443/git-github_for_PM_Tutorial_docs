"""Authored explanatory figures: one scene shared by SVG and print.

Figures explain selected paragraphs, not a second course or an answer key.
No JavaScript, remote fonts, animation, or future-stage data is required.
"""
from copy import deepcopy
from html import escape
from pathlib import Path
import math
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
INK = '#26334d'
MUTED = '#53627a'
COLORS = {
    'evidence': ('#edf2fa', '#355d9e'),
    'work': ('#fffefb', '#64728a'),
    'decision': ('#fbf0df', '#916323'),
    'result': ('#eaf4ef', '#3f705e'),
}


def figures_for(unit):
    from figure_specs_early import FIGURES as early
    from figure_specs_late import FIGURES as late
    return deepcopy({**early, **late}[unit])


def all_figures():
    return {f['id']: f for u in range(10) for f in figures_for(u)}


def text_width(text, size):
    """Conservative width; actual Korean font metrics are checked in browser/PDF."""
    return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .59 for c in text) * size


def wrap(text, width, size):
    result = []
    line = ''
    for token in re.findall(r'\S+\s*', text):
        if line and text_width(line + token.rstrip(), size) > width:
            result.append(line.rstrip()); line = ''
        for c in token:
            if line and text_width(line + c, size) > width:
                result.append(line.rstrip()); line = ''
            line += c
    if line.strip(): result.append(line.rstrip())
    return result


def scene(spec):
    """Screen coordinates with rectangles, polylines, and single-line text."""
    width = 840
    nodes = {n['id']: n for n in spec['nodes']}
    assert set(nodes) == {n for row in spec['rows'] for n in row}
    if spec['kind']=='tree': return tree_scene(spec)
    boxes = {}; items = []; y = 56
    horizontal_rows = {i for i, row in enumerate(spec['rows']) if any(e['from'] in row and e['to'] in row for e in spec['edges'])}
    for row_index, row in enumerate(spec['rows']):
        if row_index in horizontal_rows: y += 44
        box_width = min(300, (width - 108 - 44 * (len(row) - 1)) / len(row))
        contents = {}
        for ident in row:
            node = nodes[ident]
            titles = wrap(node['title'], box_width - 32, 20)
            lines = [line for text in node['lines'] for line in wrap(text, box_width - 32, 17)]
            contents[ident] = (titles, lines)
        height = max(32 + len(t) * 27 + len(b) * 25 + 10 for t, b in contents.values())
        left = (width - len(row) * box_width - (len(row) - 1) * 44) / 2
        for col, ident in enumerate(row):
            x = left + col * (box_width + 44)
            boxes[ident] = dict(x=x, y=y, w=box_width, h=height, row=row_index)
            fill, stroke = COLORS[nodes[ident]['role']]
            items.append(dict(type='rect', x=x, y=y, w=box_width, h=height, fill=fill, stroke=stroke))
            titles, lines = contents[ident]; ty = y + 31
            for title in titles:
                items.append(dict(type='text', x=x+16, y=ty, text=title, size=20, color=INK, anchor='start', weight='bold')); ty += 27
            ty += 8
            for line in lines:
                items.append(dict(type='text', x=x+16, y=ty, text=line, size=17, color=MUTED, anchor='start')); ty += 25
        y += height + 92
    height = y - 48
    paths = []; labels = []
    for i, edge in enumerate(spec['edges']):
        a, b = boxes[edge['from']], boxes[edge['to']]
        ax, bx = a['x'] + a['w']/2, b['x'] + b['w']/2
        if a['row'] == b['row']:
            # Sequential boxes use separate side ports. Reusing their top ports
            # would join incoming/outgoing paths and visually bypass a review.
            forward=bx>ax
            points=[(a['x']+a['w'] if forward else a['x'],a['y']+a['h']/2),
                    (b['x'] if forward else b['x']+b['w'],b['y']+b['h']/2)]
            lx,ly=(points[0][0]+points[1][0])/2,a['y']-19
        elif b['row'] == a['row'] + 1:
            top, bottom = a['y']+a['h'], b['y']
            yy = (top+bottom)/2
            points = [(ax,top), (ax,yy), (bx,yy), (bx,bottom)]
            gap_edges=[e for e in spec['edges'] if boxes[e['from']]['row']==a['row'] and boxes[e['to']]['row']==b['row']]
            if len({e['from'] for e in gap_edges})>1 and len({e['to'] for e in gap_edges})>1:
                # Separate relationships must not accidentally become one shared bus.
                points=[(ax,top),(bx,bottom)]
            incoming = sum(e['to']==edge['to'] for e in spec['edges'])
            lx = ax if incoming>1 else bx
            ly = yy-11
        else:
            # Feedback/skip links run outside all nodes, not through a middle row.
            rail = 20 if bx <= ax else width-20
            start = (a['x'] if rail < ax else a['x']+a['w'], a['y']+a['h']/2)
            end = (b['x'] if rail < bx else b['x']+b['w'], b['y']+b['h']/2)
            points = [start,(rail,start[1]),(rail,end[1]),end]
            lx = 110 if rail < ax else width-110
            ly = (start[1]+end[1])/2
        paths.append(dict(type='path', points=points, color=MUTED))
        label_lines = wrap(edge.get('label',''), 194, 15)
        for j, text in enumerate(label_lines):
            labels.append(dict(type='label',x=lx,y=ly+j*20,text=text,size=15,color=MUTED,anchor='middle'))
    # A shared branch can carry one common label (e.g. EV feeds both comparisons).
    labels = list({(item['x'],item['y'],item['text']):item for item in labels}.values())
    return {'width':width,'height':height,'items':paths+items+labels,'boxes':boxes}


def tree_scene(spec):
    """All work packages are siblings on one bus, never sequential activities."""
    root=spec['nodes'][0]; children=spec['nodes'][1:]; items=[]; boxes={}; y=20
    for n in children:
        titles=wrap(n['title'],438,20)
        lines=[line for text in n['lines'] for line in wrap(text,438,17)]
        h=32+len(titles)*27+len(lines)*25+10
        boxes[n['id']]=dict(x=330,y=y,w=470,h=h,row=1)
        fill,stroke=COLORS[n['role']]
        items.append(dict(type='rect',x=330,y=y,w=470,h=h,fill=fill,stroke=stroke))
        ty=y+31
        for title in titles:
            items.append(dict(type='text',x=346,y=ty,text=title,size=20,color=INK,anchor='start',weight='bold'));ty+=27
        ty+=8
        for line in lines:
            items.append(dict(type='text',x=346,y=ty,text=line,size=17,color=MUTED,anchor='start'));ty+=25
        y+=h+20
    height=y
    titles=wrap(root['title'],208,20)
    lines=[line for text in root['lines'] for line in wrap(text,208,17)]
    h=42+len(titles)*27+len(lines)*25; yy=(height-h)/2
    boxes[root['id']]=dict(x=20,y=yy,w=240,h=h,row=0)
    fill,stroke=COLORS[root['role']]
    items.append(dict(type='rect',x=20,y=yy,w=240,h=h,fill=fill,stroke=stroke))
    ty=yy+31
    for title in titles:
        items.append(dict(type='text',x=36,y=ty,text=title,size=20,color=INK,anchor='start',weight='bold'));ty+=27
    ty+=8
    for line in lines:
        items.append(dict(type='text',x=36,y=ty,text=line,size=17,color=MUTED,anchor='start'));ty+=25
    paths=[]
    for n in children:
        b=boxes[n['id']]; cy=b['y']+b['h']/2
        paths.append(dict(type='path',points=[(260,height/2),(296,height/2),(296,cy),(330,cy)],color=MUTED))
    return dict(width=840,height=height,items=paths+items,boxes=boxes)


def svg_figure(spec):
    s = scene(spec)
    ident = spec['id']
    desc = ' '.join(n['title'] + '：' + '、'.join(n['lines']) + '。' for n in spec['nodes'])
    nodes = {n['id']:n['title'] for n in spec['nodes']}
    desc += ' '.join(nodes[e['from']]+' → '+nodes[e['to']]+'：'+e.get('label','')+'。' for e in spec['edges'])
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s["width"]} {s["height"]}" role="img" aria-labelledby="{ident}-title {ident}-desc" lang="ko">',
           f'<title id="{ident}-title">{escape(spec["title"])}</title><desc id="{ident}-desc">{escape(desc)}</desc>',
           f'<defs><marker id="{ident}-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="{MUTED}"/></marker></defs>']
    for item in s['items']:
        k = item['type']
        if k == 'rect':
            out.append(f'<rect x="{item["x"]}" y="{item["y"]}" width="{item["w"]}" height="{item["h"]}" rx="4" fill="{item["fill"]}" stroke="{item["stroke"]}" stroke-width="1.5"/>')
        elif k == 'path':
            points = ' '.join(f'{x},{y}' for x,y in item['points'])
            out.append(f'<polyline points="{points}" fill="none" stroke="{item["color"]}" stroke-width="1.7" marker-end="url(#{ident}-arrow)"/>')
        else:
            if k == 'label':
                w = text_width(item['text'],item['size'])+12
                out.append(f'<rect x="{item["x"]-w/2}" y="{item["y"]-16}" width="{w}" height="21" fill="#fffefb"/>')
            out.append(f'<text x="{item["x"]}" y="{item["y"]}" font-family="NanumGothic, Apple SD Gothic Neo, sans-serif" font-size="{item["size"]}" font-weight="{item.get("weight","normal")}" text-anchor="{item.get("anchor","start")}" fill="{item["color"]}">{escape(item["text"])}</text>')
    return ''.join(out)+'</svg>'


def figure_html(spec):
    esc = escape; nodes = {n['id']:n for n in spec['nodes']}
    mobile = []
    for row in spec['rows']:
        for ident in row:
            n = nodes[ident]
            connections = [f'<li>→ {esc(nodes[e["to"]]["title"])} <span>({esc(e["label"])})</span></li>' for e in spec['edges'] if e['from']==ident]
            mobile.append(f'<div class="figure-node figure-node-{n["role"]}"><strong>{esc(n["title"])}</strong><div>'+ '<br>'.join(esc(t) for t in n['lines'])+'</div>' + ('<ul class="figure-connections">'+''.join(connections)+'</ul>' if connections else '')+'</div>')
    return (f'<figure class="chapter-figure" data-figure="{spec["id"]}" aria-labelledby="figure-{spec["id"]}">'
            f'<h4 id="figure-{spec["id"]}">{esc(spec["title"])}</h4><p class="figure-lead">{esc(spec["lead"])}</p>'
            f'<div class="figure-desktop">{svg_figure(spec)}</div><div class="figure-mobile">'+''.join(mobile)+'</div>'
            f'<figcaption><p>{esc(spec["caption"])}</p><p class="figure-question"><strong>내 문서에서 확인하기</strong><br>{esc(spec["question"])}</p>'
            f'<p class="figure-source">근거: {esc(" · ".join(spec["sources"]))} · {esc(spec["stage"])} 자료를 설명한 교육용 도식</p></figcaption></figure>')


def insert_figures(body, specs, html=False):
    """Anchor after an authored paragraph, shared by chapter and manuscript."""
    from onboarding import markdown_html
    blocks = body.split('\n\n')
    for f in specs:
        # Specs may nominate an exact paragraph; otherwise immediately after the introduction.
        anchor = f.get('after', '')
        index = next((i for i,b in enumerate(blocks) if isinstance(b,str) and anchor and anchor in b), 0)
        if anchor and not any(isinstance(b,str) and anchor in b for b in blocks): raise ValueError(f'Missing figure anchor: {f["id"]}')
        blocks.insert(index+1, f)
    result = []
    for b in blocks:
        if isinstance(b,dict):
            if html: result.append(figure_html(b))
            else:
                result.append(f'#### 그림. {b["title"]}\n\n{b["lead"]}\n\n![{b["title"]}](../03_Level1_교재/그림/{b["id"]}.svg)\n\n{b["caption"]}\n\n내 문서에서 확인하기: {b["question"]}\n\n근거: '+ ' · '.join(b['sources']) + f' / {b["stage"]} / 교육용 도식')
        else: result.append(markdown_html(b) if html else b)
    return ('\n' if html else '\n\n').join(result)


def export_figures(base=ROOT, stage='S4'):
    dest = base/'03_Level1_교재/그림'; dest.mkdir(parents=True,exist_ok=True)
    visible = {i:f for i,f in all_figures().items() if f['stage'] <= stage}
    # This directory is wholly generated; remove obsolete or future pictures.
    for p in dest.glob('u*.svg'):
        if p.stem not in visible: p.unlink()
    for ident,f in visible.items():
        (dest/f'{ident}.svg').write_text(svg_figure(f),encoding='utf-8')


def pdf_drawing(spec, font='Korean', width=499):
    from reportlab.graphics.shapes import Drawing, Rect, PolyLine, Polygon, String
    from reportlab.lib.colors import HexColor
    s = scene(spec); scale = width/s['width']; h=s['height']
    drawing=Drawing(s['width'],h)
    for item in s['items']:
        k=item['type']
        if k=='rect':
            drawing.add(Rect(item['x'],h-item['y']-item['h'],item['w'],item['h'],rx=4,ry=4,fillColor=HexColor(item['fill']),strokeColor=HexColor(item['stroke']),strokeWidth=1.5))
        elif k=='path':
            points=[c for x,y in item['points'] for c in (x,h-y)]
            drawing.add(PolyLine(points,strokeColor=HexColor(item['color']),strokeWidth=1.7))
            (x0,y0),(x1,y1)=item['points'][-2:];angle=math.atan2(y1-y0,x1-x0)
            pts=[x1,h-y1]
            for sign in [-1,1]:
                pts += [x1-8*math.cos(angle)+sign*4*math.sin(angle),h-(y1-8*math.sin(angle)-sign*4*math.cos(angle))]
            drawing.add(Polygon(pts,fillColor=HexColor(item['color']),strokeColor=None))
        else:
            if k=='label':
                w=text_width(item['text'],item['size'])+12
                drawing.add(Rect(item['x']-w/2,h-item['y']-5,w,21,fillColor=HexColor('#fffefb'),strokeColor=None))
            drawing.add(String(item['x'],h-item['y'],item['text'],fontName=font,fontSize=item['size'],fillColor=HexColor(item['color']),textAnchor=item.get('anchor','start')))
    drawing.scale(scale,scale);drawing.width*=scale;drawing.height*=scale
    return drawing
