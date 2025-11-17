#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_eda_table.py

Reads Meteorite_Landings.csv from the current directory and writes a styled
HTML EDA table to:
  EDA_table_1.html

No command line arguments needed.
"""

from pathlib import Path
import pandas as pd

# ================================
# 1. Paths (hard-coded, current dir)
# ================================
INPUT_CSV = Path("Meteorite_Landings.csv")
OUTPUT_HTML = Path("EDA_table_1.html")


def main():
    # Ensure output directory exists (typically ".")
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    # ================================
    # 2. Load Your Dataset
    # ================================
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found:\n  {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    # ================================
    # 3. Descriptions from NASA Catalog
    # ================================
    descriptions = {
        "name": "Name of the meteorite as recorded in the catalog.",
        "id": "Unique numeric identifier assigned to each meteorite record.",
        "nametype": "Indicates valid meteorite names ('Valid') or paired/duplicate names ('Relict').",
        "recclass": "Classification based on chemical and petrological type.",
        "mass (g)": "Reported mass of the meteorite in grams.",
        "fall": "Indicates whether the meteorite was 'Fell' (observed fall) or 'Found'.",
        "year": "Year the meteorite was found or fell.",
        "reclat": "Latitude of the recovery site.",
        "reclong": "Longitude of the recovery site.",
        "GeoLocation": "Coordinate pair representing the recovery location (latitude, longitude).",
    }

    # ================================
    # 4. Helpers: Column Classification
    # ================================
    def classify_col(col: pd.Series) -> str:
        if pd.api.types.is_numeric_dtype(col):
            return "Numerical"
        if pd.api.types.is_datetime64_any_dtype(col):
            return "Numerical"
        return "Categorical"

    # Convert 'year' to datetime if possible
    if "year" in df.columns:
        try:
            df["year"] = pd.to_datetime(df["year"], errors="coerce")
        except Exception:
            pass

    # ================================
    # 5. Build the Table Rows
    # ================================
    rows = []
    for col in df.columns:
        series = df[col]
        dtype = str(series.dtype)
        cat_num = classify_col(series)
        nunique = series.nunique(dropna=True)
        pmiss = series.isna().mean() * 100.0
        desc = descriptions.get(col, "No description available.")

        rows.append(f"""
    <tr>
      <td>{col}</td>
      <td>{dtype}</td>
      <td>{cat_num}</td>
      <td>{nunique}</td>
      <td>{pmiss:.2f}%</td>
      <td>{desc}</td>
    </tr>
    """)

    rows_html = "\n".join(rows)

    # ================================
    # 6. Compose the Full HTML
    # ================================
    html_output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Meteorite Landings — EDA Table</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #ffffff;
      margin: 24px;
    }}
    h2 {{
      text-align: center;
      margin-bottom: 6px;
    }}
    p.subtitle {{
      text-align: left;
      margin-top: 16px;
      margin-bottom: 0;
      font-size: 14px;
      max-width: 98%;
    }}
    .table-wrapper {{
      margin-top: 8px;

      /* >>> OUTER BORDER: thickness + color
         Change 4px (thickness) or #000000 (color) to adjust the look.
      */
      border: 4px solid #000000;   /* solid BLACK outer border */
      border-radius: 10px;
      padding: 0;
      overflow: hidden;            /* keeps rounded corners clean */
    }}
    .eda-table {{
      width: 100%;
      border-collapse: collapse;   /* ensures borders touch cleanly */
      background: #f5f4e8;         /* beige background for main table body */
    }}
    .eda-table th {{
      background: #4ade80;         /* green header */
      color: black;
      font-weight: bold;
      padding: 10px;
      border-bottom: 2px solid black;
      border-right: 1px solid black; /* vertical line between header columns */
      text-align: center;
    }}
    .eda-table th:last-child {{
      border-right: none;
    }}
    .eda-table td {{
      padding: 8px;
      border-bottom: 1px solid black;  /* horizontal row lines */
      border-right: 1px solid black;   /* vertical column lines */
      text-align: center;
    }}
    .eda-table tr:last-child td {{
      border-bottom: none;
    }}
    .eda-table td:last-child {{
      border-right: none;
    }}
  </style>
</head>
<body>

  <h2>Table 1. Initial EDA Exploration</h2>

  <div class="table-wrapper">
    <table class="eda-table">
      <tr>
        <th>Feature Name</th>
        <th>Pandas dtype</th>
        <th>Categorical / Numerical</th>
        <th># Unique</th>
        <th>% Missing</th>
        <th>Description</th>
      </tr>
      {rows_html}
    </table>
  </div>

  <p class="subtitle">
    Table 1. Summary of the primary features in the NASA Meteorite Landings dataset,
    including pandas data types, inferred feature type, cardinality, missingness,
    and brief semantic descriptions used for subsequent exploratory analysis.
  </p>

</body>
</html>
"""

    # ================================
    # 7. Write HTML to Disk
    # ================================
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ EDA table written to:\n  {OUTPUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
