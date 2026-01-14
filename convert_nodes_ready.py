import pandas as pd

input_csv = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\nodes_ready.csv"
output_csv = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\nodes_ready_epanet.csv"

df = pd.read_csv(input_csv)

df_out = pd.DataFrame()
df_out['NodeID'] = df['NodeID']
df_out['Type'] = df['Type']
df_out['Elevation_ft'] = df['Elevation_ft']
df_out['BaseDemand_gpm'] = df['BaseDemand_gpm']
df_out['Pattern'] = df['Pattern'] if 'Pattern' in df else ''
df_out['X'] = df['X'] if 'X' in df else 0
df_out['Y'] = df['Y'] if 'Y' in df else 0
df_out['InitLevel_ft'] = df['InitLevel_ft'] if 'InitLevel_ft' in df else ''
df_out['MinLevel_ft'] = df['MinLevel_ft'] if 'MinLevel_ft' in df else ''
df_out['MaxLevel_ft'] = df['MaxLevel_ft'] if 'MaxLevel_ft' in df else ''

df_out.to_csv(output_csv, index=False)
print(f"Converted file saved as: {output_csv}")


