
import math, os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Set

TOTAL_CNS_DEFINED=92
REMOVED_CNS:Set[int]={41,89,91,92}
NO_FLOW_CNS:Set[int]={1,2,3,4,66,88,90}
ACTIVE_CN_NUMS:List[int]=sorted(set(range(1,TOTAL_CNS_DEFINED+1))-REMOVED_CNS-NO_FLOW_CNS)
assert len(ACTIVE_CN_NUMS)==81

RHO=62.4; G=32.174; PSF_PER_PSI=144.0; MU=1.1e-5; EPS=5e-6
D=2.469/12.0; DT=2.5; T=120.0
SCENARIOS=[1.25,1.0,0.75,0.5,0.125]; FOCUS=["CN40","CN70","CN81","CN86"]
CUT1,CUT2,COUT=45.0,40.0,60.0
PTANK=1280.0; S_MAX=5800.0; S_ON=5000.0; WELL_GPM=20.0

@dataclass
class Node: id:str; x:float; y:float; elev:float; is_cn:bool=False
@dataclass
class Edge: frm:str; to:str; L:float; D:float; Q_cfs:float=0.0

def psi_to_head(p): return (p*PSF_PER_PSI)/(RHO*G)
def head_to_psi(h): return (h*RHO*G)/PSF_PER_PSI

def build():
    nodes:Dict[str,Node]={}; edges:List[Edge]=[]
    def elev(x): return x*(10.0/1000.0)
    nodes["P"]=Node("P",0.0,0.0,0.0,False)
    sn_pos={}; xvals=list(range(600,10601,600))
    for i,x in enumerate(xvals,1):
        sn=f"SN{i}"; nodes[sn]=Node(sn,float(x),0.0,elev(float(x)),False); sn_pos[sn]=x
        prev="P" if i==1 else f"SN{i-1}"; prev_x=0.0 if prev=="P" else sn_pos[prev]
        edges.append(Edge(prev,sn,float(x-prev_x),D))
    def near(tx): return min(sn_pos.keys(), key=lambda k: abs(sn_pos[k]-tx))
    alias={"SN41":near(5000.0),"SN71":near(7100.0),"SN89":near(8900.0),"SN91":near(9500.0)}
    edges.append(Edge(alias["SN41"],alias["SN91"],450.0,D))
    edges.append(Edge(alias["SN89"],alias["SN71"],100.0,D))
    for num,name in {40:"SN41",70:"SN71",81:"SN91",86:"SN89"}.items():
        base=alias[name]; x=nodes[base].x+12.0; nid=f"CN{num}"
        nodes[nid]=Node(nid,x,0.0,elev(x),True); edges.append(Edge(base,nid,float(x-nodes[base].x),D))
    made={40,70,81,86}
    rng=np.random.default_rng(41)
    for n in range(1,TOTAL_CNS_DEFINED+1):
        if n in REMOVED_CNS or n in made: continue
        sn=f"SN{int(rng.integers(1,len(sn_pos)+1))}"; x=nodes[sn].x+float(rng.uniform(10,20))
        nid=f"CN{n}"; nodes[nid]=Node(nid,x,0.0,elev(x),True); edges.append(Edge(sn,nid,float(x-nodes[sn].x),D))
    return nodes,edges

def assemble(nodes,edges):
    ids=list(nodes.keys()); idx={nid:i for i,nid in enumerate(ids)}
    A=np.zeros((len(edges),len(nodes)))
    for k,e in enumerate(edges): A[k,idx[e.frm]]=1.0; A[k,idx[e.to]]=-1.0
    return A,idx,ids

def solve(nodes,edges,plant_head,dem,iters=6):
    A,idx,ids=assemble(nodes,edges); pidx=ids.index("P"); g2c=1/448.831
    Ddem=np.zeros(len(ids))
    for nid,q in dem.items():
        if nid in idx: Ddem[idx[nid]]=q*g2c
    H=np.array([nodes[n].elev+(plant_head if n=='P' else 0.0) for n in ids],float)
    ei=np.array([idx[e.frm] for e in edges]); ej=np.array([idx[e.to] for e in edges])
    L=np.array([e.L for e in edges],float); Darr=np.array([e.D for e in edges],float); Asec=np.pi*(Darr**2)/4.0
    Qlast=np.zeros(len(edges))
    for _ in range(iters):
        dH=H[ei]-H[ej]; v=Qlast/np.maximum(Asec,1e-12); Re=np.abs((RHO*v*Darr)/MU)
        f=np.where(Re<2000.0, 64.0/np.maximum(Re,1e-6), 0.25/(np.log10((EPS/(3.7*Darr))+(5.74/(np.power(Re,0.9))))**2))
        r=f*(L/Darr)*(1/(2*G))*np.power(1/np.maximum(Asec,1e-12),2.0)
        Q=np.sign(dH)*np.sqrt(np.maximum(np.abs(dH),1e-12)/np.maximum(r,1e-12))
        dQd=0.5/np.sqrt(np.maximum(np.abs(dH),1e-12)*np.maximum(r,1e-12))
        Rn=A.T@Q - Ddem; Rn[pidx]=0.0; W=np.diag(dQd); J=A.T@W@A
        J[pidx,:]=0.0; J[:,pidx]=0.0; J[pidx,pidx]=1.0
        rhs=-Rn.copy(); rhs[pidx]=(nodes['P'].elev+plant_head)-H[pidx]
        try: dHn=np.linalg.solve(J,rhs)
        except np.linalg.LinAlgError: break
        H+=dHn; Qlast=Q
        if np.linalg.norm(dHn,np.inf)<5e-4: break
    for k,e in enumerate(edges): e.Q_cfs=Qlast[k]
    return {nid:H[i] for i,nid in enumerate(ids)}

