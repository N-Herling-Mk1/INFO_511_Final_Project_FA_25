#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_kurtosis_skew_analysis_table.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science.

Goal
----
Summarize the skewness / kurtosis analysis and candidate transforms
(from EDA Phase 3 Normality Check) into a styled HTML table.

Based on program output:

  Note: For a perfectly Normal distribution, skewness ≈ 0 and
        kurtosis ≈ 3 (mesokurtic), per INFO 511 Lecture 4.

  === Candidate Transforms: Skewness & Kurtosis ===
  Score = |skew| + |kurtosis - 3|  (lower is closer to Normal)
  - sqrt    : skew =   0.5761, kurtosis =   2.5769, score =   0.9991
  - cuberoot: skew =   0.2880, kurtosis =   2.0930, score =   1.1950
  - log1p   : skew =   0.0076, kurtosis =   1.7394, score =   1.2682
  - boxcox  : skew =  -0.0550, kurtosis =   1.7588, score =   1.2962 (lambda ≈ 0.105)
  - identity: skew =   1.5610, kurtosis =   5.5396, score =   4.1006

  Recommended transform:
    'sqrt' — skew ≈ 0.5761, kurtosis ≈ 2.5769, closest to Normal (skew≈0, kurtosis≈3).
"""

from pathlib import Path

# Output HTML filename (current directory)
OUTPUT_HTML = Path("py_kurtosis_skew_analysis_table.html")


def main():
    # Ensure parent directory exists (typically ".")
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    # ---- Data: hard-coded from program output ----
    # transform, skew, kurtosis, score, notes
    rows = [
        {
            "name": "sqrt",
            "skew": 0.5761,
            "kurtosis": 2.5769,
            "score": 0.9991,
            "notes": "Recommended transform (gentle for count data).",
        },
        {
            "name": "cuberoot",
            "skew": 0.2880,
            "kurtosis": 2.0930,
            "score": 1.1950,
            "notes": "Reduces skew; tails slightly lighter than Normal.",
        },
        {
            "name": "log1p",
            "skew": 0.0076,
            "kurtosis": 1.7394,
            "score": 1.2682,
            "notes": "Strong skew reduction; tails noticeably light.",
        },
        {
            "name": "boxcox",
            "skew": -0.0550,
            "kurtosis": 1.7588,
            "score": 1.2962,
            "notes": "Box–Cox (λ ≈ 0.105); similar to log, light tails.",
        },
        {
            "name": "identity",
            "skew": 1.5610,
            "kurtosis": 5.5396,
            "score": 4.1006,
            "notes": "Original shape; strongly right-skewed, heavy tails.",
        },
    ]

    # Build HTML rows
    body_rows_html = []
    for r in rows:
        # Bold the recommended transform (sqrt)
        if r["name"] == "sqrt":
            name_cell = f"<strong>{r['name']}</strong>"
        else:
            name_cell = r["name"]

        row_html = f"""
      <tr>
        <td>{name_cell}</td>
        <td>{r['skew']:.4f}</td>
        <td>{r['kurtosis']:.4f}</td>
        <td>{r['score']:.4f}</td>
        <td>{r['notes']}</td>
      </tr>
        """
        body_rows_html.append(row_html)

    body_html = "\n".join(body_rows_html)

    # ---- Full HTML document ----
    html_output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Meteorite Landings — Skewness & Kurtosis Transform Summary</title>
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
      font-size: 16px;
      max-width: 98%;
    }}
    .table-wrapper {{
      margin-top: 8px;
      border: 4px solid #000000;   /* solid BLACK outer border */
      border-radius: 10px;
      padding: 0;
      overflow: hidden;            /* keeps rounded corners clean */
    }}
    .eda-table {{
      width: 100%;
      border-collapse: collapse;
      background: #f5f4e8;         /* beige background for main table body */
    }}
    .eda-table th {{
      background: #4ade80;         /* green header */
      color: black;
      font-weight: bold;
      padding: 10px;
      border-bottom: 2px solid black;
      border-right: 1px solid black;
      text-align: center;
    }}
    .eda-table th:last-child {{
      border-right: none;
    }}
    .eda-table td {{
      padding: 8px;
      border-bottom: 1px solid black;
      border-right: 1px solid black;
      text-align: center;
      font-size: 14px;
    }}
    .eda-table tr:last-child td {{
      border-bottom: none;
    }}
    .eda-table td:last-child {{
      border-right: none;
      text-align: center;  /* center Notes column as well */
      padding-left: 0;
    }}
    code {{
      font-family: "Courier New", monospace;
      font-size: 13px;
    }}
  </style>
</head>
<body>

  <h2>Table 3. Skewness &amp; Kurtosis Transform Summary</h2>

  <div class="table-wrapper">
    <table class="eda-table">
      <tr>
        <th>Transform</th>
        <th>Skewness</th>
        <th>Kurtosis<br>(fisher=False)</th>
        <th>Score<br><span style="font-size:12px;">|skew| + |kurtosis − 3|</span></th>
        <th>Notes</th>
      </tr>
{body_html}
    </table>
  </div>

  <p class="subtitle">
    <b>Table 3.</b> Note. For a perfectly Normal distribution, skewness ≈ 0 and kurtosis ≈ 3
    (mesokurtic), per INFO 511 Lecture 4. The score
    <code>|skew| + |kurtosis − 3|</code> is a simple heuristic: smaller values
    indicate a distribution closer to Normal in both asymmetry and tailedness.
    The square-root transform (<code>sqrt</code>) provides the best balance for
    these meteorite yearly counts (moderate skew reduction and kurtosis near 3),
    and is therefore recommended as the primary Normality-oriented transform.
  </p>

</body>
</html>
"""

    # Write to disk
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ Skewness / kurtosis summary table written to:\n  {OUTPUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
