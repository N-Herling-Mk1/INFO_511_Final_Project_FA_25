#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_EDA_phase4_finalData_Tx.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science

Goal
----
Phase 4: Apply the recommended square-root transform to the yearly
meteorite counts (num_fell_found) after outlier removal, and perform
basic regression-assumption checks.

Input
-----
    outlier_filter_2.csv

Expected columns:
    year, num_fell_found

Processing
----------
1. Load the outlier-filtered dataset.
2. Apply a square-root transform:

       num_fell_found_sqrt = sqrt(num_fell_found)

3. Save a new CSV:

       final_data_Tx.csv

   with columns:
       year, num_fell_found, num_fell_found_sqrt

4. Generate four plots of the transformed response:

   - Graph 9.  Scatter plot: year vs sqrt(num_fell_found)
   - Graph 10. Histogram of sqrt(num_fell_found)
   - Graph 11. Box plot of sqrt(num_fell_found)
   - Graph 12. Q–Q plot of sqrt(num_fell_found) vs Normal

Outputs (PNG)
-------------
  EDA_phase4_scatter_year_vs_sqrt_counts.png   (Graph 9)
  EDA_phase4_hist_sqrt_counts.png              (Graph 10)
  EDA_phase4_box_sqrt_counts.png               (Graph 11)
  EDA_phase4_qq_sqrt_counts.png                (Graph 12)

Regression Checks
-----------------
Fit a simple linear regression:

    sqrt(num_fell_found) = beta0 + beta1 * (year_centered) + eps

and print:

  - n, min/max/mean/std of transformed counts
  - regression slope, intercept, R^2
  - Normality of residuals:
      * Shapiro–Wilk test statistic + p-value
      * residual skewness, residual kurtosis (fisher=False)
  - Autocorrelation / independence:
      * Durbin–Watson statistic
  - Homoscedasticity (rough check):
      * correlation between |residuals| and fitted values

No command line arguments needed.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# =========================
# 1. Paths
# =========================
INPUT_CSV = Path("outlier_filter_2.csv")
OUTPUT_CSV = Path("final_data_Tx.csv")

OUTPUT_SCATTER = Path("EDA_phase4_scatter_year_vs_sqrt_counts.png")  # Graph 9
OUTPUT_HIST = Path("EDA_phase4_hist_sqrt_counts.png")                # Graph 10
OUTPUT_BOX = Path("EDA_phase4_box_sqrt_counts.png")                  # Graph 11
OUTPUT_QQ = Path("EDA_phase4_qq_sqrt_counts.png")                    # Graph 12


# =========================
# 2. Data loading & transform
# =========================
def load_and_transform(path: Path) -> pd.DataFrame:
    """Load outlier-filtered data and apply square-root transform."""
    if not path.exists():
        raise FileNotFoundError(f"Could not find input CSV at:\n  {path}")

    df = pd.read_csv(path)

    required_cols = {"year", "num_fell_found"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            "Input CSV must contain columns: 'year', 'num_fell_found'.\n"
            f"Columns found: {list(df.columns)}"
        )

    # Coerce types
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["num_fell_found"] = pd.to_numeric(df["num_fell_found"], errors="coerce")

    # Drop rows with missing values
    df = df.dropna(subset=["year", "num_fell_found"])
    df["year"] = df["year"].astype(int)

    # Sort by year for time-series sense
    df = df.sort_values("year").reset_index(drop=True)

    # Square-root transform (counts should be >= 0; outlier-filtered set
    # is positive by construction, but we clip just in case).
    counts = df["num_fell_found"].clip(lower=0)
    df["num_fell_found_sqrt"] = np.sqrt(counts)

    return df


