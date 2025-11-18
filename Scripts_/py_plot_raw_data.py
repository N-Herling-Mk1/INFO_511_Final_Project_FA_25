#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""'
Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science.
.
py_plot_raw_data.py
....
Read the original Meteorite_Landings.csv file and create a jittered
time-series scatter plot of meteorite FALLS and FINDS by year.

Input:
    Data_/Meteorite_Landings.csv

Output:
    Meteorite_Falls_Found_Time_Series.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# 1. Paths
# =========================
INPUT_CSV = Path("..\Data_") / "Meteorite_Landings.csv"
OUTPUT_PNG_LINEAR = Path("Meteorite_Falls_Found_Time_Series_linear.png")
OUTPUT_PNG_LOGX = Path("Meteorite_Falls_Found_Time_Series_logx.png")


def build_jittered_coords(df):
    """
    Given a dataframe with columns 'fall' and 'year_int',
    return:
        - summary stats
        - a dict mapping category -> (x_vals, y_vals)
    """
    # Total counts by year (any category)
    counts_by_year_total = df.groupby("year_int").size()

    min_year = int(counts_by_year_total.index.min())
    max_year = int(counts_by_year_total.index.max())
    min_count = int(counts_by_year_total.min())
    max_count = int(counts_by_year_total.max())
    total_meteorites = int(len(df))

    # Counts per category
    counts_by_category = df["fall"].value_counts().to_dict()
    n_fell = counts_by_category.get("Fell", 0)
    n_found = counts_by_category.get("Found", 0)

    # Build jittered scatter coordinates per category
    rng = np.random.default_rng(seed=42)  # reproducible jitter
    category_coords = {}

    for category in ["Fell", "Found"]:
        df_cat = df[df["fall"] == category]

        x_vals = []
        y_vals = []

        for year, group in df_cat.groupby("year_int"):
            n = len(group)
            indices = np.arange(1, n + 1, dtype=float)

            # Vertical jitter so points for the same year don't stack exactly
            jitter = rng.uniform(-0.2, 0.2, size=n)
            y_jittered = indices + jitter

            x_vals.extend([year] * n)
            y_vals.extend(y_jittered)

        category_coords[category] = (np.array(x_vals), np.array(y_vals))

    summary = {
        "min_year": min_year,
        "max_year": max_year,
        "min_count": min_count,
        "max_count": max_count,
        "total_meteorites": total_meteorites,
        "n_fell": n_fell,
        "n_found": n_found,
    }

    return summary, category_coords


def make_plot(summary, category_coords, output_path, log_x=False, graph_index=1):
    """
    Make a scatter plot (linear or log-x) and save to output_path.

    One legend on the LEFT.
    Summary box directly BELOW the legend, also on the left.
    Nothing on the right.

    Below each graph, add a caption:
      Graph 1. <synopsis>
    with "Graph X." in bold, font size 13.
    """

    min_year = summary["min_year"]
    max_year = summary["max_year"]
    min_count = summary["min_count"]
    max_count = summary["max_count"]
    total_meteorites = summary["total_meteorites"]
    n_fell = summary["n_fell"]
    n_found = summary["n_found"]

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Colors
    color_map = {"Fell": "tab:blue", "Found": "tab:orange"}

    # Scatter
    fell_x, fell_y = category_coords["Fell"]
    found_x, found_y = category_coords["Found"]

    fell_scatter = ax.scatter(fell_x, fell_y, s=10, alpha=0.7, color=color_map["Fell"])
    found_scatter = ax.scatter(found_x, found_y, s=10, alpha=0.7, color=color_map["Found"])

    # Axis labels/title
    ax.set_xlabel("Calendar year (log scale)" if log_x else "Calendar year")
    ax.set_ylabel("Meteorites per year (jittered index)")
    ax.set_title(
        "Meteorite Falls and Finds Over Time (log-x scale)\nRaw data"
        if log_x
        else "Meteorite Falls and Finds Over Time\nRaw data"
    )

    ax.set_xlim(min_year - 5, max_year + 5)
    if log_x:
        ax.set_xscale("log")

    # -----------------------
    #  ONE LEGEND (Left Side)
    # -----------------------
    legend = ax.legend(
        [fell_scatter, found_scatter],
        [f"Fell (n={n_fell})", f"Found (n={n_found})"],
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98),   # inset from left & top
        frameon=True,
    )
    ax.add_artist(legend)

    # -----------------------
    # SUMMARY BOX (Below legend)
    # -----------------------
    summary_text = (
        f"Years: {min_year} – {max_year}\n"
        f"Min yearly count: {min_count}\n"
        f"Max yearly count: {max_count}\n"
        f"Total meteorites: {total_meteorites}\n"
        f"  Fell:  {n_fell}\n"
        f"  Found: {n_found}"
    )

    ax.text(
        0.03, 0.78,                      # BELOW the legend
        summary_text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
    )

    # -----------------------
    # CAPTION BELOW GRAPH
    # -----------------------
    fig = plt.gcf()

    # Synopsis text depends on the graph
    if log_x:
        synopsis = " Raw data - Jittered scatterplot of raw Fell and Found meteorites by calendar year (log-scaled x-axis)."
    else:
        synopsis = " Raw data - Jittered scatterplot of raw Fell and Found meteorites by calendar year (linear x-axis)."

    caption = rf"$\bf{{Graph\ {graph_index}.}}$" + synopsis

    # Give extra vertical space between x-axis and caption by increasing bottom margin
    plt.subplots_adjust(bottom=0.15)

    # Left-justified caption, slightly below the axes area
    fig.text(
        0.03, 0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=13,
    )

    #plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    # =========================
    # 2. Load data
    # =========================
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Could not find input CSV at:\n  {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    # Need 'fall' and 'year' columns
    if "fall" not in df.columns or "year" not in df.columns:
        raise ValueError(
            "CSV must contain 'fall' and 'year' columns. "
            f"Columns found: {list(df.columns)}"
        )

    # Keep only 'Fell' or 'Found' meteorites
    df = df[df["fall"].isin(["Fell", "Found"])].copy()

    # Convert 'year' to integer; drop rows where this fails
    df["year_int"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year_int"])
    df["year_int"] = df["year_int"].astype(int)

    if df.empty:
        raise ValueError("No valid 'Fell' or 'Found' meteorites with a usable year.")

    # =========================
    # 3. Shared coordinates + summary
    # =========================
    summary, category_coords = build_jittered_coords(df)

    # =========================
    # 4. Make linear-x plot
    # =========================
    make_plot(summary, category_coords, OUTPUT_PNG_LINEAR, log_x=False, graph_index=1)
    print(f"Linear-x plot saved to: {OUTPUT_PNG_LINEAR.resolve()}")

    # =========================
    # 5. Make log-x plot
    # =========================
    make_plot(summary, category_coords, OUTPUT_PNG_LOGX, log_x=True, graph_index=2)
    print(f"Log-x plot saved to: {OUTPUT_PNG_LOGX.resolve()}")

    # Also print summary to console
    print(
        "Summary:\n"
        f"  Years: {summary['min_year']} – {summary['max_year']}\n"
        f"  Min total count in a year: {summary['min_count']}\n"
        f"  Max total count in a year: {summary['max_count']}\n"
        f"  Total meteorites plotted: {summary['total_meteorites']}\n"
        f"    Fell:  {summary['n_fell']}\n"
        f"    Found: {summary['n_found']}"
    )


if __name__ == "__main__":
    main()
