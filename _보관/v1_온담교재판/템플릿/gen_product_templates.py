# -*- coding: utf-8 -*-
"""Product 트랙 빈 템플릿 생성기 — Product_specs.py → 템플릿/Product_DayN/src/{NN_body.tex, NN_<file>_빈템플릿.tex, wbstyle.sty, build.sh}
사용: cd 교재/템플릿 && python3 gen_product_templates.py  (완성 예시 드라이버는 워크북 X.5 확정 후 추가)"""
import os,re,shutil,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from Product_specs import SPECS
try:
    from Product_fills import FILLS
except ImportError:
    FILLS={}
HERE=os.path.dirname(os.path.abspath(__file__))
CIRC={21:"㉑",22:"㉒",23:"㉓",24:"㉔",25:"㉕",26:"㉖",27:"㉗",28:"㉘",29:"㉙",30:"㉚",31:"㉛",32:"㉜",33:"㉝",34:"㉞",35:"㉟",36:"㊱",37:"㊲",38:"㊳",39:"㊴",40:"㊵"}
DAYTOPIC={5:"프리시드",6:"시드",7:"PMF 추적",8:"시리즈A·엔터프라이즈"}

def esc(s):  # 표 셀·안내문용 최소 이스케이프 (&, %, # ) — 명세는 이미 \\& 를 쓰는 곳이 있어 이중 처리 방지
    s=s.replace('\\&','\x00')
    s=s.replace('&','\\&').replace('%','\\%').replace('#','\\#').replace('_','\\_').replace('\x00','\\&')
    return s

def wbstyle_product():
    src=open(os.path.join(HERE,'PM_Day1','src','wbstyle.sty'),encoding='utf-8').read()
    src=src.replace('온담F&B PM 특강 Day1 워크북 산출물 템플릿 공통 스타일','딥게이지 Product 특강 워크북 산출물 템플릿 공통 스타일 (PM_Day1/src/wbstyle.sty 파생)')
    src=src.replace('\\ProvidesPackage{wbstyle}[2026/09/12 Ondam workbook template style]','\\ProvidesPackage{wbstyle}[2026/09/13 DeepGauge workbook template style]')
    # header/footer 문구
    src=src.replace('{\\small 온담F\\&B 특강 워크북 · Day1}\\\\\n    {\\small 산출물 \\DocNum/5 · \\DocVariant}',
                    '{\\small 딥게이지 Product 특강 워크북 · Day\\DocDay}\\\\\n    {\\small 산출물 \\DocCirc\\ (\\DocIdx/5) · \\DocVariant}')
    src=src.replace('\\fancyfoot[L]{\\footnotesize 온담F\\&B 특강 워크북 · Day1 · 산출물 \\DocNum/5 — \\DocTitle\\ (\\DocVariant)}',
                    '\\fancyfoot[L]{\\footnotesize 딥게이지 Product 특강 워크북 · Day\\DocDay\\ · 산출물 \\DocCirc\\ — \\DocTitle\\ (\\DocVariant)}')
    src=src.replace('\\hd{문서명} & \\hd{프로젝트명} & \\hd{버전 / 기준일} & \\hd{작성자 (서명)} & \\hd{승인자 (서명)}',
                    '\\hd{문서명} & \\hd{회사 · 제품} & \\hd{버전 / 기준일(D+n)} & \\hd{작성자 (서명)} & \\hd{검토·승인자 (서명)}')
    # ㉛~㊵ 대체 글꼴
    src=src.replace('\\newunicodechar{−}{-}',
        '\\newunicodechar{−}{-}\n\\newfontfamily\\circfont{Hiragino Sans W3}\n'+''.join('\\newunicodechar{%s}{{\\circfont\\mdseries %s}}'%(c,c) for c in "㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵")+'\n\\newcommand{\\chk}{\\raisebox{-0.5pt}{$\\square$}}')
    src=src.replace('\\begin{minipage}[b]{0.72\\linewidth}','\\begin{minipage}[b]{0.66\\linewidth}').replace('\\begin{minipage}[b]{0.26\\linewidth}\\raggedleft','\\begin{minipage}[b]{0.32\\linewidth}\\raggedleft')
    assert '\\DocCirc' in src and 'circfont' in src
    return src

