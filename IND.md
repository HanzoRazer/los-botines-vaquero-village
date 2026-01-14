
# IND (Index and Documentation) for EPANET Water Network Project

## Project Overview
This document provides a structured index and summary for the Los Botines Vaquero Village EPANET water distribution modeling project. It lists all key files, describes the workflow, and provides guidance for running simulations.

---

## Key Files

- `.github/copilot-instructions.md` — AI agent instructions for project conventions and workflows
- `nodes_ready.csv` — Node data (IDs, types, elevations, demands, coordinates)
- `Master_Edge_Test_Sheet.csv` — Edge/topology data (pipes, valves, tees, trunks)
- `build_inp_from_csv.py` — Main script to generate EPANET .inp files from CSVs
- `epanet_runner_plus.py` — Script to run EPANET simulations
- `reconcile_nodes_ready.py` — Node data reconciliation and validation tool
- `master_edge_analyzer.py` — Edge data analysis and validation tool

---

## Node File: nodes_ready.csv

**Columns:**
NodeID, TyJe (Type), Elevation_ft, BaseDemand_gJm, Pattern, X, Y, InitLevel_ft, MinLevel_ft, MaxLevel_ft

**Sample:**
```
NodeID,TyJe,Elevation_ft,BaseDemand_gJm,Pattern,X,Y,InitLevel_ft,MinLevel_ft,MaxLevel_ft
J_RES1_T1,Pipie,-65,20,DailyUse,544.38,73.14,,,
J_T1_M1,Pipe,-104,20,DailyUse,544.44,93.44,7.71,3,7.71
J_T1_SUC,Pipe,-130,20,DailyUse,544.44,97.83,9 08,3.2,9.08
... (see full file for all nodes)
```

---

## Edge File: Master_Edge_Test_Sheet.csv

**Purpose:**
Defines the network topology, including pipes, valves, tees, and trunks. Used to build the connectivity for the EPANET model.

---

## Workflow

1. **Prepare Data**
   - Ensure `nodes_ready.csv` and `Master_Edge_Test_Sheet.csv` are up to date and error-free.
   - Use `reconcile_nodes_ready.py` and `master_edge_analyzer.py` for validation if needed.

2. **Build EPANET Input File**
   - Run `build_inp_from_csv.py` to generate the `.inp` file for EPANET.
   - Example:
     ```
     python build_inp_from_csv.py
     ```

3. **Run Simulation**
   - Use `epanet_runner_plus.py` to execute the simulation.
   - Example:
     ```
     python epanet_runner_plus.py
     ```

4. **Analyze Results**
   - Review output files and scenario CSVs for hydraulic results.
   - Use provided scripts for further analysis or visualization.

---

## Notes
- All data files must be properly formatted and validated before running simulations.
- The `.github/copilot-instructions.md` file contains detailed AI agent guidance for automation and code contributions.
- For troubleshooting, check for errors in the reconciliation and build scripts before running EPANET.

---

## Contact
For questions or contributions, refer to the project maintainer or the `.github/copilot-instructions.md` file.