# =========================
# 3. Plotting functions
# =========================
def plot_scatter(df: pd.DataFrame, output_path: Path):
    """Graph 9. Scatter: year vs sqrt(num_fell_found)."""
    years = df["year"].values
    y_sqrt = df["num_fell_found_sqrt"].values

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    ax.scatter(years, y_sqrt, s=20, alpha=0.8, color="tab:blue", edgecolor="black")
    ax.set_title("Year vs sqrt(num_fell_found)", fontsize=14)
    ax.set_xlabel("Calendar year", fontsize=12)
    ax.set_ylabel("sqrt(num_fell_found)", fontsize=12)
    ax.set_xlim(years.min() - 1, years.max() + 1)

    # Leave room for caption
    fig.subplots_adjust(bottom=0.18)

    caption = (
        "Graph 9. EDA Phase 4 — Scatter of square-root transformed yearly "
        "meteorite counts (sqrt(num_fell_found)) \nversus calendar year."
    )
    fig.text(
        0.03,
        0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Scatter plot (Graph 9) saved to: {output_path.resolve()}")


def plot_histogram(df: pd.DataFrame, output_path: Path):
    """Graph 10. Histogram of sqrt(num_fell_found)."""
    y_sqrt = df["num_fell_found_sqrt"].values

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    ax.hist(y_sqrt, bins=20, edgecolor="black", color="tab:green", alpha=0.8)
    ax.set_title("Histogram of sqrt(num_fell_found)", fontsize=14)
    ax.set_xlabel("sqrt(num_fell_found)", fontsize=12)
    ax.set_ylabel("Frequency (number of years)", fontsize=12)

    fig.subplots_adjust(bottom=0.18)

    caption = (
        "Graph 10. EDA Phase 4 — Histogram of square-root transformed yearly "
        "meteorite counts (sqrt(num_fell_found)),\nshowing the distribution "
        "after outlier removal and variance-stabilizing transform."
    )
    fig.text(
        0.03,
        0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Histogram (Graph 10) saved to: {output_path.resolve()}")


def plot_box(df: pd.DataFrame, output_path: Path):
    """Graph 11. Box plot of sqrt(num_fell_found)."""
    y_sqrt = df["num_fell_found_sqrt"].values

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    ax.boxplot(
        y_sqrt,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="lightgray", color="black"),
        medianprops=dict(color="red"),
    )

    ax.set_title("Box plot of sqrt(num_fell_found)", fontsize=14)
    ax.set_ylabel("sqrt(num_fell_found)", fontsize=12)
    ax.set_xticks([])

    fig.subplots_adjust(bottom=0.20)

    caption = (
        "Graph 11. EDA Phase 4 — Box plot of square-root transformed yearly\n"
        "meteorite counts (sqrt(num_fell_found)), summarizing central\n tendency, "
        "spread, and remaining moderate outliers after filtering."
    )
    fig.text(
        0.03,
        0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Box plot (Graph 11) saved to: {output_path.resolve()}")


def plot_qq(df: pd.DataFrame, output_path: Path):
    """Graph 12. Q–Q plot of sqrt(num_fell_found) vs theoretical Normal."""
    y_sqrt = df["num_fell_found_sqrt"].values.astype(float)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    stats.probplot(y_sqrt, dist="norm", plot=ax)
    ax.set_title("Q–Q plot of sqrt(num_fell_found) vs Normal", fontsize=14)
    ax.set_xlabel("Theoretical quantiles (Normal)", fontsize=12)
    ax.set_ylabel("Sample quantiles (sqrt(num_fell_found))", fontsize=12)

    fig.subplots_adjust(bottom=0.20)

    caption = (
        "Graph 12. EDA Phase 4 — Q–Q plot comparing square-root transformed\n"
        "yearly meteorite counts (sqrt(num_fell_found)) to a theoretical "
        "Normal\ndistribution, used to assess residual Normality assumptions."
    )
    fig.text(
        0.03,
        0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Q–Q plot (Graph 12) saved to: {output_path.resolve()}")


# =========================
# 4. Regression-assumption checks
# =========================
def regression_checks(df: pd.DataFrame):
    """
    Perform simple numeric checks related to linear regression assumptions for:

        sqrt(num_fell_found) ~ year

    Prints:
      - basic summary of transformed counts
      - regression slope/intercept/R^2
      - Shapiro–Wilk test on residuals
      - residual skewness & kurtosis
      - Durbin–Watson statistic
      - correlation between |residuals| and fitted values
    """
    years = df["year"].values.astype(float)
    y_sqrt = df["num_fell_found_sqrt"].values.astype(float)

    n = len(y_sqrt)
    y_min, y_max = float(y_sqrt.min()), float(y_sqrt.max())
    y_mean, y_std = float(y_sqrt.mean()), float(y_sqrt.std(ddof=1))

    # Center the year variable for numerical stability
    year_mean = years.mean()
    years_centered = years - year_mean

    # Simple linear regression via np.polyfit (degree 1)
    beta1, beta0 = np.polyfit(years_centered, y_sqrt, deg=1)
    y_hat = beta0 + beta1 * years_centered
    residuals = y_sqrt - y_hat

    # R^2
    ss_tot = np.sum((y_sqrt - y_mean) ** 2)
    ss_res = np.sum(residuals ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    # Shapiro–Wilk for residual normality
    try:
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
    except Exception as e:
        shapiro_stat, shapiro_p = np.nan, np.nan
        print(f"[WARN] Shapiro–Wilk test failed: {e}")

    # Residual skewness & kurtosis
    resid_skew = stats.skew(residuals, bias=False)
    resid_kurt = stats.kurtosis(residuals, fisher=False, bias=False)

    # Durbin–Watson statistic for autocorrelation of residuals
    diff_resid = np.diff(residuals)
    dw = np.sum(diff_resid ** 2) / np.sum(residuals ** 2)

    # Simple homoscedasticity check: correlation between |resid| and fitted
    abs_resid = np.abs(residuals)
    if np.std(abs_resid) > 0 and np.std(y_hat) > 0:
        corr_abs_resid_fitted = np.corrcoef(abs_resid, y_hat)[0, 1]
    else:
        corr_abs_resid_fitted = np.nan

    # -------- Print summary --------
    print("\n=== EDA Phase 4 — Square-Root Transformed Data Summary ===")
    print(f"n (years): {n}")
    print(f"sqrt(num_fell_found): min = {y_min:.4f}, max = {y_max:.4f}")
    print(f"sqrt(num_fell_found): mean = {y_mean:.4f}, std = {y_std:.4f}\n")

    print("--- Linear Regression (sqrt(num_fell_found) ~ year_centered) ---")
    print(f"beta0 (intercept): {beta0:.4f}")
    print(f"beta1 (slope)    : {beta1:.6f} per year")
    print(f"R^2              : {r_squared:.4f}\n")

    print("--- Residual Normality ---")
    print(f"Shapiro–Wilk W   : {shapiro_stat:.4f}")
    print(f"Shapiro p-value  : {shapiro_p:.4g}")
    print(
        "  (p > 0.05 → cannot reject normality; "
        "p < 0.05 → evidence of non-normal residuals)"
    )
    print(f"Residual skewness: {resid_skew:.4f}")
    print(f"Residual kurtosis (fisher=False): {resid_kurt:.4f}")
    print("  (For ideal Normal residuals, skew ≈ 0, kurtosis ≈ 3)\n")

    print("--- Residual Independence / Autocorrelation ---")
    print(f"Durbin–Watson statistic: {dw:.4f}")
    print(
        "  (DW ≈ 2 suggests little autocorrelation; "
        "< 1 or > 3 can indicate strong autocorrelation.)\n"
    )

    print("--- Residual Homoscedasticity (rough check) ---")
    print(f"Corr(|residuals|, fitted): {corr_abs_resid_fitted:.4f}")
    print(
        "  (Correlation near 0 suggests no strong trend in spread "
        "with fitted values; large |corr| hints at heteroscedasticity.)"
    )
    print("=============================================================\n")


# =========================
# 5. Main
# =========================
def main():
    # Load and transform
    df = load_and_transform(INPUT_CSV)

    # Save transformed data
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Transformed dataset written to:\n  {OUTPUT_CSV.resolve()}")

    # Plots: Graphs 9–12
    plot_scatter(df, OUTPUT_SCATTER)   # Graph 9
    plot_histogram(df, OUTPUT_HIST)    # Graph 10
    plot_box(df, OUTPUT_BOX)           # Graph 11
    plot_qq(df, OUTPUT_QQ)             # Graph 12

    # Regression-assumption checks
    regression_checks(df)


if __name__ == "__main__":
    main()
