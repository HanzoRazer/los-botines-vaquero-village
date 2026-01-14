import pandas as pd

# Path to nodes.csv
nodes_path = 'EPANET/WT8/nodes.csv'
# List of missing nodes to add
missing_nodes = [
    {'NodeID': 'J_SNT1_160', 'Type': 'Junction'},
    {'NodeID': 'J_V1_IN_160', 'Type': 'Junction'},
]

# Read nodes.csv, skipping any extra headers or blank lines
rows = []
with open(nodes_path, encoding='utf-8') as f:
    for line in f:
        line = line.strip('\r\n')
        if not line or line.startswith('NodeID'):
            continue
        parts = line.split(',')
        # Pad to 10 columns
        parts += [''] * (10 - len(parts))
        rows.append(parts[:10])

# Add missing nodes if not present
existing_ids = {row[0] for row in rows}
for node in missing_nodes:
    if node['NodeID'] not in existing_ids:
        rows.append([node['NodeID'], node['Type']] + [''] * 8)

# Write cleaned file with single header, all rows 10 columns, no blank lines
header = ['NodeID','Type','Elevation_ft','BaseDemand_gpm','Pattern','X','Y','InitLevel_ft','MinLevel_ft','MaxLevel_ft']
with open(nodes_path, 'w', encoding='utf-8') as f:
    f.write(','.join(header) + '\n')
    for row in rows:
        f.write(','.join(row) + '\n')
print(f"nodes.csv cleaned and missing nodes added. Total rows: {len(rows)}")
