# GitHub Pages 운영 안내

공개 주소: https://voidmain443.github.io/git-github_for_PM_Tutorial_docs/

학생은 시작 화면 → 0단원 본문 읽기 → 단계별 실습(개념 → 근거·예제 → 작성·검토) → 다음 단원 순서로 진행한다. 로그인과 Python 설치가 필요 없다. 기존 교재·ERP의 사실과 시점은 동일하다.

## 공개 범위와 동작

- 첫 화면: 처음 읽을 순서, 10개 단원, 초안·검토·승인의 구분.
- 교재: 0~9단원의 60절 본문과 69개 실습 단계, 49개 프로세스. 단원마다 상황·자료 읽기·부분 예제·검토·수정·다음 업무를 연결한다.
- ERP: 같은 SQLite 스냅샷의 검색·필터·상세·집계·CSV·읽기 전용 SQL.
- 자료실: 회사·용어 참고, 빈 양식의 브라우저 미리보기·원본, 현재 단계의 교재·워크북 PDF.
- 강사용 완성 답안, 개인 실습 기록, 제작 도구와 검증 파일은 웹 산출물에 넣지 않는다.

S0→S0A→S1→S1A→S2→S3→S4를 교재의 자료 선택에서 연다. 브라우저에는 읽던 위치와 시점만 저장하며 작성한 문서를 서버로 보내지 않는다. 다른 탭은 같은 시점으로 갱신되고 다른 학생의 브라우저는 바뀌지 않는다.

GitHub Pages는 정적 사이트이므로 미래 자료의 시점 구분은 학습 순서 안내다. 공개된 파일의 접근 권한을 통제하거나 강사가 개별 학생의 진행을 강제하는 기능은 아니다. 엄격한 자료 공개 통제가 필요한 수업은 로컬 단계별 배포팩을 사용한다. 공개 저장소의 제작 원천도 강사용 보안 저장소로 취급하지 않는다.

## 자동 배포

저장소 루트의 `.github/workflows/financial-pm-pages.yml`이 다음을 수행한다.

1. Python·Node·한글 글꼴과 고정 버전 의존성을 준비한다.
2. 원천 데이터·교재·PDF를 다시 생성하고 자료·문서 연결·시점을 검사한다.
3. 학생 공개 목록에 포함된 파일만 `_site/`에 생성한다.
4. 실제 브라우저에서 로컬 ERP와 조회 결과를 비교하고 학생의 진행 흐름을 검사한다.
5. 검사가 성공한 main 브랜치만 GitHub Pages에 배포한다. PR에서는 검사만 진행한다.

실패한 빌드는 배포하지 않는다. Actions의 `classroom-validation`에서 검사 결과와 화면을 확인한다. 학생 산출물에는 강사용 파일이나 작업 폴더 전체를 업로드하지 않는다. sql.js 1.14.1은 라이선스와 해시를 함께 보관하며 실행 시 외부 CDN에 의존하지 않는다.

처음 설정하는 다른 저장소에서는 Settings → Pages → Build and deployment → Source를 GitHub Actions로 선택한다. 기본 브랜치가 main이 아니라면 워크플로의 브랜치 조건도 함께 변경한다.

## 로컬에서 공개본 확인

```sh
python3 -m pip install -r requirements-pages.txt
npm ci
npx playwright install chromium
python3 tools/rebuild.py --pdf
python3 tools/build_pages.py
npm run test:pages
python3 -m http.server 8880 --directory _site --bind 127.0.0.1
```

마지막 명령 뒤 http://127.0.0.1:8880/ 을 연다. `file://`로 HTML을 직접 열면 브라우저의 SQLite·자료 로딩이 동작하지 않는다. 테스트의 Python 명령은 PM_PYTHON, Chrome 실행파일은 PM_CHROME으로 지정할 수 있다.

Linux 글꼴: fonts-nanum 패키지. 그 밖의 환경에서는 NanumGothic.ttf 경로를 PM_KOREAN_FONT에 지정한다. 자료·양식은 생성 원고의 제작 규칙에서 수정한다. `_site/`는 결과물이므로 직접 고치지 않는다. 웹 첫 안내와 공개 파일 목록은 tools/build_pages.py, 단원 안내는 ERP/onboarding.js에서 관리한다.

