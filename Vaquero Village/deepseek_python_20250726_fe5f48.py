import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# System parameters
ρ = 62.4                   # lbm/ft³
μ = 0.000017888            # lbf·s/ft²
g = 32.174                 # ft/s²
dia_SN = 2.5 / 12          # ft
dia_CN = 1.5 / 12          # ft
L_total = 5420             # ft (main trunk)
Δz = -10                   # ft (elevation change)

def calculate_pressure(Q_gpm, L_pipe, D_pipe):
    """Compute pressure drop using Darcy-Weisbach (laminar)"""
    Q = Q_gpm * (1/7.48052) / 60  # Convert GPM to ft³/s
    Re = (4 * ρ * Q) / (np.pi * μ * D_pipe)
    f = 64 / Re if Re > 0 else 0
    v = Q / (np.pi * (D_pipe/2)**2)
    hf = f * (L_pipe/D_pipe) * (v**2) / (2*g)
    ΔP = (ρ * g * (hf + Δz)) / 144  # Convert to psi
    return 60 + ΔP  # P_plant = 60 psi

# Test flow rates
flows = [2.5, 1.0, 0.5]  # GPM
results = []

for Q in flows:
    P_CN92 = calculate_pressure(Q, L_total, dia_SN)
    results.append({
        "Flow (GPM)": Q,
        "CN92 Pressure (psi)": P_CN92,
        "Time <35 psi (min)": "Never" if P_CN92 > 35 else "Immediate"
    })

df_results = pd.DataFrame(results)
print(df_results)