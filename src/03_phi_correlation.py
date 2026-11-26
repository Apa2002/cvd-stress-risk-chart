"""
پیوست ۳ - همبستگی متغیرهای دوحالته با آماره فی (Phi)
Phi coefficient matrix between binary variables. Cells with phi > 0.7 are
highlighted in the Excel output (one of each highly-correlated pair is dropped).

Usage:
    python src/03_phi_correlation.py data/final_data.xlsx
Output:
    results/phi_coefficients_styled.xlsx
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from scipy.stats import chi2_contingency

RESULTS = Path(__file__).resolve().parent.parent / "results"
THRESHOLD = 0.7

BINARY_VARS = [
    "sex", "DMHx", "sms2cat", "sbpcat2", "sbpcat3", "sbpcat4",
    "PHQ2", "pORsex", "pANDDMHX", "pORDMHX", "pORsms2cat",
    "pANDsbpcat2", "pANDsbpcat3", "pANDsbpcat4", "pORsbpcat2",
    "pORsbpcat3", "pORsbpcat4",
]


def phi_coefficient(x, y):
    """phi = sqrt(chi2 / n) (unsigned) for two binary variables."""
    table = pd.crosstab(x, y)
    if table.size == 0:
        return np.nan
    chi2, _, _, _ = chi2_contingency(table)
    return float(np.sqrt(chi2 / table.to_numpy().sum()))


def main(path):
    df = pd.read_excel(path)
    phi = pd.DataFrame(index=BINARY_VARS, columns=BINARY_VARS, dtype=float)
    for a in BINARY_VARS:
        for b in BINARY_VARS:
            phi.loc[a, b] = 1.0 if a == b else phi_coefficient(df[a], df[b])

    RESULTS.mkdir(exist_ok=True)
    raw = RESULTS / "phi_coefficients.xlsx"
    styled = RESULTS / "phi_coefficients_styled.xlsx"
    phi.to_excel(raw)

    wb = load_workbook(raw)
    ws = wb.active
    red = PatternFill(start_color="FF9999", end_color="FF9999", fill_type="solid")
    n = len(BINARY_VARS)
    for r, row in enumerate(ws.iter_rows(min_row=2, min_col=2, max_row=n + 1, max_col=n + 1)):
        for c, cell in enumerate(row):
            # diagonal (r == c) is always 1, do not highlight it
            if r != c and isinstance(cell.value, float) and cell.value > THRESHOLD:
                cell.fill = red
    wb.save(styled)
    print(f"Saved {styled}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/final_data.xlsx")
