import csv, time, os
from epanettools import epanet2 as en

# ---- paths ----
INP = r"C:\EPANET\WT8\baseline_80CN_with_controls_clean.inp"   # <-- fixed
RPT = r"C:\EPANET\WT8\dummy.rpt"
BIN = r"C:\EPANET\WT8\dummy.bin"
OUTDIR = r"C:\EPANET\WT8"

# ---- scenarios (global demand multiplier) ----
SCENARIOS = [1.25, 1.0, 0.75, 0.5, 0.125]

# ---- only export these critical CNs (keeps CSVs compact) ----
CRITICAL_CNS = ["CN41","CN66","CN87","CN88","CN89","CN90","CN91","CN92"]

def write_matrix(path, header, times, mat, retries=3):
    for attempt in range(retries):
        try:
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Time_s"] + header)
                for t, row in zip(times, mat):
                    w.writerow([t] + row)
            return
        except PermissionError:
            if attempt == retries - 1: raise
            time.sleep(0.5)

# ---- open project once ----
if not os.path.exists(INP):
    raise FileNotFoundError(f"INP not found: {INP}")

en.ENopen(INP, RPT, BIN)

# timing: 1 hr duration, 3-min steps everywhere
en.ENsettimeparam(en.EN_DURATION,    3600)   # 1 hr
en.ENsettimeparam(en.EN_HYDSTEP,      180)   # 3 min
en.ENsettimeparam(en.EN_QUALSTEP,     180)   # 3 min
en.ENsettimeparam(en.EN_PATTERNSTEP,  180)   # 3 min
en.ENsettimeparam(en.EN_REPORTSTEP,   180)   # 3 min

# (optional but safe) prefer Darcy–Weisbach if available
try:
    en.ENsetoption(en.EN_HEADLOSS, en.EN_DW)
except Exception:
    try: en.ENsetoption(en.EN_HEADLOSS, 1)  # 0=HW,1=DW,2=CM in some builds
    except Exception: pass

# resolve node/link indices up front
nnodes = en.ENgetcount(en.EN_NODECOUNT)[1]
nlinks = en.ENgetcount(en.EN_LINKCOUNT)[1]
node_id_by_idx = {i: en.ENgetnodeid(i)[1] for i in range(1, nnodes+1)}
link_id_by_idx = {k: en.ENgetlinkid(k)[1] for k in range(1, nlinks+1)}

# indices for just the critical CNs (skip ones that might be absent)
crit_idx = []
crit_ids = []
for nid in CRITICAL_CNS:
    try:
        i = en.ENgetnodeindex(nid)[1]
        crit_idx.append(i); crit_ids.append(nid)
    except Exception:
        # silently skip IDs not present in this INP
        pass

# run each scenario by scaling global demand multiplier
for mult in SCENARIOS:
    # set global demand multiplier (does not change base demands in INP)
    try:
        en.ENsetoption(en.EN_DEMANDMULT, float(mult))
    except Exception:
        # fallback: nothing; INP demands will be unscaled
        pass

    # hydraulics loop
    en.ENopenH()
    en.ENinitH(0)

    times = []
    press = []     # pressures for critical CNs only
    head  = []
    dmd   = []
    flow  = []
    vel   = []
    stat  = []

    while True:
        t = en.ENrunH()[1]
        times.append(t)

        # nodes (critical only)
        p_row, h_row, d_row = [], [], []
        for i in crit_idx:
            p_row.append(en.ENgetnodevalue(i, en.EN_PRESSURE)[1])
            h_row.append(en.ENgetnodevalue(i, en.EN_HEAD)[1])
            d_row.append(en.ENgetnodevalue(i, en.EN_DEMAND)[1])
        press.append(p_row); head.append(h_row); dmd.append(d_row)

        # links (all)
        q_row, v_row, s_row = [], [], []
        for k in range(1, nlinks+1):
            q_row.append(en.ENgetlinkvalue(k, en.EN_FLOW)[1])
            v_row.append(en.ENgetlinkvalue(k, en.EN_VELOCITY)[1])
            s_row.append(en.ENgetlinkvalue(k, en.EN_STATUS)[1])
        flow.append(q_row); vel.append(v_row); stat.append(s_row)

        tstep = en.ENnextH()[1]
        if tstep <= 0: break

    en.ENcloseH()

    tag = f"x{str(mult).replace('.','p')}"  # e.g., x1p25
    # write compact node CSVs (critical CNs only)
    write_matrix(os.path.join(OUTDIR, f"ct_nodes_pressure_{tag}.csv"),  crit_ids,  times, press)
    write_matrix(os.path.join(OUTDIR, f"ct_nodes_head_{tag}.csv"),      crit_ids,  times, head)
    write_matrix(os.path.join(OUTDIR, f"ct_nodes_demand_{tag}.csv"),    crit_ids,  times, dmd)
    # write full link CSVs
    write_matrix(os.path.join(OUTDIR, f"ct_links_flow_{tag}.csv"),      list(link_id_by_idx.values()), times, flow)
    write_matrix(os.path.join(OUTDIR, f"ct_links_velocity_{tag}.csv"),  list(link_id_by_idx.values()), times, vel)
    write_matrix(os.path.join(OUTDIR, f"ct_links_status_{tag}.csv"),    list(link_id_by_idx.values()), times, stat)

en.ENclose()
print(f"Done. CSVs written to: {OUTDIR}")




