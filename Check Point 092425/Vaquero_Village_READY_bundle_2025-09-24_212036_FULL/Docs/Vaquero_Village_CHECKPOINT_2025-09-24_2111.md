# Vaquero Village — Checkpoint Summary (2025-09-24 17:11:21 EDT)

## Snapshot
- Strict **Darcy–Weisbach** modeling maintained throughout (valves preserved, curves not enforced).
- Backdrop grid corrected to **1/16"** → **6.25 ft per square**.
- NodeID normalization applied (EPANET rules: start letter, A–Z/0–9/_, ≤31).

## Edges
- ⬜ Master_Edge_READY.csv — Edges that passed hard checks (Darcy–Weisbach; valves preserved)
- ⬜ Master_Edge_REJECTS.csv — Edges that failed checks with reasons
- ⬜ Master_Edge_VALIDATION.txt — Per-sheet validation summary
- ⬜ Master_Edge_PROPOSED_FIXES.csv — Proposed self-loop _TEE fixes applied to NodeID2 on 0-ft links
- ⬜ Master_Edge_SELFLOOP_PATCH.csv — Patch log for _TEE fixes
- ⬜ Partial_No_2_READY.csv — Partial No 2 edges READY
- ⬜ Partial_No_2_REJECTS.csv — Partial No 2 edges REJECTS
- ⬜ Partial_No_2_VALIDATION.txt — Partial No 2 validation report
- ⬜ Edges_READY.csv — READY edges from earlier partial
- ⬜ Edges_REJECTS.csv — REJECTS edges from earlier partial
- ⬜ Edges_Data_Dictionary.txt — Edges CSV data dictionary (DW only)

## Nodes
- ⬜ Vaquero_Village_nodes_VALIDATED.csv — Validated nodes with notes
- ⬜ Vaquero_Village_nodes_READY.csv — Nodes READY
- ⬜ Vaquero_Village_nodes_REJECTS.csv — Nodes REJECTS
- ⬜ Vaquero_Village_nodes_PATCHLOG.csv — Nodes validation patch log
- ⬜ Vaquero_Village_nodes_FILLONLY.csv — Nodes with fill-only policy applied
- ⬜ Vaquero_Village_nodes_FILLONLY_READY.csv — Fill-only READY
- ⬜ Vaquero_Village_nodes_FILLONLY_REJECTS.csv — Fill-only REJECTS
- ⬜ Vaquero_Village_nodes_FILLONLY_PATCHLOG.csv — Fill-only patch log
- ⬜ Vaquero_Village_nodes2_IDFIXED.csv — NodeID strict-compliant (applied)
- ⬜ Vaquero_Village_nodes2_ID_PATCHMAP.csv — NodeID patch map (old→new, actions)
- ⬜ Vaquero_Village_nodes2_IDFIXED_REMAINING_ISSUES.csv — NodeID remaining issues (should be empty)

## Backdrop
- ⬜ EPANET_BACKDROP_snippet.txt — Generic [BACKDROP] block
- ⬜ Backdrop_Calibration.md — Original calibration guide (1/2" grid assumption)
- ⬜ Backdrop_Calibration_CORRECTED.md — Corrected guide (1/16" grid ⇒ 6.25 ft/sq)
- ⬜ convert_to_bmp_windows.bat — PDF→BMP converter (ImageMagick)
- ⬜ Where_to_put_BACKDROP_in_INP.txt — INP placement helper
- ⬜ EPANET_BACKDROP_from_BMP.txt — Auto-estimated [BACKDROP] from BMP metadata

## Scripts
- ⬜ merge_edges_to_master.py — Merge edge CSVs → MASTER with validation
- ⬜ validate_nodes.py — Node CSV validator
- ⬜ grid_to_nodes.py — Squares→feet converter for nodes (1/16" grid)
- ⬜ grid_measurements_template.csv — Measurements template (SquaresX/Y)
- ⬜ grid_calibration.json — Calibration JSON (6.25 ft/sq; margins)
- ⬜ README_nodes_from_grid.md — Quickstart for measuring from grid

## Suggested Next Actions
1. **Edges**: If happy with `_TEE` node approach, propagate `_TEE` nodes into the **Nodes** list (zero demand unless needed).
2. **Nodes**: Use *fill-only* workflow to compute missing `X_ft/Y_ft` from `SquaresX/Y` (6.25 ft/sq).
3. **Backdrop**: Count usable grid squares and update `[BACKDROP] DIMENSIONS/OFFSET` to lock alignment.
4. **INP Build**: When edges & nodes are finalized, run the builder to produce the INP, then spot-check headloss/pressures at valves and tees.
