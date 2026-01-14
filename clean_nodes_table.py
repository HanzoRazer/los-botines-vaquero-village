import pandas as pd
import sys

# Change this path if needed
NODES_CSV = 'nodes.csv'
CLEANED_CSV = 'nodes_cleaned.csv'
REPORT = 'nodes_duplicates_report.txt'

def main():
    df = pd.read_csv(NODES_CSV, dtype=str)
    df['NodeID'] = df['NodeID'].astype(str).str.strip()
    
    # Find duplicates (case-insensitive, ignore whitespace)
    norm_ids = df['NodeID'].str.lower().str.strip()
    duplicates = df[norm_ids.duplicated(keep=False)]
    
    if not duplicates.empty:
        with open(REPORT, 'w', encoding='utf-8') as f:
            f.write('DUPLICATE NodeIDs FOUND:\n')
            for nodeid in duplicates['NodeID'].unique():
                f.write(f'{nodeid}\n')
        print(f"Duplicates found. See {REPORT} for details.")
    else:
        print("No duplicates found.")
        with open(REPORT, 'w', encoding='utf-8') as f:
            f.write('No duplicates found.')
    
    # Drop all but the first occurrence of each NodeID (case-insensitive, ignore whitespace)
    df_clean = df[~norm_ids.duplicated(keep='first')]
    df_clean.to_csv(CLEANED_CSV, index=False)
    print(f"Cleaned file written to {CLEANED_CSV}")

if __name__ == '__main__':
    main()
