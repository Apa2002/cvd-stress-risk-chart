"""
Appendix 6 — leakage-conscious logistic-regression evaluation.

Scaling and SMOTE are fitted only within each training fold by an
imbalanced-learn Pipeline. This avoids fitting preprocessing on the test
partition and avoids applying SMOTE before cross-validation.

Usage:
    python src/06_model_evaluation.py data/6varcateg.xlsx

Expected columns:
    pORsms2cat, sms2cat, sex, DMHx, pANDDMHX, Agec, sbp, CVD5
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay, f1_score, matthews_corrcoef,
    precision_recall_curve, precision_score, recall_score, roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    StratifiedKFold, cross_val_score, train_test_split,
)
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

FEATURES = [
    "pORsms2cat", "sms2cat", "sex", "DMHx",
    "pANDDMHX", "Agec", "sbp",
]
TARGET = "CVD5"
THRESHOLD = 0.55
RANDOM_STATE = 99


def make_pipeline():
    """All learned transformations are fitted within the training fold."""
    return Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("smote", SMOTE(random_state=42)),
        ("classifier", LogisticRegression(
            C=10.0,
            class_weight="balanced",
            max_iter=1000,
            solver="liblinear",
            random_state=0,
        )),
    ])


def main(path):
    data = pd.read_excel(path)
    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    clean = data[required].dropna()
    X = clean[FEATURES]
    y = clean[TARGET].astype(int)

    if set(y.unique()) != {0, 1}:
        raise ValueError(f"{TARGET} must contain both binary classes 0 and 1.")
    if y.value_counts().min() < 2:
        raise ValueError("At least two observations per class are required.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    model = make_pipeline()
    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= THRESHOLD).astype(int)

    cm = confusion_matrix(y_test, predictions, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")

    lines = []

    def log(label, value):
        line = f"{label}: {value}"
        print(line)
        lines.append(line)

    log("Rows after dropping missing values", len(clean))
    log("Training rows", len(X_train))
    log("Test rows", len(X_test))
    log("Decision threshold", THRESHOLD)
    log("Accuracy", f"{accuracy_score(y_test, predictions):.4f}")
    log("Precision", f"{precision_score(y_test, predictions, zero_division=0):.4f}")
    log("Recall / Sensitivity", f"{recall_score(y_test, predictions, zero_division=0):.4f}")
    log("F1-score", f"{f1_score(y_test, predictions, zero_division=0):.4f}")
    log("ROC-AUC", f"{roc_auc_score(y_test, probabilities):.4f}")
    log("Specificity", f"{specificity:.4f}")
    log("MCC", f"{matthews_corrcoef(y_test, predictions):.4f}")
    log("Confusion matrix (rows=true [0,1], columns=predicted [0,1])", cm.tolist())
    lines.append("\nClassification report:\n" + classification_report(
        y_test, predictions, zero_division=0
    ))

    # Stratified CV: scaling and SMOTE are refitted independently in each fold.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    log("5-fold stratified CV accuracy", np.round(cv_scores, 4).tolist())
    log("Mean 5-fold CV accuracy", f"{cv_scores.mean():.4f}")
    log("CV standard deviation", f"{cv_scores.std():.4f}")

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, label=f"ROC-AUC = {roc_auc_score(y_test, probabilities):.3f}")
    ax.plot([0, 1], [0, 1], "k--", label="Chance")
    ax.set(xlim=(0, 1), ylim=(0, 1.05),
           xlabel="False Positive Rate", ylabel="True Positive Rate",
           title="Receiver Operating Characteristic")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(RESULTS / "roc_curve.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # Precision-recall curve
    precision, recall, _ = precision_recall_curve(y_test, probabilities)
    ap = average_precision_score(y_test, probabilities)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(recall, precision, label=f"Average precision = {ap:.3f}")
    ax.set(xlim=(0, 1), ylim=(0, 1.05),
           xlabel="Recall", ylabel="Precision",
           title="Precision–Recall Curve")
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(RESULTS / "precision_recall_curve.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No CVD", "CVD"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    fig.savefig(RESULTS / "confusion_matrix.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    (RESULTS / "metrics.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved evaluation outputs to {RESULTS}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/6varcateg.xlsx"
    main(input_path)