def render_item(it, fill=None):
    typ,title,guide,o=it
    out=[]
    if typ=='table' and o.get('land',False): out.append('\\landscapeon')
    out+=['\\secbar{%s}'%esc(title),'\\guide{%s}'%esc(guide)]
    if typ=='text':
        filled = esc(fill) if isinstance(fill,str) else '\\g{[완성 예시 — 워크북 §X.5 확정 후 기입]}'
        out.append('\\begin{fieldbox}\n\\ifwbblank\n\\lines{%d}{9.5mm}\n\\else\n%s\n\\fi\n\\end{fieldbox}'%(o['lines'],filled))
    elif typ=='table':
        cols=o['cols']; rows=o['rows']; labels=o.get('labels'); h=o.get('h',9); land=o.get('land',False)
        spec='|'+'|'.join(('L{%dmm}'%w if w else 'Y') for _,w in cols)+'|'
        head=' & '.join('\\hd{%s}'%esc(n) for n,_ in cols)+' \\\\ \\hline'
        body=[]
        n=len(labels) if labels else rows
        for i in range(n):
            first='\\rd{%dmm}%s'%(h,esc(labels[i])) if labels else '\\rd{%dmm}'%h
            body.append(first+' & '*(len(cols)-1)+' \\\\ \\hline')
        if isinstance(fill,list) and fill:
            fbody=[]
            for row in fill:
                cells=[esc(str(c)) for c in row]+['']*(len(cols)-len(row))
                fbody.append(' & '.join(cells[:len(cols)])+' \\\\ \\hline')
            tab='{\\footnotesize\n\\begin{tabularx}{\\linewidth}{%s}\\hline\n%s\n\\ifwbblank\n%s\n\\else\n%s\n\\fi\n\\end{tabularx}}'%(spec,head,'\n'.join(body),'\n'.join(fbody))
        else:
            tab='{\\footnotesize\n\\begin{tabularx}{\\linewidth}{%s}\\hline\n%s\n%s\n\\end{tabularx}}'%(spec,head,'\n'.join(body))
        out.append(tab)
        if land: out.append('\\landscapeoff')
        if o.get('note'): out.append('\\guide{%s}'%esc(o['note']))
    elif typ=='check':
        rows='\n'.join('\\rd{8mm}\\chk & %s & \\\\ \\hline'%esc(x) for x in o['items'])
        out.append('{\\footnotesize\n\\begin{tabularx}{\\linewidth}{|C{8mm}|Y|L{50mm}|}\\hline\n\\hd{} & \\hd{항목} & \\hd{확인 방법 · 비고} \\\\ \\hline\n%s\n\\end{tabularx}}'%rows)
    elif typ=='sign':
        cols=len(o['names'])
        head=' & '.join('\\hd{%s}'%esc(n) for n in o['names'])+' \\\\ \\hline'
        blank_row='\\rd{16mm} '+'& '*(cols-1)+' \\\\ \\hline'
        if isinstance(fill,list):
            sig_row='\\rd{16mm} '+' & '.join(esc(x) for x in fill)+' \\\\ \\hline'
            rows='\\ifwbblank\n%s\n\\else\n%s\n\\fi'%(blank_row,sig_row)
        else:
            rows=blank_row
        out.append('{\\footnotesize\n\\begin{tabularx}{\\linewidth}{|%s}\\hline\n%s\n%s\n\\rd{7mm}일자 %s \\\\ \\hline\n\\end{tabularx}}'%('Y|'*cols,head,rows,'& '*(cols-1)))
    return '\n'.join(out)

