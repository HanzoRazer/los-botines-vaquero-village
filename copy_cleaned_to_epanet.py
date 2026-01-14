import pandas as pd

# Read the provided cleaned file
infile = 'nodes_cleaned.csv'
outfile = 'EPANET/WT8/nodes.csv'

df = pd.read_csv(infile, dtype=str)
# Remove any duplicate NodeIDs (just in case)
df = df.drop_duplicates(subset=['NodeID'])
df.to_csv(outfile, index=False)
print(f"nodes.csv written to {outfile} with {len(df)} unique NodeIDs.")
