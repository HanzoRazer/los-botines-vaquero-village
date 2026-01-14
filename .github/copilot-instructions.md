# Los Botines Vaquero Village - Water System Simulation

## Project Purpose
EPANET hydraulic simulation for an 80-connection water distribution network to verify **20 psi minimum pressure compliance** under TCEQ regulatory scenarios.

## Architecture Overview
```
CSV Data Sources → build_inp_from_csv.py → EPANET .inp → epanet_runner_plus.py → Scenario CSVs
     ↓                                                              ↓
nodes_ready.csv + Master_Edge_Test_Sheet.csv          Pressure/flow results per node
```

## Key Data Files
| File | Purpose | Critical Columns |
|------|---------|------------------|
| `nodes_ready.csv` | Node definitions | `NodeID, Type, Elevation_ft, BaseDemand_gpm, X, Y` |
| `Master_Edge_Test_Sheet.csv` | Pipe/valve topology | `LinkID, LinkType, Node1, Node2, Length_ft, Diameter_in` |
| `Baseline_FIXED_*.inp` | Production EPANET models (use these, not archived versions) |

## Node Naming Conventions
- **`J_CNT##`** - Customer connections (1-80) with demand via pattern multiplier
- **`J_SNT#_###`** - Service line trunk segments (e.g., `J_SNT1_445_500`)
- **`J_TEE_*`** - Tee fittings (demand=0.0)
- **`V#`** - Flow control valves (FCV, typically set to 20 GPM)
- **`J_BP1_DIS/SUC`** - Booster pump discharge/suction nodes
- **Critical monitoring**: `J_CNT36`, `J_CNT41`, `J_CNT80` (end-of-line, lowest pressure)

## Standard Workflow
```bash
# 1. Validate data before building
python reconcile_nodes_ready.py      # Check node data quality
python master_edge_analyzer.py       # Check edge topology

# 2. Generate EPANET input file
python build_inp_from_csv.py         # Creates auto_built.inp

# 3. Run simulations (hardcoded paths in script - edit INP path first)
python epanet_runner_plus.py         # Outputs Scenario_*.csv files
```

## Demand Scenarios
| Scenario | GPM/connection | Total GPM | Use Case |
|----------|---------------|-----------|----------|
| Agreed Order | 0.14 | 11.20 | Regulatory minimum |
| TCEQ Minimum | 0.60 | 48.00 | Compliance baseline |
| RV Park Modified | 0.75 | 60.00 | High-demand testing |
| Stress Test | 1.25 | 100.00 | Worst-case validation |

## Code Conventions
- **CSV Headers**: Must match exactly (case-sensitive). See `NODES_HDR` and `EDGES_HDR` in [build_inp_from_csv.py](build_inp_from_csv.py)
- **Elevation Values**: Negative numbers indicate depth below datum; positive values are likely errors
- **Zero-Length Pipes**: Automatically converted to 1 ft (EPANET requirement)
- **Missing Patterns**: Default to `StressTest` (constant multiplier of 1.0)

## Common Data Issues (reconcile_nodes_ready.py handles)
- Column typos: `TyJe` → `Type`, `BaseDemand_gJm` → `BaseDemand_gpm`
- Type typos: `JumJ` → `Junction`, `Pipie` → `Pipe`
- Sign errors: Positive elevations that should be negative

## Key Constants
```python
COMPLIANCE_THRESHOLD = 20.0   # psi - TCEQ regulatory minimum (do not change)
OPERATING_MIN = 38.0          # psi - pressure tank lower setpoint
OPERATING_MAX = 60.0          # psi - pressure tank upper setpoint
```

## Dependencies
- `wntr` - EPANET Python interface
- `epanettools` - Alternative EPANET bindings (used in `epanet_runner_plus.py`)
- `pandas`, `numpy`, `matplotlib` - Data analysis and visualization

## Important: FIXED vs Legacy Models
**Always use `Baseline_FIXED_*.inp` files.** Legacy models in subdirectories incorrectly assigned demands to infrastructure nodes (tanks, pumps, tees). FIXED models set infrastructure `demand=0.0`—only `J_CNT##` customer nodes have demand.
