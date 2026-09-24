"""Allowlisted learner-only static publication. Run rebuild.py first."""
from pathlib import Path
import argparse,hashlib,html,json,re,shutil,sys
from urllib.parse import urlparse,parse_qs,quote
from build import ROOT,MODULES,STAGES
from onboarding import markdown_html
from stage_materials import prepare
from home_tour import build_tour

STYLE='''*{box-sizing:border-box}body{margin:0;background:#f6f4ef;color:#26334d;font:17px/1.8 system-ui,sans-serif}a{color:#355d9e}a:focus-visible,button:focus-visible,select:focus-visible{outline:3px solid #466eae;outline-offset:4px}header{border-bottom:1px solid #1d3152;background:#1d3152}header a{color:#f8f5ef}header a:focus-visible{outline-color:#e4bd83}nav,main,footer{max-width:1120px;margin:auto;padding:22px}nav{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}nav a{text-decoration:none}nav .links{display:flex;gap:22px;flex-wrap:wrap}.hero{padding:45px 0 30px;max-width:800px}.eyebrow{font-size:13px;letter-spacing:.14em;color:#8c5a24}h1{font-size:clamp(30px,5vw,48px);line-height:1.3;letter-spacing:-.04em}h2{font-size:26px;margin-top:42px}h3{font-size:19px;margin:0 0 10px}.muted{color:#626d7f}.actions{display:flex;gap:12px;flex-wrap:wrap;margin:25px 0}.button{display:inline-block;border:1px solid #8391a9;background:white;border-radius:9px;padding:12px 20px;text-decoration:none}.button:hover{background:#ebf0f8}.primary{background:#355d9e;color:white;border-color:#355d9e}.primary:hover{background:#284a82;border-color:#284a82}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}.card{background:#fffefb;border:1px solid #d8dde5;border-radius:12px;padding:24px}.card a{font-weight:600}.number{font-size:13px;color:#8c5a24}details{border-top:1px solid #d8dde5;margin-top:16px;padding:16px 0}summary{cursor:pointer;font-weight:600}table{border-collapse:collapse;width:100%;font-size:15px}td,th{border:1px solid #ccd5e2;padding:10px;vertical-align:top;text-align:left}.reading-table{overflow-x:auto}select,button{font:inherit;padding:9px;border:1px solid #8391a9;border-radius:6px}footer{font-size:13px;color:#626d7f}.skip{position:absolute;top:-60px}.skip:focus{top:5px;background:white;padding:12px}h1,h2,h3{color:#172b4d}th{background:#ebf0f8}p{overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf2fa;border:1px solid #d8dde5;border-radius:8px;padding:18px;font:14px/1.8 ui-monospace,monospace}@media(max-width:560px){main,nav,footer{padding:18px}.hero{padding-top:20px}.card{padding:20px}}'''
NAV='<a class="skip" href="#content">본문으로 바로가기</a><header><nav aria-label="주 메뉴"><a href="index.html"><strong>모아페이 · 금융 PM 실습</strong></a><div class="links"><a href="learn.html?unit=0">교재</a><a href="visual.html">시각화 워크북</a><a href="erp.html">ERP</a><a href="guide.html">사용 안내</a><a href="resources.html">자료실</a></div></nav></header>'
FOOTER='<footer>Level 1 · 가상 회사의 교육 자료 · 학습 기록을 서버에 제출하지 않습니다.<br>실제 수강생 파일럿과 수업 시간 측정은 별도 진행합니다.</footer>'

def shell(title,body,scripts=''):
    return f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="가상 핀테크 회사에서 헌장부터 종료까지 배우는 금융 프로젝트 PM 실습 교재"><title>{html.escape(title)} | 모아페이</title><style>{STYLE}</style>{NAV}<main id="content">{body}</main>{FOOTER}{scripts}</html>'

def href(value):
    if not value.startswith('/'):return value
    u=urlparse(value)
    routes={'/':'erp.html','/learn':'learn.html','/guide':'guide.html','/onboarding.js':'onboarding.js','/app.js':'app.js','/study-workspace.js':'study-workspace.js','/study-workspace.css':'study-workspace.css'}
    if u.path=='/download':return 'templates/'+quote(parse_qs(u.query)['name'][0])
    if u.path not in routes:raise ValueError('Unhandled static route '+value)
    return routes[u.path]+('?' + u.query if u.query else '')

