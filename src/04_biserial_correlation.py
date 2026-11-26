"""
پیوست ۴ - همبستگی بای‌سریال بین متغیر پیوسته (سن) و متغیرهای دوحالته
Biserial correlation between a continuous variable (Age) and binary variables.

Usage:
    python src/04_biserial_correlation.py data/final_data.xlsx
"""
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm

CONTINUOUS_VAR = "Age"
BINARY_VARS = [
    "sex", "DMHx", "sms2cat", "sbpcat2", "sbpcat3", "sbpcat4",
    "pORsex", "pANDDMHX", "pORDMHX", "pORsms2cat",
    "pANDsbpcat2", "pANDsbpcat3", "pANDsbpcat4",
    "pORsbpcat2", "pORsbpcat3", "pORsbpcat4",
]


def biserial_correlation(dichotomous, continuous):
    d = np.asarray(dichotomous)
    x = np.asarray(continuous, dtype=float)
    p = d.mean()
    q = 1 - p
    mean1, mean0 = x[d == 1].mean(), x[d == 0].mean()
    std = x.std(ddof=1)
    y = norm.pdf(norm.ppf(p))  # ordinate of the normal curve at the p-quantile
    return (mean1 - mean0) / std * (p * q) / y


def calculate_biserial_correlations(df, continuous_var, binary_vars):
    return {v: biserial_correlation(df[v], df[continuous_var]) for v in binary_vars}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/final_data.xlsx"
    df = pd.read_excel(path)
    for var, r in calculate_biserial_correlations(df, CONTINUOUS_VAR, BINARY_VARS).items():
        print(f"Biserial correlation between {var} and {CONTINUOUS_VAR}: {r:.4f}")
