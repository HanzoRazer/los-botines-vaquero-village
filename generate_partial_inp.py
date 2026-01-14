import pandas as pd

import os

# Load the Master Edge Test Sheet
df = pd.read_csv(r'C:\Users\thepr\Downloads\Los Botines Vaquero Village\Master_Edge_Test_Sheet.csv', encoding='latin-1')

# Output INP file path
output_dir = r'C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Output'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'partial_network.inp')

with open(output_path, 'w') as f:
    # Header
    f.write("[TITLE]\n")
    f.write("Los Botines Vaquero Village Water Network - Partial INP\n")
    f.write("Generated from Master_Edge_Test_Sheet.csv\n")
    f.write("Note: JUNCTIONS, RESERVOIRS, TANKS, and COORDINATES sections need to be added\n\n")
    
    # Options section
    f.write("[OPTIONS]\n")
    f.write("Units           GPM\n")
    f.write("Headloss        D-W\n")
    f.write("Specific Gravity 1.0\n")
    f.write("Viscosity       1.0\n")
    f.write("Trials          40\n")
    f.write("Accuracy        0.001\n")
    f.write("CHECKFREQ       2\n")
    f.write("MAXCHECK        10\n")
    f.write("DAMPLIMIT       0\n")
    f.write("Unbalanced      Continue 10\n\n")
    
    # PIPES Section
    f.write("[PIPES]\n")
    f.write(";ID              Node1           Node2           Length      Diameter    Roughness   MinorLoss   Status\n")
    
    pipes = df[df['LinkType'].isin(['Pipe', 'Pipie'])]
    for _, row in pipes.iterrows():
        link_id = str(row['LinkID']).strip()
        node1 = str(row['Node1']).strip()
        node2 = str(row['Node2']).strip()
        length = float(row['Length_ft']) if pd.notna(row['Length_ft']) else 10.0
        diameter = float(row['Diameter_in']) if pd.notna(row['Diameter_in']) else 2.469
        roughness = float(row['Roughness']) if pd.notna(row['Roughness']) else 0.000167
        minor_loss = float(row['MinorLoss_K']) if pd.notna(row['MinorLoss_K']) and str(row['MinorLoss_K']).replace('.','').isdigit() else 0.0
        status = str(row['Status']).strip() if pd.notna(row['Status']) else 'Open'
        
        f.write(f"{link_id:16} {node1:16} {node2:16} {length:12.2f} {diameter:12.4f} {roughness:12.6f} {minor_loss:12.2f} {status:8}\n")
    
    f.write("\n")
    
    # VALVES Section
    f.write("[VALVES]\n")
    f.write(";ID              Node1           Node2           Diameter    Type    Setting     MinorLoss\n")
    
    valves = df[df['LinkType'] == 'Valve']
    for _, row in valves.iterrows():
        link_id = str(row['LinkID']).strip()
        node1 = str(row['Node1']).strip()
        node2 = str(row['Node2']).strip()
        diameter = float(row['Diameter_in']) if pd.notna(row['Diameter_in']) else 2.469
        valve_type = str(row['Valve  Type']).strip() if pd.notna(row['Valve  Type']) else 'TCV'
        setting = float(row['Setting']) if pd.notna(row['Setting']) else 0.0
        minor_loss = float(row['MinorLoss_K']) if pd.notna(row['MinorLoss_K']) and str(row['MinorLoss_K']).replace('.','').isdigit() else 0.0
        
        f.write(f"{link_id:16} {node1:16} {node2:16} {diameter:12.4f} {valve_type:8} {setting:12.2f} {minor_loss:12.2f}\n")
    
    f.write("\n")
    
    # Tags section
    f.write("[TAGS]\n\n")
    
    # End section
    f.write("[END]\n")

print(f"Partial INP file generated: {output_path}")
print(f"\nSummary:")
print(f"  Pipes written: {len(pipes)}")
print(f"  Valves written: {len(valves)}")
print(f"\nNote: You still need to add:")
print(f"  - [JUNCTIONS] section with node elevations and demands")
print(f"  - [RESERVOIRS] section (if any)")
print(f"  - [TANKS] section (pressure tanks)")
print(f"  - [PUMPS] section (booster pumps)")
print(f"  - [COORDINATES] section for visualization")
print(f"  - [PATTERNS] section for demand patterns")
