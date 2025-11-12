import pandas as pd
from pathlib import Path

# --- Paths ---
base_dir = Path(__file__).resolve().parent.parent  # from Scripts_/ up to project root
input_csv = base_dir / "Data_" / "Meteorite_Landings.csv"
output_csv = base_dir / "Data_" / "geo_id_mass.csv"

# --- Load data ---
try:
    df = pd.read_csv(input_csv)
    print(f"[INFO] Loaded: {input_csv}")
except FileNotFoundError:
    raise FileNotFoundError(f"Input file not found: {input_csv}")

# --- Identify columns ---
# Expecting: 'id', 'mass (g)', 'GeoLocation'
id_col = "id"

# grab the mass column (handles 'mass (g)' or similar)
mass_col = None
for c in df.columns:
    if c.lower().startswith("mass"):
        mass_col = c
        break

# grab geolocation column
geo_col = None
for c in df.columns:
    if "geolocation" in c.lower():
        geo_col = c
        break

missing = [name for name, col in [("id", id_col), ("mass", mass_col), ("GeoLocation", geo_col)] if col is None]
if missing:
    raise ValueError(f"Missing expected column(s): {', '.join(missing)}")

# --- Build filtered DataFrame ---
out = df[[id_col, mass_col, geo_col]].copy()
out.columns = ["id", "mass", "GeoLocation"]  # normalize column names

# --- Save ---
out.to_csv(output_csv, index=False)
print(f"[SUCCESS] Wrote {len(out)} rows to: {output_csv}")
