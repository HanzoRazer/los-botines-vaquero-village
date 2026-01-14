
import math, csv, os
from dataclasses import dataclass, asdict

NUM_CNS = 81
SCENARIOS_GPM_CN = [1.25, 1.00, 0.75, 0.50, 0.125]

P_CUT_OUT = 60.0
P_CUT_IN  = 38.0
P_FAIL    = 20.0

BOOSTER_GPM = 20.0
DRAW_TOTAL_GAL = 640.0

DT_MIN   = 2.5
T_MAX_MIN= 120.0

DRAW_60_TO_38_GAL = DRAW_TOTAL_GAL * ((P_CUT_OUT - P_CUT_IN) / (P_CUT_OUT - P_FAIL))
DRAW_38_TO_20_GAL = DRAW_TOTAL_GAL - DRAW_60_TO_38_GAL

@dataclass
class Row:
    Time_min: float
    Pressure_psi: float
    Total_Demand_GPM: float
    Booster_On: int
    Booster_Flow_GPM: float
    Tank_Rem_gal_60to38: float
    Tank_Rem_gal_38to20: float

def run_scenario(flow_per_cn: float, out_csv: str):
    total_demand = NUM_CNS * flow_per_cn
    t = 0.0; p = P_CUT_OUT
    tank_60_38 = DRAW_60_TO_38_GAL
    tank_38_20 = DRAW_38_TO_20_GAL
    rows = []
    while t <= T_MAX_MIN + 1e-9 and p > P_FAIL + 1e-9:
        booster_on = int(p <= P_CUT_IN + 1e-9)
        booster_flow = BOOSTER_GPM if booster_on else 0.0
        if p > P_CUT_IN + 1e-9:
            need_gal = total_demand * DT_MIN
            draw = min(need_gal, tank_60_38)
            tank_60_38 -= draw
            frac_used = (DRAW_60_TO_38_GAL - tank_60_38) / DRAW_60_TO_38_GAL if DRAW_60_TO_38_GAL>0 else 1.0
            p = max(P_CUT_OUT - frac_used*(P_CUT_OUT - P_CUT_IN), P_CUT_IN)
        else:
            deficit_gpm = max(total_demand - booster_flow, 0.0)
            need_gal = deficit_gpm * DT_MIN
            draw = min(need_gal, tank_38_20)
            tank_38_20 -= draw
            frac_used = (DRAW_38_TO_20_GAL - tank_38_20) / DRAW_38_TO_20_GAL if DRAW_38_TO_20_GAL>0 else 1.0
            p = max(P_CUT_IN - frac_used*(P_CUT_IN - P_FAIL), P_FAIL)
        rows.append(Row(round(t,2), round(p,3), round(total_demand,3), booster_on, round(booster_flow,3), round(tank_60_38,3), round(tank_38_20,3)))
        t += DT_MIN
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "Time_min","Pressure_psi","Total_Demand_GPM","Booster_On","Booster_Flow_GPM",
            "Tank_Rem_gal_60to38","Tank_Rem_gal_38to20"
        ])
        w.writeheader()
        for r in rows: w.writerow(asdict(r))
    return rows

def main():
    png_series = []
    for scenario in SCENARIOS_GPM_CN:
        out_csv = f"Scenario_{scenario:.3f}_GPM_per_CN_81CN.csv"
        rows = run_scenario(scenario, out_csv)
        times = [r.Time_min for r in rows]; press = [r.Pressure_psi for r in rows]
        png_series.append((f"{scenario:.3f}_GPM_per_CN", times, press))
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,6))
    for label, times, press in png_series:
        plt.plot(times, press, label=label, linewidth=2)
    plt.axhline(20.0, color="orange", linestyle="--", linewidth=2, label="Failure Threshold (20 psi)")
    plt.title("Combined Pressure Decay – Baseline 81 CNs\n(1 booster @20 GPM, 640-gal drawdown, dt=2.5 min)")
    plt.xlabel("Time (min)"); plt.ylabel("System Pressure (psi)"); plt.grid(True, alpha=0.3)
    plt.legend(); plt.savefig("Combined_Pressure_Chart_81CN_Baseline.png", dpi=180, bbox_inches="tight"); plt.close()
if __name__ == "__main__":
    main()
