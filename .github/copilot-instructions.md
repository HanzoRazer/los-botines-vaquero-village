# Copilot Instructions: Los Botines Vaquero Village Water System

## Project Purpose
EPANET hydraulic simulation for Los Botines Vaquero Village water distribution network to resolve TCEQ regulatory sanctions and achieve compliance. The system models ~80+ connection nodes (CNs) with demand scenarios from 0.14 to 1.25 GPM per connection.

## Architecture Overview

```
CSV Data Sources                   Build Pipeline                  Simulation & Analysis
─────────────────                 ──────────────                  ─────────────────────
nodes.csv (nodes_ready.csv)  ──┐
                               ├──► build_inp_from_csv.py ──► auto_built.inp ──► epanet_runner_plus.py
Master_Edge_Test_Sheet.csv ────┘                                    │
(edges.csv)                                                         ▼
                                                              Pressure/Flow CSVs
                                                                    │
                                                                    ▼
                                                          epanet_chart_helper.py ──► Compliance Charts
```

## Critical CSV Header Requirements

**DO NOT modify header order or case.** Scripts exit immediately on mismatch.

```csv
# nodes.csv (10 columns, exact order)
NodeID,Type,Elevation_ft,BaseDemand_gpm,Pattern,X,Y,InitLevel_ft,MinLevel_ft,MaxLevel_ft

# edges.csv (9 columns, exact order)  
LinkID,LinkType,Node1,Node2,Length_ft,Diameter_in,Roughness,Coefficient,Status
```

## Key Scripts and Their Roles

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `build_inp_from_csv.py` | Builds EPANET model | `nodes.csv`, `edges.csv` | `auto_built.inp` |
| `epanet_runner_plus.py` | Runs batch simulations | `.inp` file | Pressure/flow CSVs |
| `epanet_interface.py` | Python API wrapper | `.inp` file | Analysis objects |
| `validate_master_edge.py` | Validates edge topology | `Master_Edge_Test_Sheet.csv` | Validation report |
| `reconcile_nodes_ready.py` | Cleans/validates nodes | Raw node data | `nodes_ready.csv` |
| `epanet_chart_helper.py` | Generates compliance charts | EPANET time series | PNG/PDF charts |

## Data Handling Rules (Enforced by Code)

1. **Zero-length pipes**: Blank or `0` in `Length_ft` → auto-set to `1.0 ft` (EPANET requirement)
2. **Missing patterns**: Blank junction `Pattern` → defaults to `"StressTest"` (constant 1.0 multiplier)
3. **Numeric parsing**: Use `to_float(val, default)` / `to_int(val, default)` helpers for tolerant parsing
4. **Valid LinkTypes**: Only `Pipe`, `Valve`, `Pump` - script flags others as invalid

## Compliance Thresholds

```python
COMPLIANCE_THRESHOLD = 20.0  # psi minimum (TCEQ requirement)
OPERATING_MIN = 38.0         # psi target minimum
OPERATING_MAX = 60.0         # psi target maximum
```

## Standard Workflows

### Run a Full Simulation
```powershell
cd "C:\Users\thepr\Downloads\los-botines-vaquero-village"

# 1. Validate data (optional but recommended)
python reconcile_nodes_ready.py
python validate_master_edge.py

# 2. Build EPANET input
python build_inp_from_csv.py

# 3. Run simulation
python epanet_runner_plus.py

# 4. Generate charts from results
python "files (4)\epanet_chart_helper.py" results.xlsx --scenario "Baseline 0.6 GPM"
```

### Python API Usage
```python
from epanet_interface import EPANETInterface

epanet = EPANETInterface("auto_built.inp")
epanet.run_simulation(duration=86400)  # 24 hours
compliance = epanet.check_pressure_compliance(min_pressure=20.0)
epanet.generate_compliance_report(output_file="report.txt")
```

## Demand Scenarios

Standard test scenarios (GPM per connection node):
- `0.14 GPM` - Minimal occupancy
- `0.60 GPM` - TCEQ minimum standard
- `0.75 GPM` - RV park modified
- `1.00 GPM` - Normal residential
- `1.25 GPM` - Stress test / peak demand

## File Naming Conventions

- **INP files**: `Baseline_FIXED_{SCENARIO}_{RATE}_GPM.inp`
- **Reports**: `Baseline_FIXED_{SCENARIO}_{RATE}_GPM.rpt`
- **Pressure CSVs**: `ct_nodes_pressure_x{multiplier}.csv`
- **Flow CSVs**: `ct_links_flow_x{multiplier}.csv`

## Project Structure

```
├── .github/copilot-instructions.md  # This file
├── nodes.csv, edges.csv             # Canonical data (build input)
├── Master_Edge_Test_Sheet.csv       # Topology source (valve→tee→trunk patterns)
├── build_inp_from_csv.py            # INP generator
├── epanet_interface.py              # Python WNTR wrapper
├── epanet_runner_plus.py            # Batch simulation runner
├── files (4)/                       # Simulation outputs and charts
│   ├── *.inp, *.rpt                 # EPANET models and reports
│   └── epanet_chart_helper.py       # Chart generator
├── examples/                        # Usage examples
├── Check Point 092425/              # Historical snapshots
└── Vaquero Village/                 # Legacy/reference data
```

## Dependencies

```
wntr>=1.0.0      # Water Network Tool for Resilience
numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.3.0
```

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `headers mismatch` | CSV column order wrong | Match exact header order from script constants |
| `blank NodeID` | Empty row in nodes.csv | Remove or fill blank NodeID rows |
| `node not found` | Edge references missing node | Ensure all Node1/Node2 values exist in nodes.csv |
| Negative pressure (-999) | Disconnected node | Check edge connectivity in topology |

## Key Reference Files

- `BASELINE_GUIDE.md` - Step-by-step simulation walkthrough
- `EPANET_GUIDE.md` - Full API documentation
- `IND.md` - Project index and file reference
