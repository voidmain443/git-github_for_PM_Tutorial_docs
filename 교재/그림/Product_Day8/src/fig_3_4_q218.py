# -*- coding: utf-8 -*-
"""그림 3-4. 218문항 3범주"""
from mplcommon import *
from day8_enterprise import Q218
fig, ax = plt.subplots(figsize=(7.8, 3.3))
left=0; cols=[TEAL,NAVY,RUST]; short=["즉시 답변 가능","조건부","불가"]
descs=["조직·정책·접근통제·감사 로그\n전송 암호화·개인정보·사고 이력(제218)","침투 테스트·SBOM\n키 관리·복구 훈련·SSDLC","ISMS-P·ISO 27001·SOC 2\n인증서 · DR 센터 · 24/7 SOC"]
for (name,n,cat,ev),c,sh,de in zip(Q218,cols,short,descs):
    ax.barh(0,n,left=left,color=c,height=0.5,zorder=2); ax.text(left+n/2,0,f"{sh}\n{n}",ha="center",va="center",color="white",fontsize=8.5,fontweight="bold")
    xx=left+n/2 if sh!="불가" else 222; ha="center" if sh!="불가" else "left"
    ax.text(xx,-0.42,de,ha=ha,va="top",fontsize=7.2,color=c); left+=n
ax.annotate("제218문항 — 사고 RCA·재발 방지 증빙\n= ㉞ v1.1 전문 + 6건 증빙 + 6개월 리포트\n(요약이 아니라 전문 — 숨긴 것이 실사에서 나온다)",xy=(131,0.25),xytext=(110,1.0),fontsize=8,color=TEAL,arrowprops=dict(arrowstyle="->",color=TEAL,lw=0.9))
ax.text(131+31,0.5,"모의해킹 1,800만 · 4주",ha="center",fontsize=7.6,color=NAVY)
ax.text(222,0.5,"ISMS-P 2029-Q4 획득 계획\n인프라·DR은 온담 통제(온프렘)",ha="left",fontsize=7.6,color=RUST)
ax.set_xlim(0,300); ax.set_ylim(-1.05,1.4); ax.set_yticks([]); ax.set_xlabel("문항 수 (계 218 · 회신 5영업일 · ISMS-P 미인증)")
ax.set_title("218문항 — 받는 쪽의 SAC: 즉시 131 / 조건부 62 / 불가 25", fontsize=10.5, loc="left")
fig.subplots_adjust(bottom=0.2)
save(fig,"fig_3_4_q218","E-12 · §4.10 · ㊲ 항목 6 [추가 설정]")
