import pandas as pd
from pathlib import Path

# --- Define paths ---
base_dir = Path(__file__).resolve().parent.parent  # goes up from Scripts_/
input_csv = base_dir / "Data_" / "Meteorite_Landings.csv"
output_csv = base_dir / "Data_" / "filter_round_1.csv"

# --- Load data ---
try:
    df = pd.read_csv(input_csv)
    print(f"[INFO] Loaded: {input_csv}")
except FileNotFoundError:
    raise FileNotFoundError(f"Input file not found: {input_csv}")

# --- Check available columns ---
print(f"[INFO] Columns found: {list(df.columns)}")

# --- Keep only 'id' and 'year' ---
keep_cols = [col for col in df.columns if col.lower() in ("id", "year")]
if not keep_cols:
    raise ValueError("Neither 'id' nor 'year' columns found in CSV.")

filtered_df = df[keep_cols]
print(f"[INFO] Keeping columns: {keep_cols}")

# --- Save result ---
filtered_df.to_csv(output_csv, index=False)
print(f"[SUCCESS] Filtered CSV written to: {output_csv}")
