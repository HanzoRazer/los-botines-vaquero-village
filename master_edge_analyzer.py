import pandas as pd
import numpy as np

def fix_column_aa_corrections(csv_file_path):
    """
    Find and report Column AA correction issues in Master Edge Test Sheet
    """
    df = pd.read_csv(csv_file_path)
    
    # Column AA is typically the 27th column (index 26)
    if len(df.columns) <= 26:
        print("Warning: CSV doesn't have enough columns for Column AA")
        return df
    
    col_aa = df.iloc[:, 26]  # Column AA
    
    # Find rows that need correction
    correction_mask = (
        col_aa.astype(str).str.contains('correction|error|fix|problem|issue', case=False, na=False) |
        col_aa.astype(str).str.contains('need|check|verify', case=False, na=False)
    )
    
    problem_rows = df[correction_mask].copy()
    
    print("=== Column AA Correction Analysis ===")
    print(f"Total rows needing correction: {len(problem_rows)}")
    
    if len(problem_rows) > 0:
        print("\nProblem rows details:")
        for idx, row in problem_rows.iterrows():
            print(f"Row {idx+2} (Excel): {row.iloc[26]}")  # +2 for header and 0-based indexing
            # Show first few columns for context
            print(f"  Context: {row.iloc[0]} -> {row.iloc[1]} -> {row.iloc[2]}")
            print()
    
    return problem_rows

def extract_normalized_nodes(csv_file_path):
    """
    Extract unique nodes from first column to create normalized node sheet
    """
    df = pd.read_csv(csv_file_path)
    
    # Get unique values from first column (should be node IDs)
    first_col_name = df.columns[0]
    unique_nodes = df[first_col_name].dropna().unique()
    
    # Create normalized node list
    normalized_df = pd.DataFrame({
        'Node_ID': unique_nodes,
        'Node_Type': '',  # To be filled based on connections
        'Connections': '',  # To be filled with connected components
        'Is_Junction': False,
        'Is_Endpoint': False
    })
    
    # Analyze node connections to determine type
    for node in unique_nodes:
        # Count how many times this node appears (indicates connections)
        connections = len(df[df[first_col_name] == node])
        
        normalized_df.loc[normalized_df['Node_ID'] == node, 'Connections'] = connections
        
        if connections == 1:
            normalized_df.loc[normalized_df['Node_ID'] == node, 'Is_Endpoint'] = True
            normalized_df.loc[normalized_df['Node_ID'] == node, 'Node_Type'] = 'Endpoint'
        elif connections > 2:
            normalized_df.loc[normalized_df['Node_ID'] == node, 'Is_Junction'] = True
            normalized_df.loc[normalized_df['Node_ID'] == node, 'Node_Type'] = 'Junction'
        else:
            normalized_df.loc[normalized_df['Node_ID'] == node, 'Node_Type'] = 'Intermediate'
    
    return normalized_df

def analyze_valve_tee_trunk_sequence(csv_file_path):
    """
    Find valve->tee->trunk->tee->split_trunk->valve patterns
    """
    df = pd.read_csv(csv_file_path)
    
    print("=== Valve-Tee-Trunk Pattern Analysis ===")
    
    # Look for component type indicators in the data
    # You'll need to adjust these based on your actual column structure
    
    # Common columns that might indicate component types:
    component_cols = [col for col in df.columns if any(keyword in col.lower() 
                     for keyword in ['type', 'component', 'fitting', 'pipe'])]
    
    print(f"Potential component type columns: {component_cols}")
    
    # Look for sequences in your data
    sequences = []
    
    for i in range(len(df) - 5):  # Need at least 6 rows for your pattern
        window = df.iloc[i:i+6]
        
        # Check if this could be your valve->tee->trunk->tee->trunk->valve pattern
        # This is a template - you'll need to customize based on your data structure
        
        pattern_match = {
            'start_row': i + 2,  # Excel row number
            'sequence': window[df.columns[0]].tolist(),  # Node sequence
            'pattern_type': 'potential_valve_tee_trunk'
        }
        
        sequences.append(pattern_match)
    
    # Show first few sequences for analysis
    print(f"\nFirst 5 sequences found:")
    for seq in sequences[:5]:
        print(f"Row {seq['start_row']}: {' -> '.join(map(str, seq['sequence']))}")
    
    return sequences

if __name__ == "__main__":
    csv_path = r"c:\Users\thepr\OneDrive\Master Edge Test Sheet.csv"
    
    print("Starting Master Edge Test Sheet analysis...")
    print(f"File: {csv_path}")
    print("=" * 60)
    
    try:
        # 1. Check Column AA corrections
        problem_rows = fix_column_aa_corrections(csv_path)
        
        print("\n" + "=" * 60)
        
        # 2. Extract normalized nodes
        normalized_nodes = extract_normalized_nodes(csv_path)
        print("=== Normalized Node List ===")
        print(f"Total unique nodes: {len(normalized_nodes)}")
        print(f"Endpoints: {len(normalized_nodes[normalized_nodes['Is_Endpoint']])}")
        print(f"Junctions: {len(normalized_nodes[normalized_nodes['Is_Junction']])}")
        
        # Save normalized nodes
        output_file = csv_path.replace('.csv', '_normalized_nodes.csv')
        normalized_nodes.to_csv(output_file, index=False)
        print(f"Normalized nodes saved to: {output_file}")
        
        print("\n" + "=" * 60)
        
        # 3. Analyze valve-tee-trunk patterns
        sequences = analyze_valve_tee_trunk_sequence(csv_path)
        
        print(f"\nAnalysis complete!")
        print(f"- Found {len(problem_rows)} rows needing correction in Column AA")
        print(f"- Extracted {len(normalized_nodes)} unique nodes")
        print(f"- Identified {len(sequences)} potential sequences")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
    except Exception as e:
        print(f"Error: {e}")