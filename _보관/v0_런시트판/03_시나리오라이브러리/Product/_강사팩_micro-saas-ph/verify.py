import math
FX=1380.0
# --- K-1 MRR
n_solo,n_st,n_sc=91,34,8; p=(19,49,99)
MRR=19*n_solo+49*n_st+99*n_sc; N=n_solo+n_st+n_sc
ARPA=MRR/N; ARR=MRR*12
# --- K-2 TAM
TAM=48000*0.30*ARPA*12
# --- K-3 Series A
REQ_ARR=4_400_000; REQ_MRR=REQ_ARR/12; REQ_ACC=REQ_ARR/(ARPA*12)
# --- K-5 GM
pad=MRR*0.62; mer=MRR*0.38
fee=pad*0.05+0.50*82+mer*0.15
GM=MRR-fee-515-2.10*N
# --- K-4 churn
base=[1652,2431,3286]; cmrr=[124,168,208]; clogo=[6,7,6]; blogo=[53,78,105]
c_rev=sum(cmrr)/sum(base); c_logo=sum(clogo)/sum(blogo)
coh=[31,30,28,24,23]; c_coh=1-(coh[4]/coh[0])**0.25
nc=[22,21,20,20,20]; c_nc=1-(nc[4]/nc[0])**0.25
# --- K-6 burn
feer=fee/MRR
rows=[("3월",0,120,0,0),("4월",0,150,0,0),("5월",973,310,31,0),("6월",1652,380,53,0),
      ("7월",2431,430,78,0),("8월",3286,470,105,1_800_000*8/31)]
cum=0; detail=[]
for m,mrr,op,acc,extra in rows:
    g=mrr-op-2.10*acc-mrr*feer; draw=4_400_000+extra; b=draw-g*FX; cum+=b
    detail.append((m,round(g,2),round(g*FX),round(draw),round(b)))
sep=(4_400_000+1_800_000)*13/30 - GM*FX*13/30
cum+=sep
CAPEX=4_800_000+3_200_000+6_400_000+7_800_000+1_800_000
REM=60_000_000-cum-CAPEX
burn_wo=4_400_000-GM*FX; burn_w=4_400_000+1_800_000-GM*FX
# --- K-7 channels
def cac(h,r,c): return h*r/c
# --- K-9 exit
def hourly(total,share,inv,hrs): return (total*share*FX-inv)/hrs
# --- K-10 10k
def months(c,nw,tgt,start=133):
    x=start
    for i in range(1,241):
        x=x*(1-c)+nw
        if x>=tgt: return i
TGT=10000/ARPA
# --- K-12 sample
def nreq(p1,p2,alpha=0.05,power=0.80):
    za=1.959963985; zb=0.8416212336; pb=(p1+p2)/2
    return math.ceil(((za*math.sqrt(2*pb*(1-pb))+zb*math.sqrt(p1*(1-p1)+p2*(1-p2)))/abs(p1-p2))**2)
out=[]
A=out.append
A(f"K-1  MRR = 19x91+49x34+99x8 = {MRR}  | ARPA = {MRR}/{N} = {ARPA:.4f} | ARR = {ARR}")
A(f"K-2  TAM(ARR) = 48000 x 0.30 x {ARPA:.4f} x 12 = {TAM:,.2f}")
A(f"K-3  reqMRR = 4,400,000/12 = {REQ_MRR:,.2f} = x{REQ_MRR/MRR:.2f} | reqACC = {REQ_ACC:,.0f} | /14400 = {REQ_ACC/14400*100:.2f}% | /TAM = {REQ_ARR/TAM*100:.2f}%")
A(f"     maintain: {REQ_ACC:,.0f} x {c_rev:.4f} = {REQ_ACC*c_rev:,.1f}/mo = x{REQ_ACC*c_rev/34:.1f} | cold cost {REQ_ACC*c_rev*381.92:,.0f} vs GM {REQ_MRR*0.7574:,.0f}")
A(f"K-4  churn: rev={c_rev*100:.3f}%  logo={c_logo*100:.3f}%  MayCohort={c_coh*100:.3f}%  nonCoupon={c_nc*100:.3f}%")
A(f"     churned avg ARPA = {sum(cmrr)}/{sum(clogo)} = {sum(cmrr)/sum(clogo):.2f} vs ARPA {ARPA:.2f}")
for c,l in ((c_rev,"rev"),(c_coh,"cohort"),(c_logo,"logo"),(c_nc,"nonCoupon")):
    A(f"     {l:9s} c={c*100:.2f}% LTV={ARPA*(GM/MRR)/c:8.2f} steady={34/c:7.1f} ceiling=${34/c*ARPA:,.0f} 12m-ret={(1-c)**12*100:.1f}%")
