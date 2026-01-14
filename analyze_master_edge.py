import pandas as pd

# Load the Master Edge Test Sheet (with encoding to handle special characters)
df = pd.read_csv(r'C:\Users\thepr\Downloads\Los Botines Vaquero Village\Master_Edge_Test_Sheet.csv', encoding='latin-1')

print("=" * 80)
print("MASTER EDGE TEST SHEET ANALYSIS FOR EPANET INP GENERATION")
print("=" * 80)

print(f"\nTotal rows: {len(df)}")
print(f"\nColumns: {list(df.columns)}")

print("\n" + "-" * 80)
print("LINK TYPE DISTRIBUTION:")
print("-" * 80)
link_types = df['LinkType'].value_counts()
for link_type, count in link_types.items():
    print(f"  {link_type}: {count}")

print("\n" + "-" * 80)
print("VALVE DETAILS (First 15):")
print("-" * 80)
valves = df[df['LinkType'] == 'Valve'][['LinkID', 'Node1', 'Node2', 'Setting', 'Valve  Type']]
print(valves.head(15).to_string(index=False))

print("\n" + "-" * 80)
print("PIPE DIAMETER DISTRIBUTION:")
print("-" * 80)
diameter_dist = df[df['LinkType'].str.contains('Pipe', na=False)]['Diameter_in'].value_counts()
for diameter, count in diameter_dist.items():
    print(f"  {diameter} inches: {count} pipes")

print("\n" + "-" * 80)
print("UNIQUE NODES (Node1 and Node2):")
print("-" * 80)
unique_nodes = set(df['Node1'].dropna()).union(set(df['Node2'].dropna()))
print(f"  Total unique nodes: {len(unique_nodes)}")
print(f"  Sample nodes: {list(unique_nodes)[:20]}")

print("\n" + "-" * 80)
print("LINKS WITH MISSING OR UNUSUAL DATA:")
print("-" * 80)
missing_length = df[df['Length_ft'].isna() | (df['Length_ft'] == 0)]
print(f"  Links with missing/zero length: {len(missing_length)}")
if len(missing_length) > 0:
    print(missing_length[['LinkID', 'LinkType', 'Node1', 'Node2', 'Length_ft']].to_string(index=False))

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
