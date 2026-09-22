-- Q01: 현재 시점 확인
SELECT * FROM meta;
-- Q02: 대사 불일치와 근거
SELECT * FROM v_대사조회 WHERE 판정='불일치';
-- Q03: 단계별 프로젝트 실제원가
SELECT * FROM v_프로젝트원가;
-- Q04: 전표 차대변 검증 (정상이면 0행)
SELECT bukrs,belnr,gjahr,SUM(hsl) AS 차이 FROM acdoca GROUP BY bukrs,belnr,gjahr HAVING SUM(hsl)<>0;
-- Q05: 계약 이행. 발주·검수·지급을 합계로 더하지 않는다.
SELECT * FROM v_조달조회;
-- Q06: 승인된 기준선
SELECT * FROM v_예산조회;
-- Q07: 회사 결산 기준 계정잔액
SELECT a.saknr,SUM(a.hsl) AS 잔액 FROM acdoca a JOIN bkpf b USING(bukrs,belnr,gjahr) WHERE b.budat<='2026-09-30' GROUP BY a.saknr;
-- Q08: 원가와 진척을 비교한다. 특정 상태일로 한정한다.
SELECT SUM(pv) AS PV,SUM(ev) AS EV,SUM(ac) AS AC,1.0*SUM(ev)/NULLIF(SUM(ac),0) AS CPI,1.0*SUM(ev)/NULLIF(SUM(pv),0) AS SPI FROM performance WHERE status_date='2026-11-30';
-- Q09: 요구사항과 원천문서
SELECT * FROM v_요구추적;
-- Q10: 정산 집계
SELECT SUM(거래금액) AS 거래,SUM(취소금액) AS 취소,SUM(수수료) AS 수수료,SUM(조정금액) AS 조정,SUM(지급예정액) AS 지급 FROM v_정산조회;