def body_tex(num,sp):
    day=sp['day']; h=sp['header']; F=FILLS.get(num,{}); hf=F.get('header',('','','',''))
    L=['%% %02d_body.tex — 산출물 %s %s (빈 템플릿 / 완성 예시 공용 본문) — gen_product_templates.py 가 Product_specs.py 에서 생성'%(num,CIRC[num],sp['title']),
       '%% 드라이버: %02d_%s_빈템플릿.tex (\\wbblanktrue) / %02d_%s_완성예시.tex (\\wbblankfalse — 워크북 §X.5 확정 후)'%(num,sp['file'],num,sp['file']),
       '\\documentclass[10pt,a4paper]{article}',
       '\\usepackage[a4paper,margin=16mm,top=14mm,bottom=20mm]{geometry}',
       '\\def\\DocNum{%d}\\def\\DocDay{%d}\\def\\DocIdx{%d}'%(num,day,sp['idx']),
       '\\def\\DocTitle{%s}'%esc(sp['title']),
       '\\def\\DocSub{%s}'%sp['sub'],
       '\\def\\DocVariant{\\B{빈 템플릿}{딥게이지 완성 예시}}',
       '\\usepackage{wbstyle}',
       '\\def\\DocCirc{%s}   %% newunicodechar(㉛~㊵ 폴백) 뒤에 정의해야 활성 문자로 읽힌다'%CIRC[num],
       '\\begin{document}',
       '\\docheader',
       ' {\\Bg{%s}{%s}}'%(esc(h[0]),esc(hf[0])),' {\\Bg{%s}{%s}}'%(esc(h[1]),esc(hf[1])),' {\\Bg{%s}{%s\\rd{7mm}}}'%(esc(h[2]),esc(hf[2])),' {\\Bg{%s}{%s\\rd{7mm}}}'%(esc(h[3]),esc(hf[3])),'']
    for i,it in enumerate(sp['items'],1):
        L.append('%% '+'-'*66+' %d'%i); L.append(render_item(it, F.get(i))); L.append('')
    L.append('\\end{document}')
    return '\n'.join(L)

def driver(num,sp):
    return '\\newif\\ifwbblank\\wbblanktrue\n\\input{%02d_body.tex}\n'%num

def build_sh(day,nums):
    files=' '.join('%02d_*_빈템플릿.pdf'%n for n in nums)
    return f'''#!/bin/zsh
# 딥게이지 Product 특강 Day{day} 워크북 템플릿 빌드 — 사용: cd 교재/템플릿/Product_Day{day}/src && ./build.sh
# 완성 예시 드라이버(NN_*_완성예시.tex)는 워크북 §X.5 확정 후 추가하면 함께 빌드된다.
set -e
setopt null_glob
cd "$(dirname "$0")"
OUT=..
for f in [0-9][0-9]_*_빈템플릿.tex [0-9][0-9]_*_완성예시.tex; do
  [ -f "$f" ] || continue
  echo "== $f"
  tectonic --chatter minimal "$f" 2>&1 | grep -iv "accessing absolute\\|^warning:   you may\\|choose a different" || true
  mv -f "${{f%.tex}}.pdf" "$OUT/"
done
cd "$OUT"
pdfunite {files} 00_Day{day}_템플릿팩_빈양식.pdf
ls [1-9][0-9]_*_완성예시.pdf >/dev/null 2>&1 && pdfunite [1-9][0-9]_*_완성예시.pdf 00_Day{day}_템플릿팩_완성예시.pdf || true
ls -la *.pdf
'''

if __name__=='__main__':
    sty=wbstyle_product()
    bydays={}
    for num,sp in SPECS.items(): bydays.setdefault(sp['day'],[]).append(num)
    for day,nums in sorted(bydays.items()):
        d=os.path.join(HERE,'Product_Day%d'%day,'src'); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'wbstyle.sty'),'w',encoding='utf-8').write(sty)
        for num in sorted(nums):
            sp=SPECS[num]
            open(os.path.join(d,'%02d_body.tex'%num),'w',encoding='utf-8').write(body_tex(num,sp))
            open(os.path.join(d,'%02d_%s_빈템플릿.tex'%(num,sp['file'])),'w',encoding='utf-8').write(driver(num,sp))
            if num in FILLS:
                open(os.path.join(d,'%02d_%s_완성예시.tex'%(num,sp['file'])),'w',encoding='utf-8').write('\\newif\\ifwbblank\\wbblankfalse\n\\input{%02d_body.tex}\n'%num)
        bs=os.path.join(d,'build.sh'); open(bs,'w',encoding='utf-8').write(build_sh(day,sorted(nums))); os.chmod(bs,0o755)
        print('Day%d:'%day,sorted(nums))