def run_folder(out_dir, gpm_per_cn):
    nodes,edges=build()
    active=[f"CN{n}" for n in sorted(set(range(1,TOTAL_CNS_DEFINED+1))-REMOVED_CNS-NO_FLOW_CNS) if f"CN{n}" in nodes]
    ppsi=60.0; phead=psi_to_head(ppsi); pt=PTANK; S=S_MAX; p1=False; p2=False; well=False
    demand=len(active)*gpm_per_cn
    ts=[]; cn=[]; pf=[]
    t=0.0
    while t<=T+1e-9:
        if ppsi<=CUT2: p1=True; p2=True
        elif ppsi<=CUT1: p1=True; p2=False
        elif ppsi>=COUT: p1=False; p2=False
        boost=(20.0 if p1 else 0.0)+(20.0 if p2 else 0.0)
        if ppsi>=60: pt_av=pt
        elif ppsi<=38: pt_av=0.0
        else:
            frac=(ppsi-38)/(60-38); pt_av=pt*max(min(frac,1.0),0.0)
        if S<S_ON: well=True
        if S>=S_MAX: well=False
        wgpm=WELL_GPM if well else 0.0
        dem={nid:0.0 for nid in nodes}
        for nid in active: dem[nid]=gpm_per_cn
        for n in NO_FLOW_CNS:
            nid=f"CN{n}"
            if nid in nodes: dem[nid]=0.0
        H=solve(nodes,edges,phead,dem,iters=6)
        deficit=max(demand - boost, 0.0)
        draw_pt=min(deficit*DT, max(pt if ppsi>=60 else pt_av,0.0)); pt=max(pt - draw_pt, 0.0)
        rem=max(deficit - draw_pt/DT, 0.0); draw_S=min(rem*DT, S); S=S - draw_S + wgpm*DT
        phead=H["P"]; ppsi=head_to_psi(phead)
        ts.append({"Time_min":round(t,2),"Plant_Pressure_psi":round(ppsi,2),"Pump1_on":int(p1),"Pump2_on":int(p2),
                   "Booster_Flow_GPM":boost,"Total_Demand_GPM":demand,"PTank_Rem_gal":round(pt,1),"Storage_gal":round(S,1),"Well_on":int(well)})
        for nid in [n for n in nodes if n.startswith("CN")]:
            cn.append({"Time_min":round(t,2),"CN":nid,"Pressure_psi":round(head_to_psi(H[nid]),3)})
        for e in edges:
            Asec=math.pi*(e.D**2)/4.0; vel=e.Q_cfs/max(Asec,1e-12)
            pf.append({"Time_min":round(t,2),"From":e.frm,"To":e.to,"Length_ft":e.L,"Q_cfs":e.Q_cfs,"Q_gpm":e.Q_cfs*448.831,"Velocity_ft_s":vel})
        t+=DT
    os.makedirs(out_dir, exist_ok=True)
    pd.DataFrame(ts).to_csv(os.path.join(out_dir,"TimeSeries.csv"), index=False)
    pd.DataFrame(cn).to_csv(os.path.join(out_dir,"NodePressures.csv"), index=False)
    pd.DataFrame(pf).to_csv(os.path.join(out_dir,"PipeFlows.csv"), index=False)
    plt.figure(figsize=(10,5)); df=pd.DataFrame(ts); plt.plot(df["Time_min"], df["Plant_Pressure_psi"])
    for y,ls in [(20.0,"--"),(60.0,":"),(45.0,":"),(40.0,":")]: plt.axhline(y, linestyle=ls, alpha=0.6)
    plt.title(f"Plant Pressure – {gpm_per_cn:.3f} GPM per CN (81 active CNs)"); plt.xlabel("Time (min)"); plt.ylabel("Pressure (psi)"); plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(out_dir,"PlantPressure.png"), dpi=160, bbox_inches="tight"); plt.close()
    plt.figure(figsize=(10,5))
    cn_df=pd.DataFrame(cn)
    for c in FOCUS:
        if c in set(cn_df["CN"]):
            sub=cn_df[cn_df["CN"]==c]; plt.plot(sub["Time_min"], sub["Pressure_psi"], label=c)
    plt.title(f"Focused CN Pressures – {gpm_per_cn:.3f} GPM per CN"); plt.xlabel("Time (min)"); plt.ylabel("Pressure at CN (psi)"); plt.grid(True, alpha=0.3); plt.legend()
    plt.savefig(os.path.join(out_dir,"FocusCNs.png"), dpi=160, bbox_inches="tight"); plt.close()

def main():
    base=os.getcwd()
    for s in SCENARIOS:
        run_folder(os.path.join(base, f"Scenario_{s:.3f}_GPM_81CN"), s)
    plt.figure(figsize=(12,6))
    for s in SCENARIOS:
        ts=os.path.join(base, f"Scenario_{s:.3f}_GPM_81CN","TimeSeries.csv")
        if os.path.exists(ts):
            df=pd.read_csv(ts); plt.plot(df["Time_min"], df["Plant_Pressure_psi"], label=f"{s:.3f} GPM/CN")
    plt.axhline(20.0, linestyle="--"); plt.title("Combined Plant Pressure – All Scenarios (81 active CNs)")
    plt.xlabel("Time (min)"); plt.ylabel("Pressure (psi)"); plt.grid(True, alpha=0.3); plt.legend()
    plt.savefig(os.path.join(base,"Combined_Plant_Pressure_All_Scenarios_81CN.png"), dpi=180, bbox_inches="tight"); plt.close()

if __name__=="__main__":
    main()
