# GitHub Pages 운영 안내

공개 주소: https://voidmain443.github.io/git-github_for_PM_Tutorial_docs/

학생은 시작 화면 → 0단원 → 단계별 원천자료·ERP 조회 → 문서 양식 순서로 진행한다. 로그인과 Python 설치가 필요 없다. 기존 교재·ERP의 사실과 시점은 동일하다.

## 공개 범위와 동작

- 첫 화면: 처음 읽을 순서, 10개 단원, 초안·검토·승인의 구분.
- 교재: 69개 읽기 단계와 49개 프로세스. 각 단원의 시작 자료와 결과 안내.
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
