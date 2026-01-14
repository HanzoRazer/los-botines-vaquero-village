import pandas as pd
import os
import re

# File path
file_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Master_Edge_Test_Sheet.csv"

# Load the CSV
df = pd.read_csv(file_path, encoding='latin-1')

print("=" * 80)
print("DATA VALIDATION REPORT - Master Edge Test Sheet")
print("=" * 80)
print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Get column names
col_names = df.columns.tolist()
print(f"\nColumn names: {col_names[:10]}...")  # Show first 10

# ==============================================================================
# 1. CHECK LINK TYPE CONSISTENCY
# ==============================================================================
print("\n" + "=" * 80)
print("1. LINK TYPE VALIDATION")
print("=" * 80)

valid_link_types = ['Pipe', 'Valve', 'Pump']
link_type_counts = df['LinkType'].value_counts()
print("\nLink type distribution:")
for link_type, count in link_type_counts.items():
    if link_type not in valid_link_types:
        print(f"  ⚠️  {link_type}: {count} (INVALID/TYPO)")
    else:
        print(f"  ✓  {link_type}: {count}")

# Find rows with invalid link types
invalid_types = df[~df['LinkType'].isin(valid_link_types)]
if len(invalid_types) > 0:
    print(f"\n⚠️  Found {len(invalid_types)} rows with invalid LinkType:")
    print(invalid_types[['LinkID', 'LinkType', 'Node1', 'Node2']].to_string(index=False))

# ==============================================================================
# 2. CHECK FOR MISSING REQUIRED FIELDS
# ==============================================================================
print("\n" + "=" * 80)
print("2. MISSING REQUIRED FIELDS")
print("=" * 80)

required_fields = ['LinkID', 'LinkType', 'Node1', 'Node2', 'Length_ft', 'Diameter_in']
for field in required_fields:
    if field in df.columns:
        missing_count = df[field].isna().sum()
        empty_count = (df[field].astype(str).str.strip() == '').sum()
        total_missing = missing_count + empty_count
        if total_missing > 0:
            print(f"  ⚠️  {field}: {total_missing} missing/empty values")
            # Show affected rows
            affected = df[df[field].isna() | (df[field].astype(str).str.strip() == '')]
            if len(affected) > 0 and len(affected) <= 10:
                print(f"     Affected LinkIDs: {affected['LinkID'].tolist()}")
        else:
            print(f"  ✓  {field}: No missing values")

# ==============================================================================
# 3. CHECK NUMERIC FIELD DATA TYPES
# ==============================================================================
print("\n" + "=" * 80)
print("3. NUMERIC FIELD VALIDATION")
print("=" * 80)

numeric_fields = ['Length_ft', 'Diameter_in', 'Roughness', 'MinorLoss_K', 'Setting']
for field in numeric_fields:
    if field in df.columns:
        print(f"\n{field}:")
        # Try to convert to numeric
        numeric_series = pd.to_numeric(df[field], errors='coerce')
        non_numeric = df[field].notna() & numeric_series.isna()
        non_numeric_count = non_numeric.sum()
        
        if non_numeric_count > 0:
            print(f"  ⚠️  {non_numeric_count} non-numeric values found")
            print(f"     Affected rows: {df[non_numeric]['LinkID'].tolist()[:10]}")
            print(f"     Sample values: {df[non_numeric][field].unique()[:5].tolist()}")
        else:
            print(f"  ✓  All values are numeric or empty")
            
        # Check for negative values where they shouldn't be
        if field in ['Length_ft', 'Diameter_in']:
            negative_vals = df[numeric_series < 0]
            if len(negative_vals) > 0:
                print(f"  ⚠️  {len(negative_vals)} negative values (should be positive)")
                print(f"     Affected LinkIDs: {negative_vals['LinkID'].tolist()}")

# ==============================================================================
# 4. CHECK NODE NAME CONSISTENCY
# ==============================================================================
print("\n" + "=" * 80)
print("4. NODE NAME VALIDATION")
print("=" * 80)

# Get all unique nodes
all_nodes = set(df['Node1'].dropna()).union(set(df['Node2'].dropna()))
print(f"\nTotal unique nodes: {len(all_nodes)}")

