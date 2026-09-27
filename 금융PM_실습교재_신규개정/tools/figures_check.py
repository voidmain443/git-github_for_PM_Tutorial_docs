"""Validate source-aware textbook figures and their seven release boundaries.

Run after the chapter build and stage_materials.prepare(). This checker reads
the generated artifacts; it does not repair, regenerate, or publish them.
Rendered font bounds and page appearance also require browser/PDF inspection.
"""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
import json
import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

from build import ROOT, DOCS, STAGES
from chapter_figures import figures_for, svg_figure, scene
from figure_specs_early import FIGURES as EARLY
from figure_specs_late import FIGURES as LATE


checks = []
rank = {stage: i for i, stage in enumerate(STAGES)}
source_stage = {source[0]: source[2] for source in DOCS}


def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    if not value:
        print('FAIL:', name)


class FigureHTML(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.figures = []
        self.classes = set()
        self.svg = 0
        self.text = []
        self.mobile_text = []
        self.mobile_depth = 0
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update(attrs.get('class', '').split())
        if attrs.get('data-figure'):
            self.figures.append(attrs['data-figure'])
        if tag == 'svg':
            self.svg += 1
        if tag == 'div':
            if 'figure-mobile' in attrs.get('class', '').split():
                self.mobile_depth = 1
            elif self.mobile_depth:
                self.mobile_depth += 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.mobile_depth:
            self.mobile_depth -= 1

    def handle_data(self, data):
        self.text.append(data)
        if self.mobile_depth:
            self.mobile_text.append(data)


def read_json(path):
    check('artifact exists: ' + str(path.relative_to(ROOT)), path.is_file())
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else None


def text_at(path):
    check('artifact exists: ' + str(path.relative_to(ROOT)), path.is_file())
    return path.read_text(encoding='utf-8') if path.is_file() else ''


def svg_checks(spec, markup, prefix):
    try:
        doc = ET.fromstring(markup)
    except ET.ParseError:
        check(prefix + ' SVG is parseable XML', False)
        return
    check(prefix + ' SVG root exists', doc.tag.split('}')[-1] == 'svg')
    box = [float(v) for v in doc.get('viewBox', '').split()]
    check(prefix + ' SVG has a positive viewBox', len(box) == 4 and box[2] > 0 and box[3] > 0)
    check(prefix + ' SVG has accessible title and description', any(el.tag.split('}')[-1] == 'title' and (el.text or '').strip() for el in doc.iter()) and any(el.tag.split('}')[-1] == 'desc' and (el.text or '').strip() for el in doc.iter()))
    check(prefix + ' SVG has no external image or script dependency', all(el.tag.split('}')[-1] not in {'script', 'image', 'foreignObject'} for el in doc.iter()))
    all_text = ''.join(doc.itertext())
    check(prefix + ' SVG retains node titles', all(node['title'] in all_text for node in spec['nodes']))
    check(prefix + ' SVG retains relationship labels', all(edge['label'] in all_text for edge in spec['edges']))


def geometry_checks(spec):
    ident = spec['id']
    layout = scene(spec)
    width, height = layout['width'], layout['height']
    boxes, items = layout['boxes'], layout['items']
    check(ident + ' scene has finite positive dimensions', all(math.isfinite(value) and value > 0 for value in [width, height]))
    check(ident + ' scene has every node box', set(boxes) == {node['id'] for node in spec['nodes']})

    def within(x, y, w=0, h=0):
        return all(math.isfinite(value) for value in [x, y, w, h]) and w >= 0 and h >= 0 and x >= 0 and y >= 0 and x + w <= width and y + h <= height

    check(ident + ' node boxes remain inside the canvas', all(within(box['x'], box['y'], box['w'], box['h']) for box in boxes.values()))
    pairs = [(a, b) for i, a in enumerate(boxes.values()) for b in list(boxes.values())[i + 1:]]
    check(ident + ' node boxes do not overlap', all(a['x'] + a['w'] <= b['x'] or b['x'] + b['w'] <= a['x'] or a['y'] + a['h'] <= b['y'] or b['y'] + b['h'] <= a['y'] for a, b in pairs))
    paths = [item for item in items if item['type'] == 'path']
    check(ident + ' every relationship has a routed path', len(paths) == len(spec['edges']))
    check(ident + ' routed edges remain inside the canvas', all(len(item['points']) >= 2 and all(within(x, y) for x, y in item['points']) for item in paths))
    def shares_segment(left, right):
        for a,b in zip(left,left[1:]):
            for c,d in zip(right,right[1:]):
                if a[0]==b[0]==c[0]==d[0] and min(max(a[1],b[1]),max(c[1],d[1]))>max(min(a[1],b[1]),min(c[1],d[1])):return True
                if a[1]==b[1]==c[1]==d[1] and min(max(a[0],b[0]),max(c[0],d[0]))>max(min(a[0],b[0]),min(c[0],d[0])):return True
        return False
    unrelated_pairs=[(a,b) for a in range(len(paths)) for b in range(a+1,len(paths)) if spec['edges'][a]['from']!=spec['edges'][b]['from'] and spec['edges'][a]['to']!=spec['edges'][b]['to']]
    check(ident+' independent relationships never become an unintended shared bus',all(not shares_segment(paths[a]['points'],paths[b]['points']) for a,b in unrelated_pairs))
    texts = [item for item in items if item['type'] in {'text', 'label'}]
    check(ident + ' rendered labels have positive font size', all(item['text'].strip() and math.isfinite(item['size']) and item['size'] > 0 for item in texts))
    # This is a conservative layout envelope, not a claim about actual glyph
    # metrics. Browser getBBox and rendered PDFs cover the latter separately.
    envelopes = []
    for item in texts:
        span = sum(item['size'] * (1 if unicodedata.east_asian_width(char) in 'WF' else .59) for char in item['text'])
        left = item['x'] - (span / 2 if item.get('anchor') == 'middle' else span if item.get('anchor') == 'end' else 0)
        top, bottom = item['y'] - item['size'], item['y'] + item['size'] * .25
        if item['type'] == 'label':
            left -= 6
            span += 12
            top, bottom = min(top, item['y'] - 16), max(bottom, item['y'] + 5)
        envelopes.append((item, left, top, span, bottom - top))
    check(ident + ' text envelopes are not clipped by canvas bounds', all(within(x, y, w, h) for _, x, y, w, h in envelopes))
    check(ident + ' node text envelopes fit their boxes', all(any(x >= box['x'] and y >= box['y'] and x + w <= box['x'] + box['w'] and y + h <= box['y'] + box['h'] for box in boxes.values()) for item, x, y, w, h in envelopes if item['type'] == 'text'))


def main():
    figures = {**EARLY, **LATE}
    check('figure registries have no overlapping units', not (set(EARLY) & set(LATE)))
    check('ten units each have two figures', set(figures) == set(range(10)) and all(len(value) == 2 for value in figures.values()))
    all_specs = [spec for unit in sorted(figures) for spec in figures[unit]]
    all_ids = [spec['id'] for spec in all_specs]
    check('twenty distinct figure identifiers', len(all_ids) == len(set(all_ids)) == 20)
    check('figure identifiers are safe filenames', all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident) for ident in all_ids))
    by_id = {spec['id']: spec for spec in all_specs}
    lessons = {}

    for unit, specs in sorted(figures.items()):
        check(f'unit {unit} public registry matches authored figures', figures_for(unit) == specs)
        lesson = read_json(ROOT / f'ERP/lessons/{unit:02}.json')
        if not lesson:
            continue
        lessons[unit] = lesson
        sections = {section['id']: section for section in lesson['unitGuide']['sections']}
        attached = [spec['id'] for section in sections.values() for spec in section.get('figures', [])]
        check(f'unit {unit} attaches each figure once', Counter(attached) == Counter(spec['id'] for spec in specs))
        manuscript_files = list((ROOT / '03_Level1_교재').glob(f'{unit:02}_*.md'))
        check(f'unit {unit} has one manuscript', len(manuscript_files) == 1)
        manuscript = text_at(manuscript_files[0]) if len(manuscript_files) == 1 else ''
        for spec in specs:
            ident = spec['id']
            check(ident + ' has teaching explanation and question', all(isinstance(spec.get(key), str) and spec[key].strip() for key in ['title', 'lead', 'caption', 'question']))
            check(ident + ' targets a real chapter section', spec['section'] in sections)
            check(ident + ' stage matches its chapter section', spec['stage'] in rank and spec.get('stage') == sections.get(spec['section'], {}).get('stage'))
            check(ident + ' source evidence is available', bool(spec['sources']) and all(source in source_stage and rank[source_stage[source]] <= rank[spec['stage']] for source in spec['sources']))
            node_ids = [node['id'] for node in spec['nodes']]
            check(ident + ' node identifiers are unique', len(node_ids) == len(set(node_ids)) > 0)
            check(ident + ' node labels are present', all(node.get('title') and node.get('lines') and all(isinstance(line, str) and line.strip() for line in node['lines']) for node in spec['nodes']))
            check(ident + ' relationships connect existing nodes', all(edge['from'] in node_ids and edge['to'] in node_ids and edge['from'] != edge['to'] and edge.get('label') for edge in spec['edges']))
            check(ident + ' desktop rows contain each node exactly once', Counter(node for row in spec['rows'] for node in row) == Counter(node_ids))
            check(ident + ' desktop rows are not empty', all(spec['rows']))
            section = sections.get(spec['section'], {})
            html = FigureHTML(section.get('html', ''))
            check(ident + ' is embedded in the reading section', html.figures.count(ident) == 1 and 'chapter-figure' in html.classes)
            check(ident + ' has desktop and mobile presentations', {'figure-desktop', 'figure-mobile'} <= html.classes and html.svg > 0)
            mobile = ''.join(html.mobile_text)
            check(ident + ' mobile alternative retains nodes and relationships', all(node['title'] in mobile and all(line in mobile for line in node['lines']) for node in spec['nodes']) and all(edge['label'] in mobile for edge in spec['edges']))
            readable = ''.join(html.text)
            check(ident + ' explanation and application question are visible', spec['caption'] in readable and spec['question'] in readable)
            expected_link = f'![{spec["title"]}](../03_Level1_교재/그림/{ident}.svg)'
            check(ident + ' manuscript links its editable SVG', expected_link in manuscript)
            check(ident + ' manuscript includes explanation and application', spec['caption'] in manuscript and spec['question'] in manuscript)
            generated = svg_figure(spec)
            svg_checks(spec, generated, ident + ' renderer')
            stored = text_at(ROOT / '03_Level1_교재/그림' / f'{ident}.svg')
            check(ident + ' stored SVG matches renderer', stored.strip() == generated.strip())
            svg_checks(spec, stored, ident + ' file')
            geometry_checks(spec)

    for stage in STAGES:
        base = ROOT / '배포본/단계자료' / stage
        visible = {spec['id'] for spec in all_specs if rank[spec['stage']] <= rank[stage]}
        actual = {path.stem for path in (base / '03_Level1_교재/그림').glob('*.svg')}
        check(stage + ' contains exactly the available figure SVGs', actual == visible)
        print_manuscript = text_at(base / '교재_인쇄원고.md')
        for unit in range(10):
            lesson = read_json(base / f'ERP/lessons/{unit:02}.json')
            if not lesson:
                continue
            sections = lesson['unitGuide']['sections']
            attached = [spec['id'] for section in sections for spec in section.get('figures', [])]
            expected = {spec['id'] for spec in figures[unit] if spec['id'] in visible}
            check(f'{stage}/{unit} exposes only released figure specs', set(attached) == expected and len(attached) == len(expected))
            markup = '\n'.join(section.get('html', '') for section in sections)
            figure_html = FigureHTML(markup)
            check(f'{stage}/{unit} exposes only released inline figures', set(figure_html.figures) == expected and len(figure_html.figures) == len(expected))
            for section in sections:
                if rank[section['stage']] > rank[stage]:
                    check(f'{stage}/{unit}/{section["id"]} future section loses figure content', set(section) == {'id', 'title', 'stage', 'locked'} and section['locked'])
        for ident, spec in by_id.items():
            check(f'{stage}/{ident} print release boundary', (f'/그림/{ident}.svg)' in print_manuscript) == (ident in visible))
            if ident in visible:
                released = text_at(base / '03_Level1_교재/그림' / f'{ident}.svg')
                check(f'{stage}/{ident} released SVG preserves its content', released.strip() == svg_figure(spec).strip())

    report = {'date': date.today().isoformat(), 'figures': len(all_ids), 'passed': sum(item['passed'] for item in checks), 'total': len(checks), 'scope': 'Authored figure structure, source stages, SVG/HTML/manuscript integration and all seven stage folders. Browser font layout and PDF appearance are separate visual checks.', 'checks': checks}
    if '--json' in sys.argv:
        print(json.dumps(report, ensure_ascii=False))
    assert all(item['passed'] for item in checks), f'{report["total"] - report["passed"]} figure checks failed'
    if '--json' not in sys.argv: print(f'{report["passed"]}/{report["total"]} figure checks passed; {len(all_ids)} figures')


if __name__ == '__main__':
    main()
