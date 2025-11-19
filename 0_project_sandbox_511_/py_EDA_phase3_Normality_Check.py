#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_EDA_phase3_Normality_Check.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science.

Goal
----
Read the EDA Phase 3 outlier-filtered meteorite dataset:

    outlier_filter_2.csv

with columns (at minimum):
    year, num_fell_found

Perform numeric normality checks on the yearly counts (num_fell_found):

  * Multimodality (via KDE-based mode-count heuristic)
  * Skewness (asymmetry)
  * Kurtosis (tailedness; using kurtosis relative to Normal with fisher=False)

Then:
  * Print metrics and short plain-language explanations
  * Evaluate several candidate transformations to move the data toward Normal:
      - identity (no transform)
      - log1p(x)
      - sqrt(x)
      - cbrt(x)
      - Box–Cox (if strictly positive)
  * Choose the best transform via a simple score:
        score = |skew| + |kurtosis - 3|
    (smaller = closer to Normal)
  * Apply that transform and:

      - Generate a side-by-side comparison plot:
          · Original histogram + Q–Q
          · Transformed histogram + Q–Q
      - Z-transform the transformed data (mean 0, sd 1) and
        report its summary metrics.

Outputs
-------
Console:
  - Original normality metrics
  - Ranked transform summary
  - Before/after “distance from Normal”
  - Z-transform summary

Figure:
  EDA_phase3_normality_comparison.png

No command line arguments needed.
"""

from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# ================================
# 1. Paths (hard-coded, current dir)
# ================================
INPUT_CSV = Path("outlier_filter_2.csv")
OUTPUT_FIG = Path("EDA_phase3_normality_comparison.png")


def load_data(path: Path) -> np.ndarray:
    """
    Load the outlier-filtered dataset and return the num_fell_found
    values as a 1D float array.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found:\n  {path}")

    df = pd.read_csv(path)

    if "num_fell_found" not in df.columns:
        raise ValueError(
            "Expected column 'num_fell_found' in input CSV.\n"
            f"Columns found: {list(df.columns)}"
        )

    counts = pd.to_numeric(df["num_fell_found"], errors="coerce")
    counts = counts.dropna()

    if counts.empty:
        raise ValueError("No valid numeric values in 'num_fell_found' column.")

    return counts.astype(float).values


# ================================
# 2. Multimodality Heuristic
# ================================
def estimate_mode_count(values: np.ndarray, grid_size: int = 512) -> int:
    """
    Estimate the number of modes (peaks) in the distribution of `values`
    using a Gaussian KDE over a 1D grid, then counting local maxima.

    This is a heuristic numeric measure:
        - mode_count = 1  → roughly unimodal
        - mode_count > 1  → evidence for multimodality
    """
    kde = stats.gaussian_kde(values)
    xs = np.linspace(values.min(), values.max(), grid_size)
    ys = kde(xs)

    peaks = 0
    for i in range(1, len(ys) - 1):
        if ys[i] > ys[i - 1] and ys[i] > ys[i + 1]:
            peaks += 1
    return peaks


# ================================
# 3. Core Normality Metrics
# ================================
def compute_shape_metrics(values: np.ndarray) -> Dict[str, float]:
    """
    Compute skewness and kurtosis for a 1D numeric array.

    Returns
    -------
    dict with keys:
        'skew', 'kurtosis'
    where kurtosis is calculated with fisher=False,
    so Normal ≈ 3, per INFO 511 Lecture 4.
    """
    skew_val = stats.skew(values, bias=False)
    kurt_val = stats.kurtosis(values, fisher=False, bias=False)
    return {
        "skew": float(skew_val),
        "kurtosis": float(kurt_val),
    }


def interpret_skew(skew: float) -> str:
    """
    Provide a short interpretation of skewness.
    """
    if abs(skew) < 0.5:
        desc = "approximately symmetric"
    elif 0.5 <= skew < 1.0:
        desc = "moderately right-skewed"
    elif skew >= 1.0:
        desc = "strongly right-skewed (heavy right tail)"
    elif -1.0 < skew <= -0.5:
        desc = "moderately left-skewed"
    else:  # skew <= -1.0
        desc = "strongly left-skewed (heavy left tail)"
    return desc


def interpret_kurtosis(kurt: float) -> str:
    """
    Provide a short interpretation of kurtosis relative to Normal (=3).
    """
    if abs(kurt - 3.0) < 0.3:
        desc = "close to mesokurtic (similar tails to Normal)"
    elif kurt > 3.0:
        desc = "leptokurtic (heavier tails, more extreme values)"
    else:  # kurt < 3.0
        desc = "platykurtic (lighter tails, fewer extremes)"
    return desc


