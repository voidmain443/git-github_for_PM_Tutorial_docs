from pathlib import Path
import zipfile,hashlib,json
from build import ROOT,STAGES,write

def make(name,files,notes=None,overrides=None):
 out=ROOT/'배포본'/name;out.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(set(files)):
   if p.is_file() and str(p.relative_to(ROOT)) not in (overrides or {}):z.write(p,p.relative_to(ROOT))
  for name,path in (overrides or {}).items():z.write(path,name)
  if notes:z.writestr('이_팩의_사용법.md',notes)
 return out

def package():
 from stage_materials import prepare
 stages=prepare()
 def release(stage):
  base=stages[stage]
  files={str(p.relative_to(base)):p for directory in ['ERP','03_Level1_교재','04_Level1_워크북','배포본/PDF'] for p in (base/directory).rglob('*') if p.is_file()}
  for kind in ['교재','워크북']:
   assert (base/f'배포본/PDF/Level1_{kind}.pdf').exists(),'Publish staged PDFs before packaging'
  return files
 student=[]
 for folder in ['01_회사자료','03_Level1_교재','04_Level1_워크북']:
  student+=list((ROOT/folder).rglob('*'))
 student += list((ROOT/'02_원천문서/S0').glob('*'))+list((ROOT/'ERP').glob('*.csv'))
 student += list((ROOT/'ERP/lessons').glob('*.json'))
 student += [ROOT/'README_실행환경.md']
 student += [ROOT/'ERP/study-workspace.js',ROOT/'ERP/study-workspace.css',ROOT/'ERP/onboarding.js',ROOT/'ERP/app.js',ROOT/'ERP/guide.html',ROOT/'ERP/처음_사용하는_ERP.md']
 student += [ROOT/'README.md',ROOT/'ERP/server.py',ROOT/'ERP/index.html',ROOT/'ERP/learn.html',ROOT/'ERP/schema.sql',ROOT/'ERP/queries.sql',ROOT/'ERP/데이터사전_SAP대응.md',ROOT/'ERP/data/S0.sqlite3',ROOT/'배포본/PDF/Level1_교재.pdf',ROOT/'배포본/PDF/Level1_워크북.pdf']
 make('학습자_시작.zip',student,'# 시작팩\n\nS0 자료와 설명·예제·PDF만 포함합니다. 이후 단계는 목차만 보이며 추가팩을 받으면 열립니다. README의 실행 안내로 시작하세요. 강사용 전체 답안과 미래 DB는 포함하지 않았습니다.\n',release('S0'))
 for stage in [s for s in STAGES if s!='S0']:
  make(f'학습자_{stage}_추가.zip',list((ROOT/f'02_원천문서/{stage}').glob('*'))+[ROOT/f'ERP/data/{stage}.sqlite3'],f'# {stage} 추가팩\n\n이전팩과 같은 폴더에 압축을 풉니다. 설명·예제·PDF도 해당 시점까지 갱신됩니다. 학습 안내 상단의 자료 선택에서 {stage}를 선택하고 「선택한 자료 열기」를 누릅니다. ERP 탭도 새로고침합니다. 자료 순서는 S0→S0A→S1→S1A→S2→S3→S4이며 자료 열기는 문서 승인을 대신하지 않습니다.\n',release(stage))
 teacher=[]
 for folder in ['00_설계','01_회사자료','02_원천문서','03_Level1_교재','04_Level1_워크북','05_강사용','ERP','tools','출판원고','검증']:
  teacher += [p for p in (ROOT/folder).rglob('*') if '__pycache__' not in str(p) and p.suffix not in ['.png','.pyc']]
 teacher += list((ROOT/'배포본/PDF').glob('*.pdf'))+[ROOT/'README.md',ROOT/'README_실행환경.md']
 make('강사_전체.zip',teacher,'# 강사 전체팩\n\n미래 자료와 정답이 포함되어 있습니다. 학생에게 이 팩을 배포하지 마세요. 교재를 수정했다면 tools/rebuild.py --pdf --package로 다시 만듭니다.\n')
 # Assert separation inside actual archives, not just selected filenames.
 with zipfile.ZipFile(ROOT/'배포본/학습자_시작.zip') as z:
  names=z.namelist();assert not any('05_강사용' in n or '강사용_해설' in n or 'tools/' in n or any('/'+s+'/' in n for s in STAGES if s!='S0') for n in names)
  assert [n for n in names if n.endswith('.sqlite3')]==['ERP/data/S0.sqlite3']
 manifest=[]
 for p in sorted((ROOT/'배포본').glob('*.zip')):manifest.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 write('배포본/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
 write('검증/배포분리검증.md','# 배포 분리 검증\n\n학습자 시작 ZIP에서 강사용 해설·완성 문서·제작 도구·미래 스냅샷이 없음을 검사했다. 시작 DB는 S0 한 개다. 다음 단계는 누적된 이전 팩 위에 추가한다. JSON·교재 원고·PDF의 미래 단계는 제목만 남기고 설명과 예제는 해당 추가팩에서 공개한다. 실제 ZIP만 추출한 독립 실행 결과는 읽기교재_독립배포검증.json을 확인한다.\n')
 print('Built learner starter, six stage packs and teacher archive; separation checked.')
if __name__=='__main__':package()