## 운영 점검

배포 뒤 첫 화면, 0단원의 원천 열기, 양식 내려받기, ST001 정확 조회, SQL, 자료 시점 전환을 확인한다. 문제가 생기면 원인을 수정한 커밋을 올리거나 이전 정상 커밋으로 되돌려 다시 배포한다. 배포 이력은 GitHub Actions와 Environments → github-pages에 남는다.

실제 입문자의 이해도와 수행 시간은 별도 파일럿으로 확인한다. 공개 사이트가 동작한다는 사실을 교육 효과 검증으로 대신하지 않는다.

참고: [GitHub Pages 배포 워크플로](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [브라우저 SQLite sql.js](https://github.com/sql-js/sql.js).

## 홈의 실제 화면 안내

홈은 0단원의 본문 읽기 → S01 원천 열기 → ST001 ERP 조회 → G00 작성·내려받기 → 검토·인계 과정을 다섯 GIF로 보여 준다. 실제 S0 화면을 조작해 촬영한 안내이며 사용자의 자료 시점이나 작성본을 변경하지 않는다. 기본은 정지 화면이고 선택한 GIF만 명시적으로 재생한다. 한 컷씩 넘기기, 현재 컷 정지, 큰 화면 확인, 개별 GIF 내려받기도 가능하다. 화면을 벗어나거나 탭을 감추면 재생을 멈춘다.

`ERP/home-tour.html`, `.css`, `.js`가 표시와 조작을 담당하며 `tools/home_tour.py`가 설명과 직접 실습 링크를 연결한다. `ERP/tour-media/manifest.json`에는 실제 프레임의 순서·설명·시간·파일과 GIF 해시를 기록한다. 공개 빌드는 그 목록에 있는 미디어만 복사하며 GIF 해시를 확인한다. 총 다섯 GIF는 약 1.38MB이며 모든 정지 컷·포스터를 포함해 약 2.86MB다. 초기 페이지에서는 GIF를 받지 않는다.

화면의 버튼명이나 배치가 바뀌면 다음 순서로 다시 촬영한다. 캡처 환경에는 Playwright와 Chrome, 인코딩 환경에는 Pillow가 필요하다. 일반 배포 CI는 버전 관리된 파일을 사용하므로 캡처 의존성을 설치하지 않는다.

```sh
python3 tools/build_pages.py
node tools/capture_home_tour.cjs
python3 tools/encode_home_tour.py
python3 tools/build_pages.py
npm run test:pages
```

`PM_CHROME`으로 Chromium 실행 파일을 지정할 수 있다. 캡처는 별도 headless 브라우저의 빈 저장소에서 수행한다. 중간 PNG와 예시 다운로드는 `tmp/home-tour-frames/`에만 남으며 배포하지 않는다. 새 GIF의 강조 위치와 글자 가독성을 직접 확인하고 인코딩한 미디어를 함께 커밋한다. `learn.html?unit=0&view=practice&step=settlement&phase=evidence` 같은 링크는 저장된 읽기 위치와 관계없이 지정한 과업을 연다. 링크가 자료 시점을 자동으로 바꾸지는 않는다.

## 시각화 워크북

각 단원의 핵심 실습 한 곳에 있는 「근거·예제」에서 선택해 열거나 상단 「시각화 워크북」으로 `visual.html`을 연다. 본문 읽기에는 시각화를 끼워 넣지 않는다. 실습의 그림은 선택 전에는 불러오지 않고 닫으면 실행 문서를 제거한다. 같은 브라우저에서 교재·ERP와 같은 자료 시점을 사용한다. 원천자료 → 그림에서 관계 확인 → 조건 비교 → 문서에 반영 순서로 진행한다.

| 실습 | 입력과 동작 | 연결할 산출물 |
|---|---|---|
| 0단원 정산 흐름 | S05의 시각·순서를 읽어 흐름도 표시, 단계별 PM 질문과 실제 ERP 조회 연결 | G00 업무 파악 메모 |
| 1단원 헌장 검토·승인 | PM·실무 검토자·스폰서의 역할별 흐름, S0A부터 S16 회신 대조 | D01 초안·검토·승인 근거 |
| 3단원 일정 | S1부터 S06 활동·기간·관계를 읽어 네트워크 계산, C/D 기간과 D→E Lead/Lag 조작, 원안과 연습안 간트 비교 | D14 ES/EF/LS/LF·총여유·날짜 |
| 8단원 성과·변경 | S2부터 ERP performance 집계로 EVM 표시, S11 대안 비교, S3부터 S12 승인 대조 | D05 성과보고·D06 변경요청 |

일정은 S02의 월~금 교육 달력(공휴일 별도 적용 없음), FS 관계, 자원 가용성 제약을 계산하지 않는 CPM 실습이다. 기술 작업 완료와 종료 행정 완료를 구분한다. 음수 지연값은 Lead로 표시하며 부분 인도·검증·자원의 가능성 확인을 별도로 요구한다. 화면의 계산과 대안 선택은 학습용이며 ERP 원본, 승인 기준선, 학습자 문서를 변경하거나 승인하지 않는다.

조작값은 저장·제출하지 않는다. 「현재 그림·계산표 내려받기」는 현재 조건·그림·계산표와 근거를 포함한 단독 HTML 파일을 만든다. 오프라인에서 열거나 가로 방향으로 인쇄할 수 있다. 전체 문서 본문은 웹 표 작성 영역 또는 내려받은 양식에서 이어 작성한다. 추가로 2단원 요구사항 연결, 4단원 원가·현금, 5단원 리스크, 6단원 업체 평가, 7단원 실행 증거, 9단원 인수·이관 실습을 제공한다. 필요한 관계를 확인하는 보조 도구이며 모두 사용할 필요는 없다.

구현 원천은 `ERP/visual-workbook.html`, `.css`, `.mjs`와 `ERP/visual-model.mjs`다. 계산은 S06·S11 본문과 현재 SQLite 자료에서 도출한다. 입력 형식이 달라지면 오류를 표시하며 오래된 별도 수치를 사용하지 않는다. `npm run test:pages`는 일정 계산·여유 소진·주공정 변경·선행/지연·달력·EVM을 검증하고, 브라우저에서 시점 잠금·원천 불변·조작·HTML 내보내기·모바일·양식 링크를 확인한다.


## 2026-09-24 웹 통합 교재 개정

- 60절의 단원 본문은 `tools/unit_lessons_early.py`와 `tools/unit_lessons_late.py`에서, 69단계 심화 설명·확인 문제는 `tools/deep_lessons.py`에서 관리합니다. `tools/unit_reading.py`가 본문과 세 실습 화면, 단원별 선택 시각화 위치를 연결합니다. `reader_revision.py`가 웹 JSON, 교재·워크북 원고로 연결하며 `stage_materials.py`는 미래 단계 본문·확인문제를 제외합니다.
- `ERP/onboarding.js`는 단원 본문과 단계별 실습을 구분하고, 실습에서 한 번에 한 화면만 보여 줍니다. `ERP/study-workspace.js`는 확인 문제, 선택형 시각화와 웹 양식을 제공합니다. 초안은 페이지 메모리 안에만 있고 다운로드·불러오기로 보관합니다. 서버 제출·학생 추적은 없습니다.
- 시각화는 `visual-workbook.mjs`, `visual-motion.mjs`, `visual-extra.mjs`에서 제공하며 D3 7.9.0을 출처·해시·라이선스와 함께 로컬 배포합니다. 외부 CDN이 필요 없습니다.
- 전체 흐름: `python3 tools/rebuild.py --pdf --package`, `python3 tools/build_pages.py`, `npm run test:pages`. 신규 계산 검증과 브라우저 통합 검증은 기존 GitHub Action에서 함께 실행합니다.
- `pathway.html`은 Level 1 완료 조건과 후속 Level 2~4 목표를 설명합니다. 상세 파일럿·확장 규칙은 `00_설계/Level1_고도화_완료기준과_후속레벨.md`에 있습니다.
- 웹 통합 시각화는 GitHub Pages 배포본에 제공됩니다. Python ERP 배포팩은 원천 조회·교재·작성 양식 경로를 지원하며 내장 시각화는 공개 웹 교재에서 사용합니다.