# Check for nodes with trailing/leading spaces
nodes_with_spaces = [n for n in all_nodes if str(n) != str(n).strip()]
if nodes_with_spaces:
    print(f"\n⚠️  {len(nodes_with_spaces)} nodes have leading/trailing spaces:")
    print(f"   {nodes_with_spaces[:10]}")
else:
    print("  ✓  No nodes with leading/trailing spaces")

# Check for inconsistent node naming patterns
node_patterns = {}
for node in all_nodes:
    node_str = str(node)
    # Extract pattern (e.g., J_SNT, J_TEE, J_CNT, V, etc.)
    match = re.match(r'^([A-Z_]+)', node_str)
    if match:
        pattern = match.group(1)
        node_patterns[pattern] = node_patterns.get(pattern, 0) + 1

print("\nNode naming patterns:")
for pattern, count in sorted(node_patterns.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {pattern}*: {count} nodes")

# ==============================================================================
# 5. CHECK FOR SELF-LOOPS (Node1 = Node2)
# ==============================================================================
print("\n" + "=" * 80)
print("5. SELF-LOOP DETECTION")
print("=" * 80)

self_loops = df[df['Node1'] == df['Node2']]
if len(self_loops) > 0:
    print(f"⚠️  Found {len(self_loops)} self-loops (Node1 = Node2):")
    print(self_loops[['LinkID', 'LinkType', 'Node1', 'Node2']].to_string(index=False))
else:
    print("✓  No self-loops detected")

# ==============================================================================
# 6. CHECK VALVE-SPECIFIC FIELDS
# ==============================================================================
print("\n" + "=" * 80)
print("6. VALVE CONFIGURATION VALIDATION")
print("=" * 80)

valves = df[df['LinkType'] == 'Valve']
print(f"\nTotal valves: {len(valves)}")

# Check valve types
if 'Valve  Type' in df.columns:
    valve_types = valves['Valve  Type'].value_counts()
    print("\nValve types:")
    for vtype, count in valve_types.items():
        print(f"  {vtype}: {count}")
    
    # Check for valves missing type
    missing_valve_type = valves[valves['Valve  Type'].isna()]
    if len(missing_valve_type) > 0:
        print(f"\n⚠️  {len(missing_valve_type)} valves missing 'Valve Type':")
        print(f"   {missing_valve_type['LinkID'].tolist()}")

# Check valve settings
if 'Setting' in df.columns:
    valves_missing_setting = valves[valves['Setting'].isna()]
    if len(valves_missing_setting) > 0:
        print(f"\n⚠️  {len(valves_missing_setting)} valves missing 'Setting' value:")
        print(f"   {valves_missing_setting['LinkID'].tolist()}")

# ==============================================================================
# 7. CHECK FOR ORPHANED NODES (nodes that appear only once)
# ==============================================================================
print("\n" + "=" * 80)
print("7. CONNECTIVITY CHECK (ORPHANED NODES)")
print("=" * 80)

from collections import Counter
node_connections = Counter()
for _, row in df.iterrows():
    if pd.notna(row['Node1']):
        node_connections[row['Node1']] += 1
    if pd.notna(row['Node2']):
        node_connections[row['Node2']] += 1

orphaned_nodes = [node for node, count in node_connections.items() if count == 1]
if orphaned_nodes:
    print(f"⚠️  Found {len(orphaned_nodes)} potentially orphaned nodes (only 1 connection):")
    print(f"   Sample: {orphaned_nodes[:20]}")
else:
    print("✓  No orphaned nodes detected")

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

issues_found = []
if len(invalid_types) > 0:
    issues_found.append(f"Invalid LinkType values: {len(invalid_types)} rows")
if len(self_loops) > 0:
    issues_found.append(f"Self-loops: {len(self_loops)} rows")
if nodes_with_spaces:
    issues_found.append(f"Nodes with spaces: {len(nodes_with_spaces)}")
if len(orphaned_nodes) > 0:
    issues_found.append(f"Orphaned nodes: {len(orphaned_nodes)}")

if issues_found:
    print("\n⚠️  ISSUES DETECTED:")
    for issue in issues_found:
        print(f"  • {issue}")
else:
    print("\n✓  No critical issues detected!")

print("\n" + "=" * 80)
