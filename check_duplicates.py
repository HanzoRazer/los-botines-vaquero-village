import pandas as pd
import os

# File path
file_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Master_Edge_Test_Sheet.csv"

# Load the CSV
df = pd.read_csv(file_path, encoding='latin-1')

print("Analyzing columns A, B, C, D for duplicates...")
print(f"Total rows: {len(df)}")

# Get column names for A, B, C, D (index 0, 1, 2, 3)
col_a = df.columns[0]  # Column A
col_b = df.columns[1]  # Column B
col_c = df.columns[2]  # Column C
col_d = df.columns[3]  # Column D

print(f"\nColumns being checked:")
print(f"  A: {col_a}")
print(f"  B: {col_b}")
print(f"  C: {col_c}")
print(f"  D: {col_d}")

# Create duplicate detection column (like the Excel formula)
# The formula checks if A|B|C|D or B|A|C|D appears more than once
def check_duplicate(row, df_all):
    a = str(row[col_a])
    b = str(row[col_b])
    c = str(row[col_c])
    d = str(row[col_d])
    
    # Create forward and reverse keys
    key_forward = f"{a}|{b}|{c}|{d}"
    key_reverse = f"{b}|{a}|{c}|{d}"
    
    # Count occurrences (excluding current row)
    count = 0
    for idx, check_row in df_all.iterrows():
        if idx == row.name:
            continue
        check_a = str(check_row[col_a])
        check_b = str(check_row[col_b])
        check_c = str(check_row[col_c])
        check_d = str(check_row[col_d])
        
        check_key = f"{check_a}|{check_b}|{check_c}|{check_d}"
        if check_key == key_forward or check_key == key_reverse:
            count += 1
    
    return "DUP_ROW" if count > 0 else ""

# Apply duplicate check to each row
print("\nChecking for duplicates (this may take a moment)...")
df['DUP_CHECK'] = df.apply(lambda row: check_duplicate(row, df), axis=1)

# Count duplicates found
dup_count = (df['DUP_CHECK'] == 'DUP_ROW').sum()
print(f"\nDuplicate rows found: {dup_count}")

if dup_count > 0:
    print("\nDuplicate rows:")
    print(df[df['DUP_CHECK'] == 'DUP_ROW'][[col_a, col_b, col_c, col_d, 'DUP_CHECK']])

# Save result to new CSV with duplicate check in column M
output_path = r"C:\Users\thepr\Downloads\Los Botines Vaquero Village\EPANET\WT8\Output\Master_Edge_Test_Sheet_with_duplicates.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Insert the duplicate check column at position M (index 12, which is column M in Excel)
# First, get all columns before M
cols = df.columns.tolist()
dup_col = cols.pop()  # Remove DUP_CHECK from end
cols.insert(12, dup_col)  # Insert at position M (index 12)
df = df[cols]

df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nOutput saved to: {output_path}")
print("The DUP_CHECK column has been inserted at column M")