A(f"     GRR=(3286-208-60)/3286={(3286-208-60)/3286*100:.2f}%  NRR={(3286-208-60+154)/3286*100:.2f}%  NRR(+118)={(3286-208-60+154+118)/3286*100:.2f}%")
A(f"K-5  fee={fee:.3f} ({fee/MRR*100:.2f}%) GM={GM:.3f} ({GM/MRR*100:.2f}%) GM/acct={GM/N:.2f} GMkrw={GM*FX:,.0f}")
A(f"     GMkrw/4.4M={GM*FX/4_400_000*100:.2f}%  founder-cost annual = ({GM:.2f}-{4_400_000/FX:.2f})x12 = {(GM-4_400_000/FX)*12:,.2f}")
for nm,pp,cnt in (("Solo",19,91),("Studio",49,34),("Scale",99,8)):
    u=pp-pp*feer-2.10; A(f"     {nm:7s} unitGM={u:6.2f} -infra 3.87 -CS = net")
csq={"Solo":(128,91,19),"Studio":(46,34,49),"Scale":(13,8,99)}
tot_net=0
for k,(q,cn,pp) in csq.items():
    cs=q*14/60/cn*25.66; u=pp-pp*feer-2.10; net=u-515/N-cs; tot_net+=net*cn
    A(f"     {k:7s} inq/acct={q/cn:.3f} CS=${cs:.2f} unitGM=${u:.2f} net=${net:.2f} LTVnet=${net/c_rev:.2f} total=${net*cn:.2f}")
A(f"     net contrib total = ${tot_net:.2f} (check GM - CS 43.63h x 25.66 = ${GM-43.63*25.66:.2f}) | Solo share {91*2.75/tot_net*100:.1f}%")
A(f"     CS hours = 187 x 14/60 = {187*14/60:.2f} h/mo = {187*14/60/(51*4.345)*100:.1f}% of 서가온 capacity")
A("K-6  burn table:")
for d in detail: A(f"     {d[0]:8s} GM=${d[1]:9.2f} GMkrw={d[2]:>10,} draw={d[3]:>10,} burn={d[4]:>10,}")
A(f"     9월(13d) burn = {sep:,.0f}")
A(f"     cum operating burn = {cum:,.0f} | CAPEX = {CAPEX:,} | total = {cum+CAPEX:,.0f} | REMAINING = {REM:,.0f}")
A(f"     burn/mo excl Park = {burn_wo:,.0f} -> runway {REM/burn_wo:.2f} mo | incl Park = {burn_w:,.0f} -> runway {REM/burn_w:.2f} mo | ratio {burn_wo and burn_w/burn_wo:.2f}x")
A("K-7  channels:")
for nm,h,r,cnt in (("community",11,25.66,7),("cold-out",22,34.72,2),("SEO",26,25.66,0)):
    if cnt: A(f"     {nm:10s} cost=${h*r:.2f} CAC=${h*r/cnt:.2f} LTV/CAC={ARPA*(GM/MRR)/c_rev/(h*r/cnt):.2f}")
    else:   A(f"     {nm:10s} cost=${h*r:.2f} CAC=undefined (0 acquired)")
A("K-8  feature cards:")
cards=[20,11,8,10,9,68,24,31,44,27,22,34,12,52,41,14,29,26,18,33]
A(f"     20 cards total = {sum(cards)} 인시 | shipped F01-F13 = {sum(cards[:13])} | cut = {sum(cards)-sum(cards[:13])} ({(sum(cards)-sum(cards[:13]))/sum(cards)*100:.1f}%)")
A(f"     capacity = (62+51)x4 = {(62+51)*4} | dev budget 320 | non-dev {(62+51)*4-320}")
A(f"     F16 14h: cost=${14*34.72:.2f} lost LTV=3x${ARPA*(GM/MRR)/c_rev:.2f}=${3*ARPA*(GM/MRR)/c_rev:.2f} ratio {3*ARPA*(GM/MRR)/c_rev/(14*34.72):.2f}x | = {3*ARPA*(GM/MRR)/c_rev/GM*100:.1f}% of monthly GM")
A(f"     F14 52h: cost=${52*34.72:.2f} vs Scale net LTV ${(99-99*feer-2.10-515/N-13*14/60/8*25.66)/c_rev:.2f}")
A("K-9  exit hourly:")
for nm,share,inv,hrs,prev,prev2 in (("도이현",0.6,42_000_000,62*28,92_000_000,115_000_000),("서가온",0.4,18_000_000,51*28,68_000_000,None)):
    for tt in (150_000,105_000):
        hh=hourly(tt,share,inv,hrs); A(f"     {nm} @${tt:,}: recv={tt*share*FX:,.0f} gain={tt*share*FX-inv:,.0f} /{hrs}h = {hh:,.0f}/h vs prev {prev/12/160:,.0f} ({hh/(prev/12/160)*100:.1f}%)"+(f" vs {prev2/12/160:,.0f} ({hh/(prev2/12/160)*100:.1f}%)" if prev2 else ""))
