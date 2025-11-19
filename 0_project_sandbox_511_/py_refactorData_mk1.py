#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py_refactorData_mk1.py

Nathan Herling
University of Arizona - Fall 2025
INFO 511 - Introduction to Data Science

Goal
----
Read the original Meteorite_Landings.csv file and refactor it down to a
two-column dataset:

    [year], [num_fell_found]

where:
  * year           = calendar year (integer)
  * num_fell_found = number of meteorites (Fell or Found) recorded in that year

Filters / cleaning steps:
  (1) Eliminate any rows with missing/invalid year values.
  (2) Eliminate any rows that are exact duplicates of existing rows.
  (3) Eliminate any rows with year > 2013.
  (4) Keep only rows whose 'fall' field is Fell or Found.

Year parsing
------------
We do NOT use pandas.to_datetime here (to avoid 1970/epoch weirdness).
Instead we:
  * Treat the raw 'year' value as a string.
  * Extract up to the first 3–4 leading digits until we hit a non-digit.
    e.g.,
      '860-01-01T00:00:00'   -> 860
      '1880-01-01T00:00:00'  -> 1880
      1985.0                 -> 1985
      '1970-01-01 00:00:00'  -> 1970

Output
------
Write the reduced dataset to:

    imputating_filter1_Tx.csv

in the current working directory.
"""

from pathlib import Path
import pandas as pd


# =========================
# 1. Paths
# =========================
INPUT_CSV = Path("..") / "Data_" / "Meteorite_Landings.csv"
OUTPUT_CSV = Path("imputating_filter1_Tx.csv")


def extract_year_from_string(val):
    """
    Safely extract a calendar year (3–4 leading digits) from the raw 'year' field.

    Strategy:
      - Convert to string and strip whitespace.
      - If empty, return pd.NA.
      - Scan characters from the start:
          accumulate digits until we hit a non-digit or have 4 digits.
      - If we collected at least one digit, convert to int; else return pd.NA.

    Examples:
      '860-01-01T00:00:00'   -> 860
      '1880-01-01T00:00:00'  -> 1880
      '860.0'                -> 860
      1985.0                 -> 1985
    """
    s = str(val).strip()
    if not s:
        return pd.NA

    digits = []
    for ch in s:
        if ch.isdigit():
            digits.append(ch)
            if len(digits) == 4:
                break
        else:
            # stop at first non-digit
            break

    if not digits:
        return pd.NA

    year_int = int("".join(digits))
    return year_int


def main():
    # -------------------------
    # Load original dataset
    # -------------------------
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Could not find input CSV at:\n  {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    if "year" not in df.columns or "fall" not in df.columns:
        raise ValueError(
            "Input CSV must contain at least 'year' and 'fall' columns.\n"
            f"Columns found: {list(df.columns)}"
        )

    n_original = len(df)

    # -------------------------
    # (1) Eliminate missing/invalid year values
    #     by extracting a 3–4 digit year from the raw 'year' field.
    # -------------------------
    df["year_int"] = df["year"].apply(extract_year_from_string).astype("Int64")
    df = df.dropna(subset=["year_int"])

    # -------------------------
    # (4) Keep only Fell / Found
    # -------------------------
    df["fall_clean"] = df["fall"].astype(str).str.strip().str.title()
    df = df[df["fall_clean"].isin(["Fell", "Found"])]

    # -------------------------
    # (2) Drop exact duplicate rows
    # -------------------------
    df = df.drop_duplicates()

    # -------------------------
    # (3) Eliminate rows with year > 2013
    # -------------------------
    df = df[df["year_int"] <= 2013]

    n_after_filters = len(df)

    # -------------------------
    # Aggregate: year -> count of Fell/Found
    # -------------------------
    grouped = (
        df.groupby("year_int")
          .size()
          .reset_index(name="num_fell_found")
          .sort_values("year_int")
    )

    # Rename year column to just 'year' for final output
    grouped = grouped.rename(columns={"year_int": "year"})

    # -------------------------
    # Save to CSV
    # -------------------------
    grouped.to_csv(OUTPUT_CSV, index=False)

    # Console summary
    print("Refactor complete.")
    print(f"Input file : {INPUT_CSV.resolve()}")
    print(f"Output file: {OUTPUT_CSV.resolve()}")
    print(f"Original rows          : {n_original}")
    print(f"Rows after all filters : {n_after_filters}")
    print(f"Distinct years in output: {len(grouped)}")
    print("\nFirst few rows of output:")
    print(grouped.head())


if __name__ == "__main__":
    main()
