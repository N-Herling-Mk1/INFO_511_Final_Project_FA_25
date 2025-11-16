#!/usr/bin/env python3
"""
meteorite_freq_stats_with_boxplots.py

Pipeline:
1. Read Meteorite_Landings.csv (pure csv)
2. Build year -> count dictionary
3. Build count -> frequency dictionary (k -> years with k)
4. Compute mean, median, mode, variance of counts
5. IQR-based outlier reduction on counts
6. Analyze skewness (after IQR) and comment on log transform
7. Apply log1p transform to trimmed counts
8. Produce a 2 x 3 figure:
      Top row:  histograms (original, IQR-trimmed, log1p(trimmed))
      Bottom row: boxplots for each corresponding data series
"""

import csv
from collections import defaultdict, Counter

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# STEP 1: Build the year -> count dictionary (pure Python)
# ============================================================

year_to_count = defaultdict(int)

with open("Meteorite_Landings.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        year_str = row.get("year", "").strip()
        if not year_str:
            continue

        # Extract first 4 chars as year (e.g., '1880-01-01...' -> '1880')
        try:
            year = int(year_str[:4])
        except ValueError:
            continue

        year_to_count[year] += 1

# Sort by year
year_to_count = dict(sorted(year_to_count.items()))

print("\nYEAR -> COUNT (first 15 years):")
for i, (y, c) in enumerate(year_to_count.items()):
    if i >= 15:
        break
    print(f"{y}: {c}")
print("...")


# ============================================================
# STEP 2: Build count -> frequency dictionary (original)
# ============================================================

counts = list(year_to_count.values())
count_frequency = dict(sorted(Counter(counts).items()))

print("\nCOUNT -> FREQUENCY (k : years_with_k) [first 15]:")
for i, (k, freq) in enumerate(count_frequency.items()):
    if i >= 15:
        break
    print(f"{k}: {freq}")
print("...")


# ============================================================
# STEP 3: Summary statistics for original counts
# ============================================================

counts_arr = np.array(counts, dtype=float)
mean_counts = counts_arr.mean()
median_counts = float(np.median(counts_arr))
var_counts = counts_arr.var(ddof=0)
std_counts = counts_arr.std(ddof=0)

count_counter = Counter(counts)
max_freq = max(count_counter.values())
modes = sorted([k for k, v in count_counter.items() if v == max_freq])

print("\n=== Summary statistics (original counts) ===")
print(f"Mean     : {mean_counts:.3f}")
print(f"Median   : {median_counts:.3f}")
print(f"Variance : {var_counts:.3f}")
print(f"Std dev  : {std_counts:.3f}")
print(f"Mode(s)  : {modes} (each appears in {max_freq} year(s))")


# ============================================================
# STEP 4: IQR-based outlier reduction on counts
# ============================================================

q1 = np.percentile(counts_arr, 25)
q3 = np.percentile(counts_arr, 75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

trimmed_counts = [c for c in counts if lower_bound <= c <= upper_bound]
trimmed_freq = dict(sorted(Counter(trimmed_counts).items()))

print("\n=== IQR outlier reduction ===")
print(f"Q1         : {q1:.3f}")
print(f"Q3         : {q3:.3f}")
print(f"IQR        : {iqr:.3f}")
print(f"Lower bd   : {lower_bound:.3f}")
print(f"Upper bd   : {upper_bound:.3f}")
print(f"Years kept : {len(trimmed_counts)} / {len(counts)}")


# ============================================================
# STEP 5: Skewness on trimmed data & transform suggestion
# ============================================================

trim_arr = np.array(trimmed_counts, dtype=float)
trim_mean = trim_arr.mean()
trim_std = trim_arr.std(ddof=0)

if trim_std == 0:
    skew_trim = 0.0
else:
    skew_trim = np.mean(((trim_arr - trim_mean) / trim_std) ** 3)

print("\n=== Skewness (after IQR trimming) ===")
print(f"Skewness(trimmed counts): {skew_trim:.3f}")

if abs(skew_trim) < 0.5:
    skew_comment = "Nearly symmetric — transform not really needed."
    recommend_log = False
elif abs(skew_trim) < 1.0:
    skew_comment = "Moderately skewed — log transform could help."
    recommend_log = True
else:
    skew_comment = "Strongly skewed — log transform recommended."
    recommend_log = True

print("Interpretation:", skew_comment)


# ============================================================
# STEP 6: Always compute log1p(trimmed_counts) for comparison
# ============================================================

transformed_arr = np.log1p(trim_arr)

t_mean = transformed_arr.mean()
t_std = transformed_arr.std(ddof=0)
if t_std == 0:
    skew_trans = 0.0
else:
    skew_trans = np.mean(((transformed_arr - t_mean) / t_std) ** 3)

print("\n=== Skewness after log1p(transform) ===")
print(f"Skewness(log1p(trimmed counts)): {skew_trans:.3f}")
if recommend_log:
    print("Log1p transform is recommended / helpful based on skewness.")
else:
    print("Log1p transform flattens skew but may be optional.")


# ============================================================
# STEP 7: Build unified 2 x 3 plotting layout
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(24, 10))

# ---------- Panel (0,0): Histogram of original frequency-of-frequencies ----------
x1 = list(count_frequency.keys())
y1 = list(count_frequency.values())

axes[0, 0].bar(x1, y1, width=0.8, color="royalblue", edgecolor="black")
axes[0, 0].set_title("Original Counts (k → years)", fontsize=14)
axes[0, 0].set_xlabel("Meteorites per Year (k)")
axes[0, 0].set_ylabel("Number of Years with Count k")
axes[0, 0].tick_params(axis="x", rotation=90)

# ---------- Panel (1,0): Boxplot of original per-year counts ----------
axes[1, 0].boxplot(counts_arr, vert=True, patch_artist=True,
                   boxprops=dict(facecolor="royalblue", alpha=0.7))
axes[1, 0].set_title("Boxplot: Original Counts", fontsize=12)
axes[1, 0].set_ylabel("Meteorites per Year (k)")

# ---------- Panel (0,1): Histogram after IQR ----------
x2 = list(trimmed_freq.keys())
y2 = list(trimmed_freq.values())

axes[0, 1].bar(x2, y2, width=0.8, color="seagreen", edgecolor="black")
axes[0, 1].set_title("After IQR Outlier Reduction", fontsize=14)
axes[0, 1].set_xlabel("Meteorites per Year (k)")
axes[0, 1].tick_params(axis="x", rotation=90)

# ---------- Panel (1,1): Boxplot after IQR ----------
axes[1, 1].boxplot(trim_arr, vert=True, patch_artist=True,
                   boxprops=dict(facecolor="seagreen", alpha=0.7))
axes[1, 1].set_title("Boxplot: Counts After IQR", fontsize=12)
axes[1, 1].set_ylabel("Meteorites per Year (k)")

# ---------- Panel (0,2): Histogram of log1p(trimmed_counts) ----------
axes[0, 2].hist(transformed_arr, bins=20, color="orchid", edgecolor="black")
title_suffix = " (recommended)" if recommend_log else " (optional)"
axes[0, 2].set_title(f"log1p(Counts After IQR){title_suffix}", fontsize=14)
axes[0, 2].set_xlabel("log1p(Meteorites per Year)")
axes[0, 2].set_ylabel("Frequency")

# ---------- Panel (1,2): Boxplot of log1p(trimmed_counts) ----------
axes[1, 2].boxplot(transformed_arr, vert=True, patch_artist=True,
                   boxprops=dict(facecolor="orchid", alpha=0.7))
axes[1, 2].set_title("Boxplot: log1p(Counts After IQR)", fontsize=12)
axes[1, 2].set_ylabel("log1p(Meteorites per Year)")

plt.tight_layout()
plt.show()
