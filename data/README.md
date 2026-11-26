# data/

این پوشه فقط برای فایل‌های داده است و **محتوای آن روی گیت‌هاب آپلود نمی‌شود** (در `.gitignore` نادیده گرفته شده؛ فقط همین فایل و `.gitkeep` ردیابی می‌شوند).

The raw data (Isfahan Healthy Heart Program + PHQ-4) are private. Put your local copies here:

| File | Used by | Description |
|------|---------|-------------|
| `data1.csv` | `01_merge_data.py` | main cohort data (key: `IHHPCode`) |
| `data2.csv` | `01_merge_data.py` | PHQ-4 questionnaire (`Sg3`, `Sg8`, `PHQ2`) |
| `preprocessed_data.xlsx` | `02_descriptive_table.R` | merged data, missing rows removed (N = 3277) |
| `final_data.xlsx` | `03_…`, `04_…` | data with the 32 stress-combination variables |
| `6varcateg.xlsx` | `06_model_evaluation.py` | the 7 selected model variables + `CVD5` |

## Main columns

`Age`, `sex`, `DMHx` (diabetes), `sms2cat` (smoking), `sbpcat2/3/4` (systolic BP groups),
`WHR2/3/4`, `PHQ2` (stress), `Follow`, `CVD5` (outcome), and logical combinations
`pAND…` / `pOR…` (AND / OR of stress with another variable), `Agec` (age category), `sbp`.
