#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_EDA_phase3_Outlier_Removal.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science.

Goal
----
Read the EDA Phase 2 refactored meteorite dataset:

    imputating_filter1_Tx.csv

with columns:
    year, num_fell_found

Apply Tukey-style outlier removal on the yearly counts (num_fell_found):

    - Compute Q1 (25%), Q3 (75%), and IQR = Q3 - Q1
    - Define lower bound: Q1 - 1.5 * IQR
    - Define upper bound: Q3 + 1.5 * IQR
    - Remove any rows with num_fell_found < lower bound
                         or num_fell_found > upper bound

Write the filtered dataset to:

    outlier_filter_2.csv

Additionally, generate boxplot figures:

    Graph 7: Boxplot of num_fell_found (unfiltered, original EDA Phase 2 data) - EDA_phase3_boxplot_unfiltered.png
    Graph 8: Boxplot of num_fell_found (after Tukey outlier removal, EDA Phase 3) - EDA_phase3_boxplot_filtered.png

Each graph includes a caption below explaining the visualization.

No command line arguments needed.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================================
# 1. Paths (hard-coded, current dir)
# ================================
INPUT_CSV = Path("imputating_filter1_Tx.csv")
OUTPUT_CSV = Path("outlier_filter_2.csv")

OUTPUT_BOX_UNFILTERED = Path("EDA_phase3_boxplot_unfiltered.png")
OUTPUT_BOX_FILTERED = Path("EDA_phase3_boxplot_filtered.png")


def plot_box_unfiltered(df: pd.DataFrame, output_path: Path):
    """
    Graph 7: Boxplot of num_fell_found for the unfiltered (original) EDA Phase 2 data.
    """
    values = df["num_fell_found"].astype(float).values

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()

    ax.boxplot(values, vert=True, patch_artist=True,
               boxprops=dict(facecolor="lightblue", color="black"),
               medianprops=dict(color="red"),
               whiskerprops=dict(color="black"),
               capprops=dict(color="black"),
               flierprops=dict(marker="o", markersize=4, markerfacecolor="gray",
                               markeredgecolor="black"))

    ax.set_title("EDA Phase 2\nYearly Meteorite Counts (Unfiltered)", fontsize=14)
    ax.set_ylabel("Meteorites per year (num_fell_found)", fontsize=12)
    ax.set_xticklabels(["Unfiltered\n(num_fell_found)"], fontsize=10)

    # Leave room for caption
    fig.subplots_adjust(bottom=0.22)

    caption = (
        r"$\bf{Graph\ 7.}$ "
        "EDA Phase 2 — Boxplot of yearly meteorite counts\n"
        "(num_fell_found) before outlier removal; the long whiskers and "
        "extreme\npoints illustrate the heavy-tailed distribution prior to "
        "Tukey 1.5×IQR \nfiltering."
    )
    fig.text(
        0.03, 0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Boxplot (unfiltered) saved to: {output_path.resolve()}")


def plot_box_filtered(df_filtered: pd.DataFrame, output_path: Path):
    """
    Graph 8: Boxplot of num_fell_found after Tukey 1.5*IQR outlier removal (EDA Phase 3).
    """
    values = df_filtered["num_fell_found"].astype(float).values

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()

    ax.boxplot(values, vert=True, patch_artist=True,
               boxprops=dict(facecolor="lightgreen", color="black"),
               medianprops=dict(color="red"),
               whiskerprops=dict(color="black"),
               capprops=dict(color="black"),
               flierprops=dict(marker="o", markersize=4, markerfacecolor="gray",
                               markeredgecolor="black"))

    ax.set_title("EDA Phase 3\nYearly Meteorite Counts (Outlier Removed)", fontsize=14)
    ax.set_ylabel("Meteorites per year (num_fell_found)", fontsize=12)
    ax.set_xticklabels(["Filtered\n(num_fell_found)"], fontsize=10)

    # Leave room for caption
    fig.subplots_adjust(bottom=0.24)

    caption = (
        r"$\bf{Graph\ 8.}$ "
        "EDA Phase 3 — Boxplot of yearly meteorite counts\n"
        "(num_fell_found) after removal of Tukey 1.5×IQR outliers;"
        "the reduced\nspread highlights the central bulk of the distribution "
        "once extreme\nhigh-count years are trimmed."
    )
    fig.text(
        0.03, 0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Boxplot (filtered) saved to: {output_path.resolve()}")


def main():
    # Ensure output directory exists (typically ".")
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # ================================
    # 2. Load Dataset
    # ================================
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found:\n  {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    required_cols = {"year", "num_fell_found"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            "Expected columns 'year' and 'num_fell_found' in input CSV.\n"
            f"Columns found: {list(df.columns)}"
        )

    # Coerce num_fell_found to numeric
    counts = pd.to_numeric(df["num_fell_found"], errors="coerce")
    df["num_fell_found"] = counts
    df = df.dropna(subset=["num_fell_found"])

    # Keep a copy of the unfiltered EDA Phase 2 data
    df_unfiltered = df.copy()

    # ================================
    # 3. Compute IQR bounds
    # ================================
    values = df["num_fell_found"].astype(float).values

    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # ================================
    # 4. Apply Outlier Filter
    # ================================
    mask_keep = (df["num_fell_found"] >= lower_bound) & (df["num_fell_found"] <= upper_bound)

    df_filtered = df[mask_keep].copy()

    # ================================
    # 5. Save Filtered Dataset
    # ================================
    df_filtered.to_csv(OUTPUT_CSV, index=False)

    # ================================
    # 6. Generate Boxplots (Graphs 7 and 8)
    # ================================
    plot_box_unfiltered(df_unfiltered, OUTPUT_BOX_UNFILTERED)
    plot_box_filtered(df_filtered, OUTPUT_BOX_FILTERED)

    # ================================
    # 7. Console Summary
    # ================================
    n_original = len(df_unfiltered)
    n_filtered = len(df_filtered)
    n_removed = n_original - n_filtered

    print("Outlier removal (Tukey 1.5 * IQR) complete.")
    print(f"Input file : {INPUT_CSV.resolve()}")
    print(f"Output file: {OUTPUT_CSV.resolve()}")
    print(f"Q1 (25%)          : {q1:,.4f}")
    print(f"Q3 (75%)          : {q3:,.4f}")
    print(f"IQR               : {iqr:,.4f}")
    print(f"Lower bound       : {lower_bound:,.4f}")
    print(f"Upper bound       : {upper_bound:,.4f}")
    print(f"Original rows     : {n_original}")
    print(f"Rows after filter : {n_filtered}")
    print(f"Rows removed      : {n_removed}")


if __name__ == "__main__":
    main()
