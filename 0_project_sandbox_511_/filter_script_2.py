#!/usr/bin/env python
"""
Generate filter_2.csv and a 3-panel plot from Meteorite_Landings.csv

Steps:
1. Read Meteorite_Landings.csv (same directory as this script).
2. Filter rows to keep only years between 1800 and 2013 (inclusive).
3. Drop duplicate rows.
4. Aggregate by year -> count number of meteorite falls per year.
5. Apply IQR outlier reduction on aggregated_falls.
6. Save cleaned data to filter_2.csv with columns [year, aggregate_falls].
7. Plot:
   - Left: scatter (year vs aggregate_falls)
   - Middle: boxplot of aggregate_falls
   - Right: histogram of aggregate_falls (frequency distribution)
   - Each graph annotated with n, min, max
   - Scatter plot includes vertical lines for min/max year
"""

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    # ------------------------------------------------------------------
    # 1. Paths (input/output in same directory as this script)
    # ------------------------------------------------------------------
    base_dir = Path(__file__).resolve().parent
    input_csv = base_dir / "Meteorite_Landings.csv"
    output_csv = base_dir / "filter_2.csv"

    # ------------------------------------------------------------------
    # 2. Read data
    # ------------------------------------------------------------------
    df = pd.read_csv(input_csv)

    # ------------------------------------------------------------------
    # 3. Clean + filter by year
    # ------------------------------------------------------------------
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= 1800) & (df["year"] <= 2013)]

    # ------------------------------------------------------------------
    # 4. Remove duplicate rows (across all columns)
    # ------------------------------------------------------------------
    df = df.drop_duplicates()

    # ------------------------------------------------------------------
    # 5. Aggregate into yearly bins:
    #    aggregate_falls = number of records per year
    # ------------------------------------------------------------------
    agg = (
        df.groupby("year")
        .size()
        .reset_index(name="aggregate_falls")
        .sort_values("year")
    )

    # ------------------------------------------------------------------
    # 6. Apply IQR outlier reduction to aggregate_falls
    # ------------------------------------------------------------------
    Q1 = agg["aggregate_falls"].quantile(0.25)
    Q3 = agg["aggregate_falls"].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    agg_iqr = agg[(agg["aggregate_falls"] >= lower_bound) &
                  (agg["aggregate_falls"] <= upper_bound)]

    print(f"IQR bounds: lower={lower_bound}, upper={upper_bound}")
    print(f"Records before IQR: {len(agg)}")
    print(f"Records after IQR:  {len(agg_iqr)}")

    # ------------------------------------------------------------------
    # 7. Save filtered data
    # ------------------------------------------------------------------
    agg_iqr.to_csv(output_csv, index=False)
    print(f"Saved IQR-filtered aggregated data to: {output_csv}")

    # ------------------------------------------------------------------
    # 8. Plot 3-panel figure
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # Shared text for all graph titles
    filter_desc = (
        "Filtered years: 1800–2013\nDuplicates removed\n"
        "IQR outlier reduction applied\nAggregated by year (count of falls)"
    )

    # Shared annotation values
    n_points = len(agg_iqr)
    min_val = agg_iqr["aggregate_falls"].min()
    max_val = agg_iqr["aggregate_falls"].max()

    # Min/max YEAR for scatter-specific annotations
    min_year = agg_iqr["year"].min()
    max_year = agg_iqr["year"].max()

    annotation_text = (
        f"n = {n_points}\n"
        f"min = {min_val}\n"
        f"max = {max_val}"
    )

    # ==================================================================
    # 1. SCATTER PLOT
    # ==================================================================
    axes[0].scatter(agg_iqr["year"], agg_iqr["aggregate_falls"], s=22)
    axes[0].set_title(
        r"$\bf{Scatter\ Plot}$"
        + ": Meteorite Falls per Year (IQR-Filtered)\n" + filter_desc,
        fontsize=10
    )
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Aggregated Meteorite Falls")

    # annotation box
    axes[0].annotate(
        annotation_text,
        xy=(0.1, 0.95),
        xycoords="axes fraction",
        fontsize=10,
        fontweight="bold",
        color="black",
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.6)
    )

    # min year line
    axes[0].axvline(min_year, color="red", linestyle="--", linewidth=1.4, alpha=0.85)
    axes[0].annotate(
        f"min year = {min_year}",
        xy=(min_year, max_val),
        xytext=(min_year, max_val + (max_val * 0.08)),
        textcoords="data",
        ha="center",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.7)
    )

    # max year line
    axes[0].axvline(max_year, color="red", linestyle="--", linewidth=1.4, alpha=0.85)
    axes[0].annotate(
        f"max year = {max_year}",
        xy=(max_year, max_val),
        xytext=(max_year, max_val + (max_val * 0.08)),
        textcoords="data",
        ha="center",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.7)
    )

    # ==================================================================
    # 2. BOX PLOT
    # ==================================================================
    axes[1].boxplot(agg_iqr["aggregate_falls"], vert=True)
    axes[1].set_title(
        r"$\bf{Box\ Plot}$"
        + ": Distribution of Aggregated Yearly Falls\n" + filter_desc,
        fontsize=10
    )
    axes[1].set_xticks([1])
    axes[1].set_xticklabels(["aggregate_falls"])
    axes[1].set_ylabel("Number of Falls per Year")

    axes[1].annotate(
        annotation_text,
        xy=(0.1, 0.95),
        xycoords="axes fraction",
        fontsize=10,
        fontweight="bold",
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.6)
    )

    # ==================================================================
    # 3. HISTOGRAM
    # ==================================================================
    axes[2].hist(agg_iqr["aggregate_falls"], bins="auto", edgecolor="black")
    axes[2].set_title(
        r"$\bf{Frequency\ Histogram}$"
        + ": Yearly Meteorite Fall Totals\n" + filter_desc,
        fontsize=10
    )
    axes[2].set_xlabel("Falls per Year")
    axes[2].set_ylabel("Number of Years")

    axes[2].annotate(
        annotation_text,
        xy=(0.2, 0.95),
        xycoords="axes fraction",
        fontsize=10,
        fontweight="bold",
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.6)
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
