# epanet_run_once.py
import os, sys
from epanet import toolkit as tk

INP = sys.argv[1] if len(sys.argv)>1 else r".\auto_built_clean.inp"
OUTDIR = r".\reports"
RPT = os.path.join(OUTDIR, "runner_r1.rpt")
OUT = os.path.join(OUTDIR, "runner_r1.out")
os.makedirs(OUTDIR, exist_ok=True)

ph = tk.createproject()
try:
    tk.open(ph, INP, RPT, OUT)
    # standard hydraulic loop
    tk.openH(ph)
    tk.initH(ph, 0)
    t = 0.0
    while True:
        t = tk.runH(ph)    # may throw Error 110 here if network is still inconsistent
        tk.nextH(ph)
        if t <= 0.0:
            break
    tk.closeH(ph)
    tk.report(ph)
    print("Hydraulics solved. See", RPT)
finally:
    tk.close(ph)
    tk.deleteproject(ph)
