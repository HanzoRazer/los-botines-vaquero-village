import pandas as pd
import os

# File path
file_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Master_Edge_Test_Sheet.csv"

# Load the CSV
df = pd.read_csv(file_path, encoding='latin-1')

# Output file
output_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Output\Issues_To_Fix_Manually.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("MASTER EDGE TEST SHEET - ISSUES TO FIX MANUALLY\n")
    f.write("=" * 80 + "\n\n")
    
    # ==============================================================================
    # ISSUE 1: LinkType Typos
    # ==============================================================================
    f.write("ISSUE 1: LinkType Typos (2 rows)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: 'Pipie' should be 'Pipe'\n\n")
    
    invalid_types = df[df['LinkType'] == 'Pipie']
    f.write("Rows to fix:\n")
    for idx, row in invalid_types.iterrows():
        f.write(f"  Row {idx + 2} (Excel): LinkID = {row['LinkID']}\n")
        f.write(f"    Current: LinkType = 'Pipie'\n")
        f.write(f"    Fix to:  LinkType = 'Pipe'\n\n")
    
    # ==============================================================================
    # ISSUE 2: Self-Loop
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 2: Self-Loop (1 row)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: Node1 and Node2 are the same (pipe connects to itself)\n\n")
    
    self_loops = df[df['Node1'] == df['Node2']]
    for idx, row in self_loops.iterrows():
        f.write(f"  Row {idx + 2} (Excel): LinkID = {row['LinkID']}\n")
        f.write(f"    Current: Node1 = {row['Node1']}, Node2 = {row['Node2']}\n")
        f.write(f"    Action: Verify correct Node2 value or delete this row if duplicate\n\n")
    
    # ==============================================================================
    # ISSUE 3: Node Names with Trailing Spaces
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 3: Node Names with Trailing Spaces (4 nodes)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: Node names have extra spaces that will cause connection issues\n\n")
    
    nodes_with_spaces = []
    for idx, row in df.iterrows():
        node1 = str(row['Node1'])
        node2 = str(row['Node2'])
        if node1 != node1.strip():
            nodes_with_spaces.append((idx, 'Node1', node1, node1.strip()))
        if node2 != node2.strip():
            nodes_with_spaces.append((idx, 'Node2', node2, node2.strip()))
    
    f.write("Rows to fix:\n")
    for idx, col, current, fixed in nodes_with_spaces:
        f.write(f"  Row {idx + 2} (Excel), Column {col}\n")
        f.write(f"    Current: '{current}'\n")
        f.write(f"    Fix to:  '{fixed}'\n\n")
    
    # ==============================================================================
    # ISSUE 4: Missing Valve Settings
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 4: Missing Valve Settings (7 valves)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: TCV valves need a Setting value to function properly\n\n")
    
    valves = df[df['LinkType'] == 'Valve']
    missing_settings = valves[valves['Setting'].isna()]
    
    f.write("Rows to fix:\n")
    for idx, row in missing_settings.iterrows():
        f.write(f"  Row {idx + 2} (Excel): LinkID = {row['LinkID']}\n")
        f.write(f"    Valve Type: {row['Valve  Type']}\n")
        f.write(f"    Current: Setting = (empty)\n")
        f.write(f"    Action: Add appropriate Setting value\n")
        f.write(f"      - For TCV: typically 0-100 (percent open)\n")
        f.write(f"      - For FCV: flow rate in GPM (e.g., 20)\n\n")
    
    # ==============================================================================
    # ISSUE 5: Non-Numeric MinorLoss_K Values
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 5: Non-Numeric Minor Loss Values (172 rows)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: MinorLoss_K column contains 'K_TEE_RUN_DIV' text instead of numbers\n\n")
    
    numeric_series = pd.to_numeric(df['MinorLoss_K'], errors='coerce')
    non_numeric = df['MinorLoss_K'].notna() & numeric_series.isna()
    non_numeric_rows = df[non_numeric]
    
    f.write(f"Found {len(non_numeric_rows)} rows with text 'K_TEE_RUN_DIV'\n\n")
    f.write("Action needed:\n")
    f.write("  1. Decide on a numeric value for TEE minor loss coefficient\n")
    f.write("     (Common values: 0.5 to 2.0 depending on flow direction)\n")
    f.write("  2. Replace 'K_TEE_RUN_DIV' with that numeric value\n\n")
    
    f.write("Sample rows (first 20):\n")
    for idx, row in non_numeric_rows.head(20).iterrows():
        f.write(f"  Row {idx + 2} (Excel): LinkID = {row['LinkID']}, MinorLoss_K = {row['MinorLoss_K']}\n")
    
    if len(non_numeric_rows) > 20:
        f.write(f"\n  ... and {len(non_numeric_rows) - 20} more rows with same issue\n")
    
    # ==============================================================================
    # ISSUE 6: Problematic Orphaned Nodes (TEE Connections)
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 6: Missing TEE Connections (130 nodes)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: TEE fittings appear disconnected (only 1 connection instead of 2+)\n\n")
    f.write("This suggests missing pipe definitions in the network.\n")
    f.write("Each TEE should have:\n")
    f.write("  - TEE_IN: inlet connection\n")
    f.write("  - TEE_OUT: outlet connection(s) - run and/or branch\n\n")
    
    from collections import Counter
    node_connections = Counter()
    for _, row in df.iterrows():
        if pd.notna(row['Node1']):
            node_connections[row['Node1']] += 1
        if pd.notna(row['Node2']):
            node_connections[row['Node2']] += 1
    
    orphaned_tee_nodes = [node for node, count in node_connections.items() 
                          if count == 1 and 'TEE' in str(node)]
    
    f.write(f"TEE nodes with only 1 connection (should have 2+): {len(orphaned_tee_nodes)}\n\n")
    f.write("Sample problematic TEE nodes (first 30):\n")
    for node in orphaned_tee_nodes[:30]:
        # Find which link connects to this node
        link_rows = df[(df['Node1'] == node) | (df['Node2'] == node)]
        if not link_rows.empty:
            link_id = link_rows.iloc[0]['LinkID']
            f.write(f"  {node:50} (connected via: {link_id})\n")
    
    if len(orphaned_tee_nodes) > 30:
        f.write(f"\n  ... and {len(orphaned_tee_nodes) - 30} more TEE nodes\n")
    
    f.write("\nAction: Review network topology and add missing pipe connections\n")
    
    # ==============================================================================
    # ISSUE 7: Incomplete Pipe Segments
    # ==============================================================================
    f.write("\n" + "=" * 80 + "\n")
    f.write("ISSUE 7: Incomplete Pipe Segments (20 nodes)\n")
    f.write("-" * 80 + "\n")
    f.write("Problem: SNT (Service Network Trunk) nodes with only 1 connection\n\n")
    
    orphaned_snt_nodes = [node for node, count in node_connections.items() 
                          if count == 1 and str(node).startswith('J_SNT')]
    
    f.write("SNT nodes that appear disconnected:\n")
    for node in orphaned_snt_nodes:
        link_rows = df[(df['Node1'] == node) | (df['Node2'] == node)]
        if not link_rows.empty:
            link_id = link_rows.iloc[0]['LinkID']
            f.write(f"  {node:50} (via: {link_id})\n")
    
    f.write("\nAction: Verify these are terminal points or add missing connections\n")
    
    # ==============================================================================
    # SUMMARY
    # ==============================================================================
    f.write("\n\n" + "=" * 80 + "\n")
    f.write("SUMMARY - QUICK REFERENCE\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total issues to fix:\n")
    f.write(f"  1. LinkType typos: 2 rows\n")
    f.write(f"  2. Self-loops: 1 row\n")
    f.write(f"  3. Node names with spaces: {len(nodes_with_spaces)} occurrences\n")
    f.write(f"  4. Missing valve settings: 7 rows\n")
    f.write(f"  5. Non-numeric MinorLoss_K: 172 rows\n")
    f.write(f"  6. Missing TEE connections: 130 nodes (requires topology review)\n")
    f.write(f"  7. Incomplete pipe segments: 20 nodes (requires topology review)\n\n")
    f.write("Priority fixes (easy, high impact):\n")
    f.write("  1. Fix 'Pipie' → 'Pipe' (2 rows)\n")
    f.write("  2. Remove trailing spaces from node names (4 locations)\n")
    f.write("  3. Add valve settings (7 rows)\n")
    f.write("  4. Replace 'K_TEE_RUN_DIV' with numeric value (172 rows - use Find/Replace)\n")
    f.write("  5. Fix self-loop (1 row)\n\n")
    f.write("=" * 80 + "\n")

print(f"Manual fix guide created: {output_path}")
print("\nThis file contains:")
print("  - Specific row numbers (Excel format)")
print("  - Current values and what to change them to")
print("  - Clear action items for each issue")
print("  - Summary of all issues at the end")
