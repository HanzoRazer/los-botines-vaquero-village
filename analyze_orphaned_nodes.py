import pandas as pd
import os
from collections import Counter, defaultdict

# File path
file_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Master_Edge_Test_Sheet.csv"

# Load the CSV
df = pd.read_csv(file_path, encoding='latin-1')

print("=" * 80)
print("ORPHANED NODES ANALYSIS - Master Edge Test Sheet")
print("=" * 80)

# Count connections for each node
node_connections = Counter()
node_link_details = defaultdict(list)  # Track which links connect to each node

for idx, row in df.iterrows():
    link_id = row['LinkID']
    node1 = row['Node1']
    node2 = row['Node2']
    
    if pd.notna(node1):
        node_connections[node1] += 1
        node_link_details[node1].append({
            'LinkID': link_id,
            'LinkType': row['LinkType'],
            'ConnectedTo': node2,
            'Direction': 'Node1'
        })
    
    if pd.notna(node2):
        node_connections[node2] += 1
        node_link_details[node2].append({
            'LinkID': link_id,
            'LinkType': row['LinkType'],
            'ConnectedTo': node1,
            'Direction': 'Node2'
        })

# Identify orphaned nodes (only 1 connection)
orphaned_nodes = [node for node, count in node_connections.items() if count == 1]

print(f"\nTotal unique nodes: {len(node_connections)}")
print(f"Orphaned nodes (1 connection): {len(orphaned_nodes)}")
print(f"Well-connected nodes (2+ connections): {len(node_connections) - len(orphaned_nodes)}")

# ==============================================================================
# CATEGORIZE ORPHANED NODES
# ==============================================================================

# Patterns for intentional stubs/dead-ends
stub_patterns = ['_Stub', 'CNT', 'RES', 'TANK', 'J_BP1_DIS', 'J_BJ1_DIS']
source_patterns = ['RES', 'TANK', 'M1']
service_patterns = ['CNT', '_Stub']

intentional_orphans = {
    'Service Connection Stubs (CNT/Stub)': [],
    'Source/Reservoir Nodes': [],
    'Tank/Storage Nodes': [],
    'Valve Inlet/Outlet Stubs': [],
    'Other Intentional (Pumps, etc.)': [],
}

problematic_orphans = {
    'Missing TEE Connections': [],
    'Incomplete Pipe Segments': [],
    'Unclassified Orphans': [],
}

for node in orphaned_nodes:
    node_str = str(node)
    details = node_link_details[node][0]  # Get the single connection
    
    # Categorize by pattern
    if 'CNT' in node_str or '_Stub' in node_str:
        intentional_orphans['Service Connection Stubs (CNT/Stub)'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif 'RES' in node_str:
        intentional_orphans['Source/Reservoir Nodes'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif 'TANK' in node_str or 'M1' in node_str:
        intentional_orphans['Tank/Storage Nodes'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif node_str.startswith('J_V') and ('_IN' in node_str or '_OUT' in node_str):
        intentional_orphans['Valve Inlet/Outlet Stubs'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif 'BP' in node_str or 'BJ' in node_str or 'SUC' in node_str or 'DIS' in node_str:
        intentional_orphans['Other Intentional (Pumps, etc.)'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif 'TEE' in node_str:
        problematic_orphans['Missing TEE Connections'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    elif node_str.startswith('J_SNT'):
        problematic_orphans['Incomplete Pipe Segments'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })
    else:
        problematic_orphans['Unclassified Orphans'].append({
            'Node': node,
            'LinkID': details['LinkID'],
            'LinkType': details['LinkType'],
            'ConnectedTo': details['ConnectedTo']
        })

# ==============================================================================
# PRINT INTENTIONAL ORPHANS
# ==============================================================================
print("\n" + "=" * 80)
print("INTENTIONAL ORPHANED NODES (Expected/By Design)")
print("=" * 80)

for category, nodes in intentional_orphans.items():
    if nodes:
        print(f"\n{category}: {len(nodes)} nodes")
        print("-" * 80)
        for item in nodes[:10]:  # Show first 10
            print(f"  {item['Node']:40} → Link: {item['LinkID']:30} Connected to: {item['ConnectedTo']}")
        if len(nodes) > 10:
            print(f"  ... and {len(nodes) - 10} more")

# ==============================================================================
# PRINT PROBLEMATIC ORPHANS
# ==============================================================================
print("\n" + "=" * 80)
print("⚠️  PROBLEMATIC ORPHANED NODES (Require Review)")
print("=" * 80)

total_problematic = sum(len(nodes) for nodes in problematic_orphans.values())

if total_problematic > 0:
    for category, nodes in problematic_orphans.items():
        if nodes:
            print(f"\n⚠️  {category}: {len(nodes)} nodes")
            print("-" * 80)
            for item in nodes[:15]:  # Show first 15
                print(f"  {item['Node']:40} → Link: {item['LinkID']:30} Type: {item['LinkType']}")
            if len(nodes) > 15:
                print(f"  ... and {len(nodes) - 15} more")
else:
    print("\n✓  No problematic orphaned nodes detected!")

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

total_intentional = sum(len(nodes) for nodes in intentional_orphans.values())
print(f"\nIntentional orphaned nodes: {total_intentional} ({total_intentional/len(orphaned_nodes)*100:.1f}%)")
for category, nodes in intentional_orphans.items():
    if nodes:
        print(f"  • {category}: {len(nodes)}")

print(f"\nProblematic orphaned nodes: {total_problematic} ({total_problematic/len(orphaned_nodes)*100:.1f}%)")
for category, nodes in problematic_orphans.items():
    if nodes:
        print(f"  • {category}: {len(nodes)}")

# ==============================================================================
# SAVE DETAILED REPORT TO CSV
# ==============================================================================
output_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Output\orphaned_nodes_report.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Prepare data for CSV
report_data = []
for category, nodes in intentional_orphans.items():
    for item in nodes:
        report_data.append({
            'Node': item['Node'],
            'Category': category,
            'Status': 'Intentional',
            'LinkID': item['LinkID'],
            'LinkType': item['LinkType'],
            'ConnectedTo': item['ConnectedTo']
        })

for category, nodes in problematic_orphans.items():
    for item in nodes:
        report_data.append({
            'Node': item['Node'],
            'Category': category,
            'Status': 'Problematic',
            'LinkID': item['LinkID'],
            'LinkType': item['LinkType'],
            'ConnectedTo': item['ConnectedTo']
        })

report_df = pd.DataFrame(report_data)
report_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n\nDetailed report saved to: {output_path}")
print("=" * 80)
