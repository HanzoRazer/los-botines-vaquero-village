# VS Code One‑Click Project — 81 CN Water System Simulation (Pinned)
Press F5 in VS Code to run the full 120‑minute, five‑scenario simulation.

## Equipment & Operating Parameters
- 2.5" Sch‑40 PVC (ID 2.469 in), ε=5e‑6 ft; ρ=62.4 lb/ft³; μ=1.1e‑5 lb·s/ft²
- Elevation: +10 ft per 1000 ft (W→E); N–S = 0; Plant datum = 0 ft
- Loops: SN41↔SN91 (450 ft), SN89↔SN71 (100 ft); SN92 removed
- Active demand CNs = 81; Removed demand CNs: CN41, CN89, CN91, CN92; No‑Flow CNs: CN1, CN2, CN3, CN4, CN66, CN88, CN90
- Scenarios (GPM/CN): 1.25, 1.0, 0.75, 0.5, 0.125
- Boosters: two × 20 GPM; cut‑in 45/40 psi; cut‑out 60 psi
- Pressure tanks: 1,280 gal usable (linear 60→38 psi); Storage: 5,800 gal; Well: 20 GPM when storage < 5,000 gal
- Δt=2.5 min; horizon=120 min; Darcy–Weisbach (Swamee–Jain); nodal continuity solve each step