def page_html(text):
    text=re.sub(r'(href|src)="(/[^"]*)"',lambda m:m[1]+'="'+html.escape(href(html.unescape(m[2])),quote=True)+'"',text)
    return text.replace('<script src="app.js">','<script>window.PM_SITE=true;</script><script src="app.js">')

def build(out):
    out=out.resolve()
    if out==ROOT or ROOT.is_relative_to(out):raise ValueError('Output must not contain the source tree')
    # Only delete a prior build made by this tool.
    if out.exists():
        if not (out/'.moapay-pages-output').exists():raise ValueError('Output exists and is not a recognized site build')
        shutil.rmtree(out)
    out.mkdir(parents=True);(out/'.moapay-pages-output').write_text('generated learner publication\n')
    def put(name,text):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    def copy(source,name):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,p)
    for src,dst in [('ERP/index.html','erp.html'),('ERP/learn.html','learn.html')]:put(dst,page_html((ROOT/src).read_text()))
    for f in ['app.js','onboarding.js','sqlite-worker.js','study-workspace.js','study-workspace.css']:copy('ERP/'+f,f)
    for f in ['visual-workbook.css','visual-workbook.mjs','visual-model.mjs','visual-motion.mjs','visual-extra.mjs','visual-extra.css']:copy('ERP/'+f,f)
    visual_scripts='<script>window.PM_SITE=true;</script><script src="app.js"></script><script src="vendor/d3.min.js"></script><script type="module" src="visual-workbook.mjs"></script>'
    put('visual.html',shell('시각화 워크북',(ROOT/'ERP/visual-workbook.html').read_text(),visual_scripts).replace('</style>', '</style><link rel="stylesheet" href="visual-workbook.css"><link rel="stylesheet" href="visual-extra.css">',1))
    for f in ['sql-wasm.js','sql-wasm.wasm','LICENSE.sql.js','provenance.json','d3.min.js','LICENSE.d3','provenance.d3.json']:copy('ERP/vendor/'+f,'vendor/'+f)
    provenance=json.loads((out/'vendor/provenance.json').read_text())
    for name,digest in provenance['files'].items():assert hashlib.sha256((out/'vendor'/name).read_bytes()).hexdigest()==digest
    d3_provenance=json.loads((out/'vendor/provenance.d3.json').read_text())
    for name,digest in d3_provenance['files'].items():assert hashlib.sha256((out/'vendor'/name).read_bytes()).hexdigest()==digest
    for stage,base in prepare().items():
        copy(f'ERP/data/{stage}.sqlite3',f'data/{stage}.sqlite3')
        for p in (base/'ERP/lessons').glob('*.json'):copy(p.relative_to(ROOT),f'lessons/{stage}/{p.name}')
        for kind in ['교재','워크북']:
            f=base/f'배포본/PDF/Level1_{kind}.pdf'
            if not f.exists():raise FileNotFoundError('Run rebuild.py --pdf before publishing: '+str(f))
            copy(f.relative_to(ROOT),f'print/{stage}/{kind}.pdf')
    put('standards.html',shell('PMI 표준과 이 교재의 적용',markdown_html((ROOT/'03_Level1_교재/표준을_읽는_방법.md').read_text())))
    templates=[]
    for p in sorted((ROOT/'04_Level1_워크북/양식').glob('*.md')):
        copy(p.relative_to(ROOT),'templates/'+p.name)
        preview='forms/'+p.stem+'.html';templates.append((p.name,preview))
        put(preview,shell(p.stem,'<p><a href="../resources.html">자료실로 돌아가기</a></p><p>표를 복사해 문서 편집기에서 작성하거나 아래 원본을 내려받으세요. 작성한 파일은 자신의 작업 폴더에 보관합니다.</p><a class="button" download href="../templates/'+quote(p.name)+'">편집용 원본 내려받기</a>'+markdown_html(p.read_text())).replace('href="index.html"','href="../index.html"').replace('href="learn.html','href="../learn.html').replace('href="erp.html"','href="../erp.html"').replace('href="guide.html"','href="../guide.html"').replace('href="resources.html"','href="../resources.html"').replace('href="visual.html"','href="../visual.html"'))
    summaries=['회사·사람·정산 자료를 읽는 첫날','사업 필요와 PM 권한을 헌장으로','요청을 요구와 인수조건으로','작업·자원·선후관계로 일정 만들기','추정에서 예산·자금 계획까지','품질 기준과 위험 대응 준비','외주 선정과 협업 방식 정하기','계획 통합·승인·실행 중 관리','성과 해석과 변경 전후 연결','검수·인수·이관 후 종료하기']
    cards=''.join(f'<article class="card"><span class="number">UNIT {i:02}</span><h3>{title}</h3><p>{summaries[i]}</p><a href="learn.html?unit={i}">{i}단원 읽기 →</a></article>' for i,title in enumerate(MODULES))
    tour,tour_files=build_tour(ROOT)
    body='''<section class="hero"><span class="eyebrow">LEVEL 1 / FINANCIAL PROJECT MANAGEMENT</span><h1>PM의 첫 업무를<br>자료에서 문서까지.</h1><p>여러분은 모아페이에 합류한 내부 PM 한지우입니다. 정산 담당자의 수작업을 줄이는 프로젝트를 맡아, 회사 자료를 읽고 헌장부터 종료보고까지 연결합니다.</p><div class="actions"><a class="button primary" href="learn.html?unit=0">0단원부터 시작하기 →</a><a class="button" href="guide.html">ERP 사용법 먼저 보기</a></div><p class="muted">설치·로그인 없이 시작 · 10개 단원 · 49개 프로세스 · 60절 단원 본문 · 69개 실습 단계</p></section>
'''+tour+'''
<section><h2>학생이 따라가는 10개 단원</h2><p>착수 → 분야별 계획 → 통합·실행 → 성과·변경 → 검수·종료 순서입니다. 뒤에서 확인한 조건은 앞서 만든 계획에도 반영합니다.</p><div class="grid">'''+cards+'''</div></section>
<section><h2>자료가 아직 없다면</h2><p>처음 조회 시점은 S0, 착수 전입니다. 승인된 기준선이나 실적이 비어 있는 것이 정상입니다. 교재에서 검토를 마친 뒤 상단의 자료 선택으로 다음 시점을 엽니다.</p><details><summary>초안·검토·승인은 어떻게 다른가요?</summary><p>초안은 PM이 작성한 제안입니다. 검토는 담당자가 근거와 조건을 확인하는 일입니다. 승인은 권한 있는 사람이 해당 버전을 결정하는 일입니다. 예제를 읽거나 다음 자료를 열었다고 내 문서가 자동 승인되는 것은 아닙니다.</p></details><details><summary>완성 답안과 개인정보는 어디에 있나요?</summary><p>이 사이트에는 학생 설명·부분 예제·빈 양식·가상 회사 자료를 제공합니다. 강사용 완성 답안과 개인 실습 기록은 배포하지 않습니다. 읽던 위치와 자료 선택만 이 브라우저에 저장됩니다.</p></details><details><summary>미래 자료가 잠겨 있는 이유는 무엇인가요?</summary><p>착수할 때 종료 결과를 먼저 보지 않도록 학습 순서를 나눴습니다. 공개 웹 교재의 자료 시점 선택은 학습 안내이며 접근 권한을 통제하는 기능은 아닙니다.</p></details></section>'''
    body+='<section class="card"><h2>Level 1 다음에는 무엇을 배우나요?</h2><p>먼저 근거를 찾아 문서를 연결하는 독립 수행을 확인합니다. 이후 변경과 편차, 상충하는 주장과 협상, 복수 프로젝트의 사업 성과로 확장합니다.</p><a href="pathway.html">완료 기준과 Level 2·3·4 학습 경로 →</a></section>'
    for name in tour_files:copy('ERP/tour-media/'+name,'tour-media/'+name)
    for name in ['home-tour.js','home-tour.css']:copy('ERP/'+name,name)
    put('index.html',shell('금융 프로젝트 PM 부트캠프',body,'<script src="home-tour.js" defer></script>').replace('</style>','</style><link rel="stylesheet" href="home-tour.css">',1))
    put('pathway.html',shell('완료 기준과 다음 레벨',markdown_html((ROOT/'ERP/학습경로.md').read_text())))
    manual=(ROOT/'ERP/처음_사용하는_ERP.md').read_text()
    manual=manual[:manual.index('## 10.')]
    manual=manual.replace('# 모의 ERP를 처음 사용하는 학생에게\n', '')
    manual=manual.replace('학습 안내 /learn에서는 설명·조회 경로·예제를 읽습니다. ERP 기본 화면 /에서는 회사 자료를 조회합니다.', '상단 「교재」에서는 설명·조회 경로·예제를 읽고, 「ERP」에서는 회사 자료를 조회합니다. 처음 방문했다면 페이지 위쪽의 「0단원부터 읽기」를 누르세요.')
    manual=manual.replace('## 5. 조회 기록에 남길 여섯 가지', '## 5. 작성 중인 문서에 근거를 남깁니다')
    manual=manual.replace('단계·기준일 / 메뉴 / 검색조건 / 행ID / 확인한 사실 / PM의 해석을 적습니다.', '별도의 웹 조회 기록을 작성할 필요는 없습니다. 내려받은 양식이나 자신의 메모에 단계·기준일 / 메뉴 / 검색조건 / 행ID / 확인한 사실 / PM의 해석을 함께 남깁니다.')
    manual=manual.replace('0단원 실습은 시작팩 S0에서 진행하고, 다음 자료팩은 교재의 인계 시점에 엽니다.', '0단원 실습은 교재 상단의 「현재 자료」가 S0인지 확인하고 진행합니다. 다음 자료는 교재의 인계 시점에 선택합니다.')
    manual=manual.replace('화면이 열리지 않으면 실습 서버가 실행 중인지 확인합니다. 파일 폴더만 열어 둔 상태로는 웹 화면이 열리지 않습니다. 실행 방법은 배포팩 README에 있습니다. 이미 다른 ERP 화면이 열리면 같은 주소의 /learn으로 돌아올 수 있습니다.','화면이 열리지 않으면 인터넷 연결과 주소를 확인한 뒤 새로고침하세요. 별도 서버 실행은 필요하지 않습니다. 위쪽 교재·ERP 메뉴로 다시 이동할 수 있습니다.')
    manual=manual.replace('읽던 위치는 이 브라우저에만 보존됩니다. 이전 버전에서 작성한 학습 기록은 삭제하지 않으며 「이전 작성 기록 내려받기」로 보관할 수 있습니다. 새 문서는 내려받은 양식에서 작성합니다.', '읽던 위치와 선택한 자료 시점은 이 브라우저에 보존됩니다. 다른 기기에서는 S0부터 열릴 수 있으니 먼저 자료 시점을 확인하세요. 작성한 문서는 사이트에 저장되지 않습니다. 자료실에서 내려받은 양식에 작성하고 자신의 작업 폴더에 보관하세요.')
    manual+='\n## 10. 공개 웹에서 자료 시점 바꾸기\n\n교재 상단의 자료 선택에서 S0 → S0A → S1 → S1A → S2 → S3 → S4 순서로 엽니다. 설치나 서버 재시작은 필요하지 않습니다. 먼저 해당 단계의 검토를 마칩니다. 선택은 이 브라우저에 저장되며 같은 사이트의 다른 탭도 갱신됩니다. 다른 학생의 시점은 바뀌지 않습니다. 공개 자료이므로 시점 선택은 접근 통제가 아닌 학습 순서 안내입니다.\n'
    guide_start='<h1>ERP 첫 사용 안내</h1><p>교재에서 할 일을 읽고, ERP에서 자료를 확인한 뒤, 내려받은 양식에 문서를 작성합니다. 아래 버튼으로 필요한 화면을 여세요.</p><div class="actions"><a class="button primary" href="learn.html?unit=0">0단원부터 읽기 →</a><a class="button" href="erp.html" target="_blank" rel="noopener">ERP 새 탭으로 열기 ↗</a><a class="button" href="resources.html">작성 양식 찾기</a></div>'
    put('guide.html',shell('ERP 첫 사용 안내',guide_start+markdown_html(manual)))
    formrows=''.join(f'<tr><td>{html.escape(n)}</td><td><a href="{quote(preview)}">양식 보기</a></td><td><a download href="templates/{quote(n)}">원본 내려받기</a></td></tr>' for n,preview in templates)
    company=''
    for p in sorted((ROOT/'01_회사자료').glob('*.md')):
        name='company/'+p.stem+'.html';company+=f'<li><a href="{quote(name)}">{html.escape(p.stem)}</a></li>'
        put(name,shell(p.stem,markdown_html(p.read_text())).replace('href="index.html"','href="../index.html"').replace('href="learn.html','href="../learn.html').replace('href="erp.html"','href="../erp.html"').replace('href="guide.html"','href="../guide.html"').replace('href="resources.html"','href="../resources.html"').replace('href="visual.html"','href="../visual.html"'))
    body='<h1>학습 자료실</h1><p><a class="button" href="visual.html">시각화 워크북 · 흐름도와 간트차트 열기 →</a></p><p>현재 단계의 인쇄본과 빈 양식을 제공합니다. 문서 본문은 한 번 작성하고, 다음 단원에서 같은 문서의 버전을 이어 갑니다.</p><section class="card"><h2>현재 자료의 인쇄본</h2><p id="print-stage"></p><div id="print-links" class="actions"></div><p class="muted">미래 단계의 설명·예제는 해당 자료 시점의 인쇄본에서 열립니다. 시점은 교재 상단에서 바꿉니다.</p></section><h2>PMI 표준과 학습 경로</h2><p><a href="standards.html">6판·8판을 이 교재에서 함께 읽는 방법</a> · <a href="pathway.html">완료 기준과 Level 2~4</a></p><h2>회사·용어 참고</h2><ul>'+company+'</ul><h2>편집할 문서 양식</h2><p>「양식 보기」에서 표를 읽고 복사하거나, Markdown 원본을 내려받아 사용하세요. 양식은 빈 문서이며 작성 예제는 해당 교재 단계에 있습니다.</p><div class="reading-table"><table><thead><tr><th>문서</th><th>브라우저로 보기</th><th>파일 보관</th></tr></thead><tbody>'+formrows+'</tbody></table></div>'
    scripts='<script>window.PM_SITE=true;</script><script src="app.js"></script><script>const stage=PMApp.currentStage();document.querySelector("#print-stage").textContent="현재 자료: "+stage;document.querySelector("#print-links").innerHTML=["교재","워크북"].map(k=>`<a class="button" href="print/${stage}/${encodeURIComponent(k)}.pdf" download>${k} PDF 내려받기</a>`).join("");</script>'
    put('resources.html',shell('학습 자료실',body,scripts))
    # Prefix-safe shared links on the original reader and ERP pages.
    for name in ['learn.html','erp.html']:
        p=out/name;s=p.read_text();s=s.replace('<header>', '<div style="padding:8px 22px;background:#ebf0f8"><a href="index.html">시작 안내</a> · <a href="visual.html">시각화 워크북</a> · <a href="resources.html">양식·인쇄본</a></div><header>',1);p.write_text(s)
    put('404.html',shell('페이지를 찾을 수 없습니다','<h1>주소를 다시 확인해 주세요.</h1><p>이전 주소를 사용했을 수 있습니다. 브라우저의 뒤로 가기로 돌아오거나 교재 첫 화면에서 다시 시작하세요.</p><p><a href="./">교재 첫 화면으로</a></p>'))
    put('.nojekyll','')
    files=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.rglob('*')) if p.is_file()]
    put('site-manifest.json',json.dumps({'edition':'2026-09-24-guided-tour','stages':list(STAGES),'units':10,'processes':49,'files':files},ensure_ascii=False,indent=2))
    forbidden=['05_강사용','06_실습수행기록','완성문서','강사용_해설','모의헌장기록','강사_전체.zip']
    assert not any(any(x in f['path'] for x in forbidden) for f in files)
    print(f'Built learner Pages site: {len(files)} files, {sum(f["bytes"] for f in files):,} bytes -> {out}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'_site'));args=parser.parse_args();build(Path(args.output))
