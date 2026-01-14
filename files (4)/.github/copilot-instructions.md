# Los Botines Vaquero Village - Water System Analysis

## Project Purpose
EPANET hydraulic simulation analysis to verify **20 psi minimum pressure compliance** for an 80-connection water distribution network under TCEQ regulatory scenarios.

## Key Files & Structure
- **`Baseline_FIXED_*.inp`** - Active EPANET models (use these, not `Old Stuff/`)
- **`epanet_chart_helper.py`** - Parses EPANET exports → generates compliance charts
- **`charts/`** - Output directory for PNG/PDF visualizations
- **`Old Stuff/`** - Deprecated models with incorrect infrastructure demands (ignore)

## Demand Scenarios
| Scenario | GPM/connection | Total GPM | File suffix |
|----------|---------------|-----------|-------------|
| Agreed Order | 0.14 | 11.20 | `_0.14_GPM` |
| TCEQ Minimum | 0.60 | 48.00 | `_0.60_GPM` |
| RV Park Modified | 0.75 | 60.00 | `_0.75_GPM` |
| Stress Test | 1.25 | 100.00 | `_1.25_GPM` |

## Chart Generation Workflow
```bash
# Install dependencies
pip install pandas numpy matplotlib

# Generate compliance charts from EPANET time series exports
python epanet_chart_helper.py node_data.txt -s "0.60 GPM TCEQ Minimum"

# Multiple node files
python epanet_chart_helper.py cnt36.txt cnt41.txt cnt80.txt -s "Stress Test"
```

## EPANET Node Naming Conventions
- **`J_CNT##`** - Customer connections (1-80), these have demand=1.0 with pattern multiplier
- **`J_BP1_DIS`** - Booster pump discharge (high-pressure reference)
- **`J_TEE_*`**, **`J_V#_*`** - Infrastructure nodes (demand=0.0 in FIXED models)
- **Critical monitoring**: `J_CNT36`, `J_CNT41`, `J_CNT80` (end-of-line, lowest pressure)

## EPANET Data Export Format
Time series exports from EPANET use whitespace-delimited format:
```
Node J_BP1_DIS    0.0000    57.7808
Node J_BP1_DIS    0.0333    60.5806
```
The parser auto-detects `.txt`, `.xlsx`, and `.csv` formats.

## Key Constants in epanet_chart_helper.py
```python
COMPLIANCE_THRESHOLD = 20.0  # psi - TCEQ regulatory minimum (do not change)
OPERATING_MIN = 38.0         # psi - pressure tank lower setpoint
OPERATING_MAX = 60.0         # psi - pressure tank upper setpoint
```

## Creating New Scenarios
1. Copy existing `Baseline_FIXED_*.inp` file
2. Edit `[PATTERNS]` section to change demand multiplier
3. Update `[TITLE]` section with scenario description
4. Run simulation in EPANET 2.2 GUI (not command line)
5. Export critical node time series data
6. Generate charts with `epanet_chart_helper.py`

## FIXED vs Old Models
**Always use `Baseline_FIXED_*` files.** The `Old Stuff/` models incorrectly assigned demands to infrastructure nodes (tanks, pumps, tees). FIXED models set infrastructure demand=0.0 GPM—only `J_CNT##` customer nodes have demand via pattern multiplier.
