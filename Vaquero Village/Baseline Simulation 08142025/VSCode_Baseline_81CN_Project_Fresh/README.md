# VS Code One‑Click Project — Baseline 81 CN (Single‑Pressure Model)

- 81 active CNs; scenarios: 1.25, 1.00, 0.75, 0.50, 0.125 GPM/CN
- 640‑gal pressure‑tank drawdown; booster = 20 GPM @ 38 psi; stop > 38 psi
- Δt = 2.5 min; horizon = 120 min
- Outputs: CSV per scenario + combined chart

## Run
1) Open in VS Code, press **F5** (Run ▶ Run Baseline 81 CN), or
2) Terminal:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # (Windows)  |  source .venv/bin/activate  # (macOS/Linux)
   pip install -r requirements.txt
   python run_baseline_81CN.py
   ```
