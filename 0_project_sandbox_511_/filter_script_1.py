#!/usr/bin/env python
"""
Generate filter_1.csv and a 3-panel plot from Meteorite_Landings.csv

Steps:
1. Read Meteorite_Landings.csv (same directory as this script).
2. Filter rows to keep only years between 1800 and 2013 (inclusive).
3. Drop duplicate rows.
4. Aggregate by year -> count number of falls per year.
5. Save aggregated data to filter_1.csv with columns [year, aggregate_falls].
6. Plot three panels:
   - Scatter Plot (year vs aggregate_falls)
   - Box Plot (distribution of aggregate_falls)
   - Frequency Histogram (distribution of aggregate_falls)
"""

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    # ------------------------------------------------------------------
    # 1. Paths (assume input/output in same directory as this script)
    # ------------------------------------------------------------------
    base_dir = Path(__file__).resolve().parent
    input_csv = base_dir / "Meteorite_Landings.csv"
    output_csv = base_dir / "filter_1.csv"

    # ------------------------------------------------------------------
    # 2. Read data
    # ------------------------------------------------------------------
    df = pd.read_csv(input_csv)

    # ------------------------------------------------------------------
    # 3. Clean + filter by year
    #    - Drop rows with missing year
    #    - Keep only 1800 <= year <= 2013
    #    - Convert year to integer (some datasets store year as float)
    # ------------------------------------------------------------------
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    df = df[(df["year"] >= 1800) & (df["year"] <= 2013)]

    # ------------------------------------------------------------------
    # 4. Remove duplicate rows across all columns
    # ------------------------------------------------------------------
    df = df.drop_duplicates()

    # ------------------------------------------------------------------
    # 5. Aggregate by year
    # ------------------------------------------------------------------
    agg = (
        df.groupby("year")
        .size()
        .reset_index(name="aggregate_falls")
        .sort_values("year")
    )

    # ------------------------------------------------------------------
    # 6. Save aggregated data to filter_1.csv
    # ------------------------------------------------------------------
    agg.to_csv(output_csv, index=False)
    print(f"Saved aggregated data to: {output_csv}")

    # ------------------------------------------------------------------
    # 7. Create 3-panel plot with descriptive titles
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # Shared description appended to each title
    filter_desc = (
        "Filtered years: 1800–2013\n"
        "Duplicates removed · Aggregated by year\n"
        "(count of meteorite falls)"
    )

    # --- Left: Scatter Plot ---
    axes[0].scatter(agg["year"], agg["aggregate_falls"], s=18)
    axes[0].set_title(
        r"$\bf{Scatter\ Plot}$" + ": Meteorite Falls per Year (After Filtering)\n" + filter_desc,
        fontsize=10
    )
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Aggregated Meteorite Falls")

    # --- Middle: Box Plot ---
    axes[1].boxplot(agg["aggregate_falls"], vert=True)
    axes[1].set_title(
        r"$\bf{Box\ Plot}$" + ": Distribution of Aggregated Yearly Falls\n" + filter_desc,
        fontsize=10
    )
    axes[1].set_xticks([1])
    axes[1].set_xticklabels(["aggregate_falls"])
    axes[1].set_ylabel("Number of Falls per Year")

    # --- Right: Frequency Histogram ---
    axes[2].hist(agg["aggregate_falls"], bins="auto", edgecolor="black")
    axes[2].set_title(
        r"$\bf{Frequency\ Histogram}$" + ": Yearly Meteorite Fall Totals\n" + filter_desc,
        fontsize=10
    )
    axes[2].set_xlabel("Falls per Year")
    axes[2].set_ylabel("Number of Years")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