A(f"     exit multiple: 150000/{ARR} = {150_000/ARR:.3f}x ARR / {150_000/MRR:.2f}x MRR")
A("     waterfall (1x non-part $2M, founders 70% of 80% residual = 0.875):")
for E in (150_000,2_000_000,5_000_000,10_000_000,20_000_000,50_000_000):
    inv=min(E,max(2_000_000,0.20*E)); A(f"       E=${E:>11,}: inv=${inv:>10,.0f} founders=${(E-inv)*0.875:>11,.0f} (bootstrap ${E:,})")
for Eb in (150_000,1_000_000,5_000_000):
    A(f"       break-even: bootstrap ${Eb:,} == seed ${Eb/0.875+2_000_000:,.0f} (x{(Eb/0.875+2_000_000)/Eb:.2f})")
A("K-10 $10,000 path:")
A(f"     target accounts = 10000/{ARPA:.4f} = {TGT:.2f}")
for c,l in ((c_nc,"2.36"),(c_rev,"6.78"),(c_logo,"8.05")):
    A(f"     churn {l}%: "+" | ".join(f"n={nw}: ceil {nw/c:.0f} / {months(c,nw,TGT)}mo" for nw in (34,40,45)))
rev=10000; f2=rev*0.0978; infra=780; cg=2.10*318; park=3_600_000/FX; mkt=645
dist=rev-f2-infra-cg-park-mkt
A(f"     at 10k: GM={rev-f2-infra-cg:.2f} ({(rev-f2-infra-cg)/rev*100:.2f}%) dist=${dist:.2f} = {dist*FX:,.0f}KRW = {dist*FX/(7_666_667+5_666_667)*100:.2f}% of combined prev salary")
A(f"       Do 60% {dist*FX*0.6:,.0f} ({dist*FX*0.6/7_666_667*100:.1f}%) | Seo 40% {dist*FX*0.4:,.0f} ({dist*FX*0.4/5_666_667*100:.1f}%)")
A("K-11 branch A/B:")
for nm,me,pa in (("baseline",0.38,0.62),("A appstore80",0.80,0.20),("B direct80",0.20,0.80)):
    ff=MRR*pa*0.05+0.50*round(MRR*pa/ARPA)+MRR*me*0.15; g=MRR-ff-515-2.10*N
    A(f"     {nm:14s} fee=${ff:7.2f} ({ff/MRR*100:5.2f}%) GM=${g:8.2f} /acct ${g/N:.2f} | appstore MRR ${MRR*me:.2f} ~{round(N*me)} acct")
A(f"     A-B GM gap = ${(MRR-(MRR*0.80*0.05+0.50*round(MRR*0.80/ARPA)+MRR*0.20*0.15)-515-2.10*N)-(MRR-(MRR*0.20*0.05+0.50*round(MRR*0.20/ARPA)+MRR*0.80*0.15)-515-2.10*N):.2f}/mo")
A("K-12 price experiment:")
nn=nreq(0.0369,0.0277); A(f"     n/arm={nn:,} total={2*nn:,} | traffic 1940/mo -> {2*nn/1940:.2f} mo = {2*nn/1940*4.345:.1f} wk")
A(f"     Solo $29: unitGM={29-29*feer-2.10:.2f} net={29-29*feer-2.10-515/N-8.42:.2f} (vs $19 net 2.75 = x{(29-29*feer-2.10-515/N-8.42)/2.75:.2f})")
A(f"     new Solo MRR: 24x19={24*19} -> 18x29={18*29} (+${18*29-24*19})")
A(f"     grandfather cost = 10x91x12 = ${10*91*12:,} /yr = ${10*91*12/12:.0f}/mo = {10*91*12/12/GM*100:.1f}% of monthly GM")
A("K-13 PH funnel & regulatory:")
A(f"     8400 -> 214 signup ({214/8400*100:.2f}%) -> 31 paid ({31/214*100:.2f}% / {31/8400*100:.3f}% of visits)")
A(f"     launch MRR 973 = {973/(4_400_000/FX)*100:.1f}% of founder draw (${4_400_000/FX:.2f})")
A(f"     decay: (176/1180)^(1/5) = {(176/1180)**0.2:.3f}; ratios "+", ".join(f"{b/a:.2f}" for a,b in zip([1180,640,410,288,214],[640,410,288,214,176])))
A(f"     fine cap 10%: ARR KRW {ARR*FX:,.0f} x 10% = {ARR*FX*0.10:,.0f} = {ARR*FX*0.10/REM*100:.1f}% of remaining capital")
A(f"     Gold requirement: appstore annual {MRR*0.38*12:,.2f} / 50000 = {MRR*0.38*12/50000*100:.1f}%")
A("K-14 asymmetry vs ONE ONDAM 428억 / P1 168억:")
A(f"     1.8M KRW / 42.8B = {1_800_000/42_800_000_000*100:.4f}% | CAPEX 24M / 16.8B = {24_000_000/16_800_000_000*100:.2f}% | 24M/60M = {24_000_000/60_000_000*100:.1f}%")
A(f"     payback rev-basis vs GM-basis multiple = 1/{GM/MRR:.4f} = {MRR/GM:.2f}x")
print("\n".join(out))
