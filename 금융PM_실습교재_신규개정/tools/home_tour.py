"""Render the allowlisted, prerecorded UI tour. Captures are versioned assets."""
import hashlib
import html
import json
import re

GUIDANCE = {
 'read': dict(title='본문을 읽고, 같은 단원의 실습으로 이동합니다.',action='교재에서 0단원의 본문을 읽습니다. 위쪽 「단계별 실습하기」 또는 본문 끝의 「이 단원의 단계별 실습 시작하기」를 누릅니다.',check='내가 맡은 일과 만들 문서를 먼저 확인합니다. 실습에서는 개념 → 근거·예제 → 작성·검토 순서로 화면이 나뉩니다.',handoff='다음에는 「근거·예제」에서 설명에 쓰인 원천자료를 직접 엽니다.',link='learn.html?unit=0',linkText='0단원 본문 열기 →',short='본문 읽기'),
 'source': dict(title='설명에 나온 S01 원천 문서를 직접 읽습니다.',action='0단원 첫 실습에서 「2. 근거·예제」를 누른 뒤 「S01 … 읽기」 버튼을 누릅니다. 문서는 같은 화면 안에서 열립니다.',check='문서 제목·버전·적용일과 사업 필요를 확인합니다. 출처가 S01이라는 사실과 내가 해석한 내용을 구분해 메모합니다.',handoff='실제 숫자가 필요하면 교재의 ERP 조회 링크를 따라 한 건을 확인합니다.',link='learn.html?unit=0&view=practice&step=start&phase=evidence',linkText='원천자료 읽기 실습 열기 →',short='원천 열기'),
 'erp': dict(title='ERP에서 정산번호 한 건을 찾아 상세를 확인합니다.',action='교재의 「ST001 함께 조회」로 ERP를 엽니다. 「정산번호 = ST001」 조건을 확인하고 「조회」를 누릅니다. 목록의 ST001을 누르면 상세·연관 기록을 볼 수 있습니다.',check='검색 결과 1건과 지급예정액 222,440원을 확인합니다. 이 금액은 가맹점 정산금입니다. 회사 매출이나 프로젝트 비용과 섞지 않습니다.',handoff='조회가 끝나면 교재 탭으로 돌아와 산식과 자료의 의미를 설명해 봅니다. CSV는 필요한 경우에만 내려받습니다.',link='learn.html?unit=0&view=practice&step=settlement&phase=evidence',linkText='정산 조회 실습 열기 →',short='ERP 조회'),
 'write': dict(title='근거를 짧게 작성하고, 내 파일로 보관합니다.',action='「3. 작성·검토」에서 「웹에서 양식 작성하기」를 열고 G00 양식을 선택합니다. 표에 메모를 적은 뒤 「작성본 내려받기」를 누릅니다.',check='확인한 사실 옆에 자료 ID와 자신의 해석을 남깁니다. 영상은 한 항목의 예시입니다. 전체 메모는 교재의 작성 항목을 따라 직접 완성하세요.',handoff='웹 초안은 페이지를 떠나거나 새로고침하면 사라집니다. 내려받은 파일을 보관하고 다음에는 「작성본 불러오기」로 이어 씁니다. 파일 편집기로 작성해도 됩니다.',link='learn.html?unit=0&view=practice&step=draft&phase=practice',linkText='메모 작성 실습 열기 →',short='작성·보관'),
 'review': dict(title='검토 의견으로 수정하고, 다음 업무에 넘깁니다.',action='0단원 마지막 실습에서 검토 의견과 수정할 항목을 읽습니다. 자신의 G00을 보완한 뒤 「다음 단원」으로 이동해 헌장 작성을 시작합니다.',check='자료를 찾았다는 사실보다 근거와 해석을 설명할 수 있는지 확인합니다. 버튼을 누르거나 다음 단원으로 이동하는 것이 문서 승인을 뜻하지는 않습니다.',handoff='다음 단원에는 G00과 확인한 원천을 가져갑니다. 작성한 파일을 보관한 뒤 이동하세요. 이후에도 같은 읽기 → 조회 → 작성 → 검토 흐름을 반복합니다.',link='learn.html?unit=0&view=practice&step=review&phase=practice',linkText='검토·수정 실습 열기 →',short='검토·인계'),
}

def build_tour(root):
    media=root/'ERP/tour-media'
    manifest=json.loads((media/'manifest.json').read_text())
    clips=manifest['clips']
    assert [c['id'] for c in clips]==list(GUIDANCE)
    assert manifest['stage']=='S0'
    files={'manifest.json'}
    for c in clips:
        assert 0<c['durationMs']<=60000 and c['width']>0 and c['height']>0
        assert len(c['frames'])>=2 and c['frames'][0]['atMs']==0
        assert all(a['atMs']<b['atMs'] for a,b in zip(c['frames'],c['frames'][1:]))
        assert c['frames'][-1]['atMs']<c['durationMs']
        files.update([c['gif'],c['poster'],*[f['still'] for f in c['frames']]])
        c.update(GUIDANCE[c['id']])
    for name in files:
        assert re.fullmatch(r'[a-z0-9][a-z0-9_.-]*\.(gif|webp|json)',name),name
        assert (media/name).is_file(),name
        if name.endswith('.gif'):assert (media/name).read_bytes()[:6] in [b'GIF87a',b'GIF89a']
    for c in clips:
        binary=(media/c['gif']).read_bytes()
        assert len(binary)==c['bytes'] and hashlib.sha256(binary).hexdigest()==c['sha256'],c['id']
    for name,digest in manifest.get('sha256',{}).items():
        assert name in files and hashlib.sha256((media/name).read_bytes()).hexdigest()==digest,name
    first=clips[0]
    markup=(root/'ERP/home-tour.html').read_text()
    fields={'STEPS':''.join(f'<li><button type="button" data-tour-step="{c["id"]}" aria-pressed="{str(i==0).lower()}"><span>STEP {i+1:02}</span>{html.escape(c["short"])}</button></li>' for i,c in enumerate(clips)),
      'POSTER':'tour-media/'+first['frames'][0]['still'],'WIDTH':str(first['width']),'HEIGHT':str(first['height']),
      'ALT':first['frames'][0]['label'],'CAPTION':f'1 / {len(first["frames"])}컷 · '+first['frames'][0]['label'],
      'TITLE':first['title'],'ACTION':first['action'],'CHECK':first['check'],'HANDOFF':first['handoff'],
      'LINK':first['link'],'LINK_TEXT':first['linkText'],'GIF':'tour-media/'+first['gif']}
    for key,value in fields.items():markup=markup.replace('__TOUR_'+key+'__',value if key=='STEPS' else html.escape(value,quote=True))
    markup=markup.replace('__TOUR_DATA__',json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c'))
    assert '__TOUR_' not in markup
    return markup,sorted(files)
