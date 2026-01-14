import pandas as pd

nodes_path = 'EPANET/WT8/nodes.csv'
df = pd.read_csv(nodes_path, dtype=str)
df = df.drop_duplicates(subset=['NodeID'], keep='first')
df.to_csv(nodes_path, index=False)
print(f"Removed duplicates. {len(df)} unique NodeIDs remain.")
