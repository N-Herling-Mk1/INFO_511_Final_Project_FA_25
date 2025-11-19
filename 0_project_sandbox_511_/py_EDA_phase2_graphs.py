#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_EDA_phase2_graphs.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science

Goal
----
Read the refactored meteorite dataset:

    imputating_filter1_Tx.csv

with columns:
    year, num_fell_found

and produce three EDA visuals:

  1. Frequency distribution / histogram of num_fell_found
     (using log-spaced bins on a log-scaled x-axis)
  2. Time-series scatter plot of yearly counts (year vs num_fell_found)
  3. Q–Q plot of num_fell_found versus a theoretical Normal distribution

Outputs
-------
PNG files in the current working directory:

  EDA_phase2_hist_num_fell_found.png
  EDA_phase2_scatter_year_counts.png
  EDA_phase2_qq_num_fell_found.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# =========================
# 1. Paths
# =========================
INPUT_CSV = Path("imputating_filter1_Tx.csv")

OUTPUT_HIST = Path("EDA_phase2_hist_num_fell_found.png")
OUTPUT_SCATTER = Path("EDA_phase2_scatter_year_counts.png")
OUTPUT_QQ = Path("EDA_phase2_qq_num_fell_found.png")


def load_data(path: Path) -> pd.DataFrame:
    """Load the year / num_fell_found dataset and do basic sanity checks."""
    if not path.exists():
        raise FileNotFoundError(f"Could not find input CSV at:\n  {path}")

    df = pd.read_csv(path)

    required_cols = {"year", "num_fell_found"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            "Input CSV must contain columns: 'year', 'num_fell_found'.\n"
            f"Columns found: {list(df.columns)}"
        )

    # Ensure types make sense
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["num_fell_found"] = pd.to_numeric(df["num_fell_found"], errors="coerce")

    df = df.dropna(subset=["year", "num_fell_found"])
    df["year"] = df["year"].astype(int)

    # Sort by year for time-series plotting
    df = df.sort_values("year")

    return df


def plot_histogram(df: pd.DataFrame, output_path: Path):
    """
    Plot the frequency distribution (histogram) of num_fell_found
    using log-spaced bins and a log-scaled x-axis.

    X-axis: num_fell_found (meteorites per year), log scale
    Y-axis: number of years with counts in each bin
    """
    counts = df["num_fell_found"].values.astype(float)

    # For log scale we must have strictly positive values
    counts = counts[counts > 0]
    if counts.size == 0:
        raise ValueError("All num_fell_found values are non-positive; cannot make log histogram.")

    min_c = counts.min()
    max_c = counts.max()

    fig = plt.figure(figsize=(10, 6))
    ax = fig.gca()

    # Log-spaced bins between min and max
    bins = np.logspace(np.log10(min_c), np.log10(max_c), num=20)

    ax.hist(counts, bins=bins, edgecolor="black", color="tab:green", alpha=0.8)

    ax.set_xscale("log")
    ax.set_title("EDA Phase 2\nYearly Meteorite Counts (log-spaced bins)", fontsize=14)
    ax.set_xlabel("Meteorites per year (num_fell_found, log scale)", fontsize=12)
    ax.set_ylabel("Number of years", fontsize=12)

    # Nicer, human-readable tick labels
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.tick_params(axis="x", rotation=45)

    # Leave extra room at the bottom for the caption
    fig.subplots_adjust(bottom=0.20)

    # Caption: Graph 4
    caption = (
        r"$\bf{Graph\ 4.}$ "
        "EDA Phase 2 — Histogram of yearly meteorite counts"
        "(num_fell_found) after imputation and transformation;\n "
        "log-spaced bins on a log-scaled x-axis highlight the heavy-tailed "
        "distribution."
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
    print(f"Histogram saved to: {output_path.resolve()}")


def plot_time_series_scatter(df: pd.DataFrame, output_path: Path):
    """
    Time-series scatter plot:

    X-axis: calendar year
    Y-axis: num_fell_found (meteorites per year)
    """
    years = df["year"].values
    counts = df["num_fell_found"].values

    fig = plt.figure(figsize=(12, 6))
    ax = fig.gca()

    ax.scatter(years, counts, s=20, alpha=0.8, color="tab:blue", edgecolor="black")

    ax.set_title("EDA Phase 2\nYearly Meteorite Counts Over Time", fontsize=14)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Meteorites per year (num_fell_found)", fontsize=12)

    ax.set_xlim(years.min() - 1, years.max() + 1)

    # Extra room for caption
    fig.subplots_adjust(bottom=0.20)

    # Caption: Graph 5
    caption = (
        r"$\bf{Graph\ 5.}$ "
        "EDA Phase 2 — Time-series scatter of yearly meteorite counts "
        "(num_fell_found) after imputation and transformation;\n reveals "
        "temporal structure and the emergence of high-count discovery years."
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
    print(f"Time-series scatter saved to: {output_path.resolve()}")


def plot_qq(df: pd.DataFrame, output_path: Path):
    """
    Q–Q plot of num_fell_found vs theoretical Normal.

    This checks how well the yearly counts resemble a Normal distribution.
    """
    counts = df["num_fell_found"].values.astype(float)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()

    # Create Q–Q plot against standard normal
    stats.probplot(counts, dist="norm", plot=ax)

    ax.set_title("EDA Phase 2\nQ–Q Plot: Yearly Meteorite Counts vs Normal", fontsize=14)
    ax.set_xlabel("Theoretical quantiles (Normal)", fontsize=12)
    ax.set_ylabel("Sample quantiles (num_fell_found)", fontsize=12)

    # Extra room for caption
    fig.subplots_adjust(bottom=0.23)

    # Caption: Graph 6
    caption = (
        r"$\bf{Graph\ 6.}$ "
        "EDA Phase 2 — Q–Q plot of yearly meteorite counts\n "
        "(num_fell_found) after imputation and transformation;"
        "strong deviations\n from the reference line indicate substantial "
        "departure from Normality."
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
    print(f"Q–Q plot saved to: {output_path.resolve()}")


def main():
    df = load_data(INPUT_CSV)

    print("Loaded data:")
    print(df.head())
    print("\nBasic summary of num_fell_found:")
    print(df["num_fell_found"].describe())

    plot_histogram(df, OUTPUT_HIST)
    plot_time_series_scatter(df, OUTPUT_SCATTER)
    plot_qq(df, OUTPUT_QQ)


if __name__ == "__main__":
    main()