def interpret_modes(mode_count: int) -> str:
    """
    Provide a short interpretation of the KDE mode count.
    """
    if mode_count <= 1:
        return "approximately unimodal (single main peak)"
    elif mode_count == 2:
        return "likely bimodal (two prominent peaks)"
    else:
        return f"multimodal (about {mode_count} peaks detected)"


# ================================
# 4. Transform Evaluation
# ================================
def evaluate_transforms(values: np.ndarray) -> Dict[str, Dict[str, Any]]:
    """
    Evaluate several transforms on the distribution and compute
    skewness / kurtosis for each.

    Returns
    -------
    dict: transform_name -> {
        'skew': ...,
        'kurtosis': ...,
        'score': abs(skew) + abs(kurtosis - 3),
        'extra': optional extra info (e.g., lambda for Box–Cox)
    }
    """
    results: Dict[str, Dict[str, Any]] = {}

    # Identity (no transform)
    metrics_id = compute_shape_metrics(values)
    score_id = abs(metrics_id["skew"]) + abs(metrics_id["kurtosis"] - 3.0)
    results["identity"] = {
        "skew": metrics_id["skew"],
        "kurtosis": metrics_id["kurtosis"],
        "score": score_id,
        "extra": None,
    }

    # Ensure strictly positive for transforms that require it
    positive_values = values[values > 0]
    if positive_values.size == 0:
        return results

    # log1p
    log_vals = np.log1p(positive_values)
    m_log = compute_shape_metrics(log_vals)
    score_log = abs(m_log["skew"]) + abs(m_log["kurtosis"] - 3.0)
    results["log1p"] = {
        "skew": m_log["skew"],
        "kurtosis": m_log["kurtosis"],
        "score": score_log,
        "extra": None,
    }

    # sqrt
    sqrt_vals = np.sqrt(positive_values)
    m_sqrt = compute_shape_metrics(sqrt_vals)
    score_sqrt = abs(m_sqrt["skew"]) + abs(m_sqrt["kurtosis"] - 3.0)
    results["sqrt"] = {
        "skew": m_sqrt["skew"],
        "kurtosis": m_sqrt["kurtosis"],
        "score": score_sqrt,
        "extra": None,
    }

    # cube-root
    cbrt_vals = np.cbrt(positive_values)
    m_cbrt = compute_shape_metrics(cbrt_vals)
    score_cbrt = abs(m_cbrt["skew"]) + abs(m_cbrt["kurtosis"] - 3.0)
    results["cuberoot"] = {
        "skew": m_cbrt["skew"],
        "kurtosis": m_cbrt["kurtosis"],
        "score": score_cbrt,
        "extra": None,
    }

    # Box–Cox (scipy.stats.boxcox requires strictly positive values)
    try:
        bc_vals, lam = stats.boxcox(positive_values)
        m_bc = compute_shape_metrics(bc_vals)
        score_bc = abs(m_bc["skew"]) + abs(m_bc["kurtosis"] - 3.0)
        results["boxcox"] = {
            "skew": m_bc["skew"],
            "kurtosis": m_bc["kurtosis"],
            "score": score_bc,
            "extra": {"lambda": lam},
        }
    except Exception as e:
        results["boxcox"] = {
            "skew": np.nan,
            "kurtosis": np.nan,
            "score": np.inf,
            "extra": {"error": str(e)},
        }

    return results


def apply_transform(
    values: np.ndarray,
    name: str,
    extra: Optional[Dict[str, Any]] = None
) -> np.ndarray:
    """
    Apply the named transform to the full (positive) array.
    """
    if name == "identity":
        return values.copy()

    # Ensure positive for the rest
    vals = values.copy()
    if np.any(vals <= 0):
        vals = vals[vals > 0]

    if name == "log1p":
        return np.log1p(vals)
    elif name == "sqrt":
        return np.sqrt(vals)
    elif name == "cuberoot":
        return np.cbrt(vals)
    elif name == "boxcox":
        lam = None
        if extra is not None:
            lam = extra.get("lambda", None)
        if lam is None or not np.isfinite(lam):
            transformed, _ = stats.boxcox(vals)
        else:
            transformed = stats.boxcox(vals, lmbda=lam)
        return transformed
    else:
        # Unknown transform; fallback to identity
        return values.copy()


