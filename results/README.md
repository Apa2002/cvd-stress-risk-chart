# results/

Generated figures and summary outputs are written here.

The revised risk-chart script creates:
- `risk_chart_diabetes_model_score.png`
- `risk_chart_no_diabetes_model_score.png`

These are labelled as model scores by default because the source appendix uses an intercept of zero. They must not be interpreted as calibrated absolute clinical risks unless the SPSS Constant has been verified and supplied through `CVD_INTERCEPT`.

The revised model-evaluation script creates:
- `roc_curve.png`
- `precision_recall_curve.png`
- `confusion_matrix.png`
- `metrics.txt`

Only commit aggregate outputs that are approved for sharing. Never commit participant-level or identifiable data. Excel workbooks are ignored by `.gitignore` by default.
