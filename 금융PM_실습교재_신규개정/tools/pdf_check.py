from pathlib import Path
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image,ImageDraw
import pdfplumber,json
root=Path(__file__).resolve().parents[1];out=root/'검증/PDF검토';out.mkdir(exist_ok=True)
report=[]
files=list((root/'배포본/PDF').glob('*.pdf'))+list((root/'배포본/단계자료').glob('*/배포본/PDF/*.pdf'))
for f in files:
 stem=f.stem if '단계자료' not in f.parts else f.parents[2].name+'_'+f.stem
 pdf=pdfium.PdfDocument(str(f));thumbs=[]
 for i,p in enumerate(pdf):
  im=p.render(scale=.5).to_pil().convert('RGB');im.thumbnail((238,337));tile=Image.new('RGB',(250,364),'#dde4e9');tile.paste(im,(6,20));ImageDraw.Draw(tile).text((8,4),str(i+1),fill='black');thumbs.append(tile)
 for start in range(0,len(thumbs),20):
  sheet=Image.new('RGB',(1250,1456),'white')
  for j,t in enumerate(thumbs[start:start+20]):sheet.paste(t,((j%5)*250,(j//5)*364))
  sheet.save(out/f'{stem}_{start+1:03}.png')
 for i in [3,min(8,len(pdf)-1),len(pdf)-2]:pdf[i].render(scale=1.3).to_pil().save(out/f'{stem}_상세_{i+1}.png')
 txt=''.join(p.extract_text() or '' for p in PdfReader(f).pages)
 assert '프로젝트' in txt and '모아페이' in txt
 bad=[]
 with pdfplumber.open(f) as check:
  for i,p in enumerate(check.pages,1):
   for c in p.chars:
    if c['x0']<40 or c['x1']>554 or c['top']<30 or c['bottom']>824:bad.append((i,c['text']))
 assert not bad,(f,bad[:10])
 report.append({'file':str(f.relative_to(root/'배포본')),'pages':len(pdf),'characters':len(txt),'outside_page_content_bounds':len(bad)})
(root/'검증/PDF검증.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
