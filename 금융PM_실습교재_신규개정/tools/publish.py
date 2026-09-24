"""Render independent Korean PDFs with embedded font. Requires reportlab."""
from pathlib import Path
import re,os,html
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,LongTable,TableStyle,KeepTogether
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]
font=os.environ.get('PM_KOREAN_FONT')
if not font:
 candidates=list(Path('/System/Library/AssetsV2').rglob('NanumGothic.ttc')) if Path('/System/Library/AssetsV2').exists() else []
 candidates+=list(Path('/usr/share/fonts').rglob('NanumGothic.ttf')) if Path('/usr/share/fonts').exists() else []
 if not candidates:raise SystemExit('Set PM_KOREAN_FONT to a Korean TrueType font path')
 font=str(candidates[0])
pdfmetrics.registerFont(TTFont('Korean',font,subfontIndex=0))
pdfmetrics.registerFontFamily('Korean',normal='Korean',bold='Korean',italic='Korean',boldItalic='Korean')
S={
 'body':ParagraphStyle('body',fontName='Korean',fontSize=10,leading=17,wordWrap='CJK',spaceAfter=8,textColor=colors.HexColor('#253b4d')),
 'h1':ParagraphStyle('h1',fontName='Korean',fontSize=21,leading=29,wordWrap='CJK',spaceAfter=18,textColor=colors.HexColor('#1d3152'),keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Korean',fontSize=14,leading=21,wordWrap='CJK',spaceBefore=15,spaceAfter=9,textColor=colors.HexColor('#11354e'),keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Korean',fontSize=11,leading=18,wordWrap='CJK',spaceBefore=12,spaceAfter=7,textColor=colors.HexColor('#355d9e'),keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Korean',fontSize=8,leading=12,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='Korean',fontSize=9,leading=14,wordWrap='CJK',spaceAfter=6),
}
def clean(s):
 s=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',s)
 s=s.replace('**','').replace('`','').replace('<br>',' / ')
 return html.escape(s)
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#cddbdc'));c.line(48,42,547,42)
 c.setFont('Korean',8);c.setFillColor(colors.HexColor('#607888'));c.drawString(48,29,'모아페이 · 금융 프로젝트 PM 실습 · Level 1');c.drawRightString(547,29,str(doc.page))
def make(source,target,title,subtitle):
 story=[Spacer(1,95),Paragraph('MOAPAY / PM BOOTCAMP',S['small']),Paragraph(title,S['h1']),Paragraph(subtitle,S['body']),Spacer(1,25),Paragraph('49개 프로세스 · 하나의 프로젝트 · 근거에서 승인까지',S['h2']),Paragraph('독립 신규개정판 / 심화 설명·시각화 연계 개정 2026-09-24 / 가상회사 교육자료',S['body']),PageBreak()]
 text=(ROOT/source).read_text();lines=text.splitlines();i=0
 headings=[x[2:] for x in lines if x.startswith('# ')]
 story += [Paragraph('차례',S['h1'])]+[Paragraph(h,S['small']) for h in headings]+[PageBreak()]
 first=True;workbook='워크북' in source;exercises=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('# '):
   if not first:story.append(PageBreak())
   first=False;exercises=0;story.append(Paragraph(clean(line[2:]),S['h1']));i+=1;continue
  if line.startswith('## '):
   if workbook and line.startswith('## 실습 '):
    if exercises:story.append(PageBreak())
    exercises+=1
   story.append(Paragraph(clean(line[3:]),S['h2']));i+=1;continue
  if line.startswith('### '):
   story.append(Paragraph(clean(line[4:]),S['h3']));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    r=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[-: ]+',c) for c in r):rows.append(r)
    i+=1
   if not rows:continue
   n=len(rows[0]);widths=[499/n]*n
   if rows[0]==['단원','업무','시작 자료','안내 단계 수','다음에 넘길 것']:widths=[28,80,40,46,305]
   elif n==2:widths=[135,364]
   elif n==3:widths=[100,260,139]
   cooked=[[Paragraph(clean(c),S['cell']) for c in r] for r in rows]
   t=LongTable(cooked,colWidths=widths,repeatRows=1,hAlign='LEFT',minRowHeights=[23]+[45 if workbook and n==2 and rows[0][0]=='작성 항목' else 30 if workbook else 23]*(len(rows)-1))
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1efed')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fa')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#9bb7bc')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#dce5e9'))]))
   story.extend([t,Spacer(1,10)]);continue
  if line.startswith('```'):i+=1;continue
  if line.startswith('- '):line='• '+line[2:]
  story.append(Paragraph(clean(line),S['body']));i+=1
 out=ROOT/target;out.parent.mkdir(parents=True,exist_ok=True)
 doc=SimpleDocTemplate(str(out),pagesize=(595,842),leftMargin=48,rightMargin=48,topMargin=48,bottomMargin=57,title=title,author='모아페이 PM 실습실')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(out)
if __name__=='__main__':
 for source,name,title,sub in [('Level1_교재','Level1_교재','프로젝트를 문서로 관리하는 법','개념·수행 안내·회사자료'),('Level1_워크북','Level1_워크북','직접 작성하는 PM 실습 워크북','49개 실습·31개 문서별 양식'),('강사용_해설','강사용_해설','검토와 피드백을 위한 강사 해설','기준 답안·계산 근거·완성문서 / 학습자 배포 금지')]:make(f'출판원고/{source}.md',f'배포본/PDF/{name}.pdf',title,sub)
 from stage_materials import prepare
 for stage,base in prepare().items():
  for kind in ['교재','워크북']:
   make(str((base/f'{kind}_인쇄원고.md').relative_to(ROOT)),str((base/f'배포본/PDF/Level1_{kind}.pdf').relative_to(ROOT)),f'모아페이 Level 1 {kind}',f'{stage} 공개본 · 이후 시점의 사례·결과는 추가팩에서 공개')