def print_transform_summary(results: Dict[str, Dict[str, Any]]):
    """
    Print a ranked summary of transforms, from most Normal-like
    (lowest score) to least, and highlight a recommended choice.
    """
    print("\n=== Candidate Transforms: Skewness & Kurtosis ===")
    print("Score = |skew| + |kurtosis - 3|  (lower is closer to Normal)")

    ordered = sorted(results.items(), key=lambda kv: kv[1]["score"])
    for name, res in ordered:
        skew = res["skew"]
        kurt = res["kurtosis"]
        score = res["score"]
        extra = res["extra"]

        extra_str = ""
        if name == "boxcox" and extra is not None and "lambda" in extra and np.isfinite(res["score"]):
            extra_str = f" (lambda ≈ {extra['lambda']:.3f})"
        print(f"- {name:8s}: skew = {skew:8.4f}, kurtosis = {kurt:8.4f}, score = {score:8.4f}{extra_str}")

    best_name, best_res = ordered[0]
    print("\n>>> Recommended transform (numeric normality heuristic):")
    print(f"    {best_name!r} — skew ≈ {best_res['skew']:.4f}, "
          f"kurtosis ≈ {best_res['kurtosis']:.4f}, "
          f"closest to Normal (skew≈0, kurtosis≈3).")

    if best_name == "identity":
        print("    The outlier-filtered data are already relatively close to Normal by this metric.")
    elif best_name == "log1p":
        print("    A log1p transform is especially common for right-skewed count data with heavy tails.")
    elif best_name == "sqrt":
        print("    A square-root transform is a gentler alternative for count data with moderate skew.")
    elif best_name == "cuberoot":
        print("    A cube-root transform can help with strong skew while preserving spread more than log.")
    elif best_name == "boxcox":
        print("    Box–Cox can be tuned (via lambda) to pull both skewness and kurtosis toward Normal.")


