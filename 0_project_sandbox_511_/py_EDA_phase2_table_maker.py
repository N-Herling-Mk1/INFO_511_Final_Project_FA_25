#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_EDA_phase2_table_maker.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science.

Goal
----
Read the refactored meteorite dataset:

    imputating_filter1_Tx.csv

with columns:
    year, num_fell_found

Compute summary statistics for the yearly counts (num_fell_found):

    - Total count (N)
    - Mean
    - Minimum
    - 25% quantile (Q1)
    - 50% quantile (Median)
    - 75% quantile (Q3)
    - Maximum
    - Standard Deviation (sample, ddof=1)
    - % of data within the IQR (Q1 to Q3 inclusive)
    - Number of outliers under Tukey's rule
      (values < Q1 - 1.5*IQR or > Q3 + 1.5*IQR)

Then write a styled HTML table (same visual style as table_1_html_code.py)
to:

    EDA_phase2_table.html

No command line arguments needed.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ================================
# 1. Paths (hard-coded, current dir)
# ================================
INPUT_CSV = Path("imputating_filter1_Tx.csv")
OUTPUT_HTML = Path("EDA_phase2_table.html")


def main():
    # Ensure output directory exists (typically ".")
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    # ================================
    # 2. Load Dataset
    # ================================
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found:\n  {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    if "num_fell_found" not in df.columns:
        raise ValueError(
            "Expected column 'num_fell_found' in input CSV.\n"
            f"Columns found: {list(df.columns)}"
        )

    # Clean / coerce numeric
    counts = pd.to_numeric(df["num_fell_found"], errors="coerce")
    counts = counts.dropna()
    counts = counts.astype(float)

    if counts.empty:
        raise ValueError("No valid numeric values in 'num_fell_found' column.")

    # ================================
    # 3. Summary Statistics
    # ================================
    n = counts.size
    mean_val = counts.mean()
    min_val = counts.min()
    max_val = counts.max()
    std_val = counts.std(ddof=1)  # sample standard deviation

    # Quartiles and median
    q1 = np.percentile(counts, 25)
    median_val = np.percentile(counts, 50)
    q3 = np.percentile(counts, 75)
    iqr = q3 - q1

    # % of data between Q1 and Q3 (inclusive)
    mask_iqr = (counts >= q1) & (counts <= q3)
    pct_in_iqr = mask_iqr.mean() * 100.0

    # Tukey outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    mask_outliers = (counts < lower_bound) | (counts > upper_bound)
    n_outliers = int(mask_outliers.sum())

    # Format numbers for table
    fmt_n = f"{n:d}"
    fmt_mean = f"{mean_val:,.2f}"
    fmt_min = f"{min_val:,.0f}"
    fmt_q1 = f"{q1:,.2f}"
    fmt_median = f"{median_val:,.2f}"
    fmt_q3 = f"{q3:,.2f}"
    fmt_max = f"{max_val:,.0f}"
    fmt_std = f"{std_val:,.2f}"
    fmt_pct_iqr = f"{pct_in_iqr:,.2f}%"
    fmt_n_out = f"{n_outliers:d}"

    # ================================
    # 4. Build HTML Row
    # ================================
    row_html = f"""
    <tr>
      <td>num_fell_found</td>
      <td>{fmt_n}</td>
      <td>{fmt_mean}</td>
      <td>{fmt_std}</td>
      <td>{fmt_min}</td>
      <td>{fmt_q1}</td>
      <td>{fmt_median}</td>
      <td>{fmt_q3}</td>
      <td>{fmt_max}</td>
      <td>{fmt_pct_iqr}</td>
      <td>{fmt_n_out}</td>
    </tr>
    """

    # ================================
    # 5. Compose the Full HTML
    #    (styling copied from table_1_html_code.py)
    # ================================
    html_output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Meteorite Landings — EDA Phase 2 Summary</title>
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

      /* Outer border: thickness + color */
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

  <h2>Table 2. EDA Phase 2 — Yearly Count Summary</h2>

  <div class="table-wrapper">
    <table class="eda-table">
      <tr>
        <th>Feature</th>
        <th>Total count (N)</th>
        <th>Mean</th>
        <th>Std. Dev.</th>
        <th>Min</th>
        <th>25% (Q1)</th>
        <th>50% (Median)</th>
        <th>75% (Q3)</th>
        <th>Max</th>
        <th>% of data within IQR</th>
        <th># of Tukey outliers</th>
      </tr>
      {row_html}
    </table>
  </div>

  <p class="subtitle">
    Table 2. Summary statistics for yearly meteorite counts
    (<code>num_fell_found</code>) after initial filtering, aggregation,
    and EDA Phase 2 transformations. Quartiles (25%, 50%, 75%) correspond
    to the empirical distribution of yearly counts. The IQR-based outlier
    definition uses Tukey's rule: values below
    Q1&nbsp;&minus;&nbsp;1.5&nbsp;&times;&nbsp;IQR or above
    Q3&nbsp;&plus;&nbsp;1.5&nbsp;&times;&nbsp;IQR are flagged as outliers.
    Total count (N) is the number of distinct years in the refactored dataset.
  </p>

</body>
</html>
"""

    # ================================
    # 6. Write HTML to Disk
    # ================================
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ EDA Phase 2 table written to:\n  {OUTPUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
