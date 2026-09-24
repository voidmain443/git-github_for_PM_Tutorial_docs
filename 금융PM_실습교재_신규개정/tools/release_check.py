"""Run the learner ZIPs in an empty directory, without source-tree imports."""
from pathlib import Path
import hashlib,json,socket,subprocess,sys,tempfile,time,urllib.request,urllib.error,zipfile

ROOT=Path(__file__).resolve().parents[1]
STAGES=['S0','S0A','S1','S1A','S2','S3','S4']
checks=[]
def check(label,ok):
    checks.append({'name':label,'passed':bool(ok)})
    assert ok,label

with tempfile.TemporaryDirectory(prefix='moapay-learner-') as td:
    base=Path(td)
    with zipfile.ZipFile(ROOT/'배포본/학습자_시작.zip') as z:z.extractall(base)
    check('starter contains only S0 database',sorted(p.stem for p in (base/'ERP/data').glob('*.sqlite3'))==['S0'])
    check('starter has no instructor content or builder',not (base/'05_강사용').exists() and not (base/'tools').exists())
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    url=f'http://127.0.0.1:{port}'
    def get(path):
        with urllib.request.urlopen(url+path,timeout=5) as r:return r.read()
    def post(stage):
        req=urllib.request.Request(url+'/api/stage',json.dumps({'stage':stage}).encode(),headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req,timeout=5) as r:return r.status,json.load(r)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    server=subprocess.Popen([sys.executable,'ERP/server.py','--port',str(port)],cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        for _ in range(50):
            try:get('/api/meta');break
            except (OSError,urllib.error.URLError):time.sleep(.1)
        else:raise RuntimeError('Isolated learner server did not start')
        check('optional worksheet script packaged and served',b'PMStudy' in get('/study-workspace.js'))
        check('optional worksheet styles packaged and served',b'study-panel' in get('/study-workspace.css'))
        check('uninstalled future stage refused',post('S0A')[0]==409)
        for stage in STAGES:
            if stage!='S0':
                with zipfile.ZipFile(ROOT/f'배포본/학습자_{stage}_추가.zip') as z:z.extractall(base)
                check(stage+' switches without restarting server',post(stage)[0]==200)
            check(stage+' database stage',json.loads(get('/api/meta'))['stage']==stage)
            check(stage+' guide served','웹페이지에 답을 입력할 필요는 없습니다' in get('/guide').decode())
            check(stage+' reader served','onboarding.js' in get('/learn?unit=0').decode())
            for unit in range(10):
                lesson=json.loads(get(f'/api/lesson?unit={unit}'))
                for step in lesson['guideSteps']:
                    if step['stage']>stage:
                        check(f'{stage}/{unit}/{step["id"]} future content withheld',step['locked'] and 'html' not in step and 'sections' not in step)
                    else:
                        check(f'{stage}/{unit}/{step["id"]} released lesson readable',bool(step.get('html')) and not step.get('locked'))
                        for sid in step['sources']:
                            detail=json.loads(get('/api/detail?menu=documents&id='+sid))
                            assert detail['document'],(stage,unit,sid)
            for kind in ['교재','워크북']:
                pdf=base/f'배포본/PDF/Level1_{kind}.pdf'
                expected=ROOT/f'배포본/단계자료/{stage}/배포본/PDF/Level1_{kind}.pdf'
                check(stage+' '+kind+' PDF matches released stage',hashlib.sha256(pdf.read_bytes()).digest()==hashlib.sha256(expected.read_bytes()).digest())
        check('instructor folder never introduced',not (base/'05_강사용').exists())
        check('all stages installed in order',sorted(p.stem for p in (base/'ERP/data').glob('*.sqlite3'))==sorted(STAGES))
    finally:
        server.terminate()
        try:server.wait(timeout=5)
        except subprocess.TimeoutExpired:server.kill();server.wait()

report={'date':'2026-09-24','passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'Actual learner ZIPs extracted into an empty temporary directory; one server, seven stages. This is a technical check, not a novice learning pilot.','checks':checks}
(ROOT/'검증/읽기교재_독립배포검증.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'{report["passed"]}/{report["total"]} isolated release checks passed')
