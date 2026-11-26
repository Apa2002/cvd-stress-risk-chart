"""
پیوست ۱ - ادغام داده‌ها
Merge the Isfahan Healthy Heart Program (IHHP) data with the PHQ-4 data.

Inputs  (put them in ../data/, they are NOT tracked by git):
    data1.csv  - main cohort data
    data2.csv  - PHQ-4 questionnaire data (columns Sg3, Sg8, PHQ2, ...)
Output:
    data/merged_data.csv
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

data1 = pd.read_csv(DATA_DIR / "data1.csv")
data2 = pd.read_csv(DATA_DIR / "data2.csv")

# left join on the participant code
merged = pd.merge(data1, data2, on="IHHPCode", how="left")

# missing PHQ answers are marked (as in the original SPSS/R pipeline)
merged[["Sg3", "Sg8", "PHQ2"]] = merged[["Sg3", "Sg8", "PHQ2"]].fillna("#NULL! ")

merged.to_csv(DATA_DIR / "merged_data.csv", index=False)
print(f"Saved {len(merged)} rows to {DATA_DIR / 'merged_data.csv'}")
