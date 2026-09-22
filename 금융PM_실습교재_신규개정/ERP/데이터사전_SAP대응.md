# 모의 ERP 데이터 사전

SAP S/4HANA의 업무 연결을 참고한 SQLite 교육용 모델이다. SAP 호환 DB나 실제 고객사의 추출본이 아니다. SAP에는 더 많은 키·필드·확장구조가 있으며 여기서는 단일회사·원화·원장0L로 축소한다.

| 업무 | 교육 테이블 | SAP 참고 개념 | 핵심 연결 |
|---|---|---|---|
| 회사·원가센터 | company,cost_center | 회사코드 BUKRS,원가센터 KOSTL | 회사→원가센터 |
| 거래처 | business_partner | Business Partner | 계약·가맹점→거래처 |
| 프로젝트·WBS | project,wbs | PSPID,POSID | MP-01→1.1~1.7 |
| 회계전표 | bkpf,acdoca | BKPF헤더,ACDOCA통합분개장 | BUKRS+BELNR+GJAHR,항목DOCLN+원장RLDNR |
| 구매 | purchase_request,purchase_order | 구매요청·발주 EBELN | 요청→계약→발주 |
| 용역검수·청구·지급 | service_acceptance,invoice,payment | 검수·송장·지급 업무 | 발주→검수→청구→지급→전표 |
| 예산·승인 | baseline,budget_line,approval | 프로젝트예산·버전 개념 | BL01/BL02→AP01/AP02 |
| 금융원천 | merchant,payment_transaction,settlement_batch,exception_case | 별도 업무시스템 | 가맹점→배치→거래→대사예외 |
| 문서 | source_document,document_link | 문서관리·증빙 연결 개념 | 문서→프로젝트·전표 |

## 금액과 키
hsl은 원 단위 부호 있는 정수다. 양수 차변·음수 대변이며 각 전표 합계0. SAP HSL 전체 의미를 구현한 것이 아니다. 계정610000만 프로젝트원가로 집계한다. 지급계정100000과 비용610000을 합산하지 않는다. 조회뷰는 원천을 복제 저장하지 않으며 JOIN으로 제공한다. BSEG는 이번 모형에서 별도 구현하지 않는다.

가맹점 수수료는 (거래-취소)×200/10,000을 원단위 절사한다. 배치지급액은 거래별 지급예정액 합계+배치조정이다. 수신액과 계산액이100원 다른12건은 이미 사유가 확인된 정상적인 대사연습 대상이며 자료 누락이 아니다. 24가맹점·480거래는 전체240가맹점의 교육표본이다.

## 시점
S0 착수전: 인물·회사재무·업무요구·거래표본. S1 계획검토: 추정·WBS·위험·제안자료 추가. S2 실행: AP01·BL01·계약·중간실적·CR01. S3 변경후: AP02·BL02·R06. S4 종료: 최종검수·지급·테스트. S0 SQL에는 BL02도 미래 문서도 존재하지 않는다.

## 필드 전체 정의
schema.sql이 실행 가능한 필드·기본키·외래키 사전이다. 화면의 ‘데이터 사전’에서도 현재 스냅샷 정의를 볼 수 있다. source_document의 확인자는 입력 사실의 확인자이며 학습자 산출물의 대리 승인자가 아니다. person의 권한과 S02를 함께 확인한다.

## 금융 표본과 회계의 연결

settlement_revenue_bridge는 표본배치의 수수료가 REV집계전표에 포함되는 관계를 기록한다. 표본수수료를REV매출에다시더하지않는다. 가맹점원금·조정금은 프로젝트원가가 아니다. QA환경같은물적자원은 physical_resource에서 별도로조회하며 인력 갈등 관리와 구분한다.