# ================================
# 5. Plotting: Side-by-Side Normality Comparison
# ================================
def plot_normality_comparison(
    original: np.ndarray,
    transformed: np.ndarray,
    transform_name: str,
    output_path: Path,
):
    """
    Produce a 2×2 figure comparing original vs transformed data:

      Top-left  : Histogram (original)
      Top-right : Q–Q plot (original)
      Bottom-left  : Histogram (transformed)
      Bottom-right : Q–Q plot (transformed)

    Saves to output_path.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # --- Original histogram ---
    ax_hist_orig = axes[0, 0]
    ax_hist_orig.hist(original, bins=20, edgecolor="black", color="tab:blue", alpha=0.8)
    ax_hist_orig.set_title("Original (Outlier-Filtered)\nHistogram", fontsize=12)
    ax_hist_orig.set_xlabel("num_fell_found", fontsize=10)
    ax_hist_orig.set_ylabel("Count of years", fontsize=10)

    # --- Original Q–Q ---
    ax_qq_orig = axes[0, 1]
    stats.probplot(original, dist="norm", plot=ax_qq_orig)
    ax_qq_orig.set_title("Original (Outlier-Filtered)\nQ–Q vs Normal", fontsize=12)
    ax_qq_orig.set_xlabel("Theoretical quantiles", fontsize=10)
    ax_qq_orig.set_ylabel("Sample quantiles", fontsize=10)

    # --- Transformed histogram ---
    ax_hist_trans = axes[1, 0]
    ax_hist_trans.hist(transformed, bins=20, edgecolor="black", color="tab:green", alpha=0.8)
    ax_hist_trans.set_title(f"Transformed ({transform_name})\nHistogram", fontsize=12)
    ax_hist_trans.set_xlabel(f"{transform_name}(num_fell_found)", fontsize=10)
    ax_hist_trans.set_ylabel("Count of years", fontsize=10)

    # --- Transformed Q–Q ---
    ax_qq_trans = axes[1, 1]
    stats.probplot(transformed, dist="norm", plot=ax_qq_trans)
    ax_qq_trans.set_title(f"Transformed ({transform_name})\nQ–Q vs Normal", fontsize=12)
    ax_qq_trans.set_xlabel("Theoretical quantiles", fontsize=10)
    ax_qq_trans.set_ylabel("Sample quantiles", fontsize=10)

    # Layout + caption
    fig.subplots_adjust(left=0.07, right=0.97, top=0.90, bottom=0.14, wspace=0.25, hspace=0.35)

    caption = (
        "Graph 9. EDA Phase 3 — Comparison of yearly meteorite counts "
        "(num_fell_found) before and after the recommended transformation. "
        "Top row: original outlier-filtered data. Bottom row: transformed "
        f"data using {transform_name}. Histograms and Q–Q plots show how the "
        "transformation pulls the distribution closer to Normal."
    )
    fig.text(
        0.05,
        0.02,
        caption,
        ha="left",
        va="bottom",
        fontsize=11,
    )

    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Normality comparison figure saved to: {output_path.resolve()}")


# ================================
# 6. Main
# ================================
def main():
    values = load_data(INPUT_CSV)

    print("=== EDA Phase 3 — Normality Check on num_fell_found ===")
    print(f"Number of yearly observations (after outlier removal): {len(values)}")
    print(f"Min / Max: {values.min():.4f} / {values.max():.4f}")
    print(f"Mean / Std: {values.mean():.4f} / {values.std(ddof=1):.4f}")

    # Multimodality + original shape metrics
    mode_count = estimate_mode_count(values)
    skew_kurt_orig = compute_shape_metrics(values)

    print("\n--- Shape Metrics (Original, Outlier-Filtered Data) ---")
    print(f"Multimodality (KDE mode count): {mode_count} "
          f"→ {interpret_modes(mode_count)}")
    print(f"Skewness: {skew_kurt_orig['skew']:.4f} "
          f"→ {interpret_skew(skew_kurt_orig['skew'])}")
    print(f"Kurtosis (fisher=False): {skew_kurt_orig['kurtosis']:.4f} "
          f"→ {interpret_kurtosis(skew_kurt_orig['kurtosis'])}")
    print("\nNote: For a perfectly Normal distribution, skewness ≈ 0 and "
          "kurtosis ≈ 3 (mesokurtic), per INFO 511 Lecture 4.")

    # Evaluate transforms
    results = evaluate_transforms(values)
    print_transform_summary(results)

    # Identify original score and best transform
    original_score = results["identity"]["score"]
    best_name, best_res = sorted(results.items(), key=lambda kv: kv[1]["score"])[0]
    best_score = best_res["score"]

    # Apply the recommended transform
    transformed_values = apply_transform(values, best_name, best_res.get("extra"))

    # Recompute shape metrics on transformed data
    skew_kurt_trans = compute_shape_metrics(transformed_values)

    print("\n--- Before vs After (Distance from Normal) ---")
    print(f"Original score:   |skew| + |kurt-3| = {original_score:.4f}")
    print(f"Transformed score (using {best_name}): {best_score:.4f}")
    if original_score > 0 and np.isfinite(best_score):
        improvement = 100.0 * (original_score - best_score) / original_score
        print(f"Relative improvement: {improvement:.2f}% reduction in distance from Normal.")
    print(f"Transformed skewness:  {skew_kurt_trans['skew']:.4f}")
    print(f"Transformed kurtosis:  {skew_kurt_trans['kurtosis']:.4f}")

    # === Z-transform of the transformed data ===
    mu = transformed_values.mean()
    sigma = transformed_values.std(ddof=1)
    if sigma == 0:
        print("\nZ-transform could not be computed: standard deviation is zero.")
        z_values = transformed_values.copy()
    else:
        z_values = (transformed_values - mu) / sigma

    z_metrics = compute_shape_metrics(z_values)

    print("\n--- Z-Transform of Transformed Data ---")
    print("We now standardize the recommended transform:")
    print(f"Z = ({best_name}(num_fell_found) - mean) / std")
    print(f"Z min / max: {z_values.min():.4f} / {z_values.max():.4f}")
    print(f"Z skewness:  {z_metrics['skew']:.4f}")
    print(f"Z kurtosis:  {z_metrics['kurtosis']:.4f}")
    print("Note: Z-transform rescales and recenters the data but does not change "
          "its shape, so skewness and kurtosis remain effectively the same as "
          "for the transformed (non-Z) data.")

    # Plot side-by-side comparison (original vs transformed)
    plot_normality_comparison(values, transformed_values, best_name, OUTPUT_FIG)

    print("\nNext steps suggestion:")
    print("  • Use the recommended transform followed by Z-scoring as input to models")
    print("    that assume Normal, standardized predictors (e.g., many regression and")
    print("    regularized methods).")
    print("  • Include Graph 9 and Z-transform summary in your report to show how the")
    print("    data were made more Normal-like and standardized before modeling.")


if __name__ == "__main__":
    main()
