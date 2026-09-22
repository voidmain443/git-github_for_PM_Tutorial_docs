# 실행 환경

공개 GitHub Pages 사이트는 설치 없이 브라우저에서 사용할 수 있습니다. 로컬 학생 배포팩은 Python 3.10 이상에서 다음 명령으로 엽니다.

```sh
python3 ERP/server.py --stage S0 --port 8878
```

Windows에서는 python3 대신 py -3을 사용할 수 있습니다. 주소는 http://127.0.0.1:8878/learn?unit=0 입니다. 로컬 ERP는 Python 표준 라이브러리만 사용합니다.

제작·배포용 PDF에는 requirements-pages.txt와 NanumGothic 한글 글꼴이 필요합니다. 글꼴 위치는 PM_KOREAN_FONT로 지정할 수 있습니다. GitHub Actions는 필요한 글꼴과 라이브러리를 설치합니다. 웹 배포의 제작·검증 절차는 README_GitHub_Pages.md를 확인하세요.
