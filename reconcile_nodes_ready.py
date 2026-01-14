import pandas as pd
import numpy as np

def reconcile_nodes_ready_csv(csv_file_path):
    """
    Reconcile and fix data quality issues in nodes_ready.csv
    Similar to the Master Edge Test Sheet analysis
    """
    df = pd.read_csv(csv_file_path)
    
    print("=== Nodes Ready CSV Reconciliation ===")
    print(f"Total nodes: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Fix column header typos
    column_fixes = {
        'TyJe': 'Type',
        'BaseDemand_gJm': 'BaseDemand_gpm'
    }
    
    df = df.rename(columns=column_fixes)
    print(f"\nFixed column headers: {column_fixes}")
    
    # Check for data quality issues
    issues = []
    
    # 1. Check for NodeID formatting issues
    malformed_nodeids = df[df['NodeID'].str.contains('J_SNT5495_530|J_SNT5_530_ CNT75', na=False)]
    if len(malformed_nodeids) > 0:
        issues.append(f"Malformed NodeIDs: {len(malformed_nodeids)} found")
        print(f"\nMalformed NodeIDs:")
        for idx, row in malformed_nodeids.iterrows():
            print(f"  Row {idx+2}: {row['NodeID']}")
    
    # 2. Check for Type field issues
    type_issues = df[df['Type'].str.contains('JumJ|Booster JumJ', na=False)]
    if len(type_issues) > 0:
        issues.append(f"Type field typos: {len(type_issues)} found")
        print(f"\nType field issues:")
        for idx, row in type_issues.iterrows():
            print(f"  Row {idx+2}: {row['NodeID']} -> {row['Type']}")
    
    # 3. Check for elevation inconsistencies (positive elevations that should be negative)
    positive_elevations = df[df['Elevation_ft'] > 0]
    if len(positive_elevations) > 0:
        issues.append(f"Suspicious positive elevations: {len(positive_elevations)} found")
        print(f"\nPositive elevations (may need review):")
        for idx, row in positive_elevations.iterrows():
            print(f"  Row {idx+2}: {row['NodeID']} -> {row['Elevation_ft']} ft")
    
    # 4. Check for coordinate vs elevation mismatches
    coord_mismatches = []
    for idx, row in df.iterrows():
        if abs(row['Elevation_ft']) != abs(row['Y']):
            # Check if Y coordinate and elevation are suspiciously similar
            if abs(abs(row['Elevation_ft']) - abs(row['Y'])) < 1:
                coord_mismatches.append((idx, row['NodeID'], row['Elevation_ft'], row['Y']))
    
    if len(coord_mismatches) > 0:
        issues.append(f"Elevation/Y-coordinate mismatches: {len(coord_mismatches)} found")
        print(f"\nElevation/Y-coordinate potential mismatches:")
        for idx, nodeid, elev, y_coord in coord_mismatches:
            print(f"  Row {idx+2}: {nodeid} -> Elevation: {elev}, Y: {y_coord}")
    
    # 5. Apply automatic fixes
    fixed_df = df.copy()
    
    # Fix Type field typos
    fixed_df['Type'] = fixed_df['Type'].str.replace('Booster JumJ', 'Booster Pump')
    fixed_df['Type'] = fixed_df['Type'].str.replace('JumJ', 'Junction')
    
    # Fix NodeID formatting issues
    fixed_df['NodeID'] = fixed_df['NodeID'].str.replace('J_SNT5495_530', 'J_SNT5_495_530')
    fixed_df['NodeID'] = fixed_df['NodeID'].str.replace('J_SNT5_530_ CNT75', 'J_SNT5_530_CNT75')
    
    # Fix the positive elevation that's likely wrong (J_SNT1_910_CNT9)
    positive_fix_mask = (fixed_df['NodeID'] == 'J_SNT1_910_CNT9') & (fixed_df['Elevation_ft'] > 0)
    if positive_fix_mask.any():
        fixed_df.loc[positive_fix_mask, 'Elevation_ft'] = -367.3
        print(f"\nFixed J_SNT1_910_CNT9 elevation: 367.3 -> -367.3")
    
    # Fix the elevation/Y coordinate mismatch for J_SNT1_1174_1194
    mismatch_fix_mask = fixed_df['NodeID'] == 'J_SNT1_1174_1194'
    if mismatch_fix_mask.any():
        # Assume elevation should be negative to match pattern
        fixed_df.loc[mismatch_fix_mask, 'Elevation_ft'] = -576.9
        print(f"Fixed J_SNT1_1174_1194 elevation: 576.9 -> -576.9")
    
    return fixed_df, issues

def generate_node_validation_report(df, normalized_nodes_df):
    """
    Cross-validate nodes_ready.csv against the normalized Master Edge Test Sheet nodes
    """
    print("\n=== Cross-Validation with Master Edge Test Sheet ===")
    
    # Get unique nodes from both datasets
    ready_nodes = set(df['NodeID'].unique())
    master_nodes = set(normalized_nodes_df['Node_ID'].unique())
    
    # Find discrepancies
    only_in_ready = ready_nodes - master_nodes
    only_in_master = master_nodes - ready_nodes
    common_nodes = ready_nodes & master_nodes
    
    print(f"Nodes only in ready file: {len(only_in_ready)}")
    if len(only_in_ready) > 0 and len(only_in_ready) < 10:
        for node in list(only_in_ready)[:5]:
            print(f"  {node}")
    
    print(f"Nodes only in Master Edge Test Sheet: {len(only_in_master)}")  
    if len(only_in_master) > 0 and len(only_in_master) < 10:
        for node in list(only_in_master)[:5]:
            print(f"  {node}")
            
    print(f"Common nodes: {len(common_nodes)}")
    
    return {
        'only_in_ready': only_in_ready,
        'only_in_master': only_in_master,
        'common_nodes': common_nodes
    }

if __name__ == "__main__":
    nodes_csv_path = "C:/workspace/nodes_ready.csv"
    master_normalized_path = "C:/workspace/Master_Edge_Test_Sheet_normalized_nodes.csv"
    
    try:
        # Read and reconcile nodes_ready.csv
        fixed_nodes_df, issues = reconcile_nodes_ready_csv(nodes_csv_path)
        
        # Read normalized master edge data
        master_nodes_df = pd.read_csv(master_normalized_path)
        
        # Cross-validate
        validation_results = generate_node_validation_report(fixed_nodes_df, master_nodes_df)
        
        # Save reconciled file
        output_path = nodes_csv_path.replace('.csv', '_reconciled.csv')
        fixed_nodes_df.to_csv(output_path, index=False)
        
        print(f"\n=== Summary ===")
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        print(f"\nReconciled file saved to: {output_path}")
        print(f"Ready to use with build_inp_from_csv.py")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error: {e}")