import os, traceback
from epanet import toolkit as tk

INP = r".\auto_built_clean.inp"
OUTDIR = r".\reports"
RPT = os.path.join(OUTDIR, "runner.rpt")
OUT = os.path.join(OUTDIR, "runner.out")

os.makedirs(OUTDIR, exist_ok=True)

def write_err(msg: str):
    with open(os.path.join(OUTDIR, "_smoketest_error.txt"), "w", encoding="utf-8") as f:
        f.write(msg)

try:
    ph = tk.createproject()
    try:
        tk.open(ph, INP, RPT, OUT)
        tk.resetreport(ph)
        tk.setreport(ph, "STATUS YES")   # <- plain string (NO b"...")
        tk.solveH(ph)
        tk.report(ph)
    finally:
        tk.close(ph)
        tk.deleteproject(ph)
    print("Smoketest complete. See reports/runner.rpt")
except Exception:
    write_err("OPEN/RUN FAILED:\n" + traceback.format_exc())
    print("Smoketest failed. See reports/_smoketest_error.txt")
