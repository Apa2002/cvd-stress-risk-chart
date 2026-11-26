"""
Appendix 7 — CVD model-score chart.

The chart enumerates all 2^5 combinations of the five binary model inputs
(sex, DMHx, sms2cat, pANDDMHX, pORsms2cat) and all 5 x 4 age/BP categories:
32 x 20 = 640 cells per complete enumeration.

IMPORTANT:
- The five binary inputs are enumerated independently to reproduce the
  640-combination design stated in the thesis. Some combinations may be
  logically inconsistent if pANDDMHX and pORsms2cat are derived from the
  same underlying stress variable. Confirm the original Appendix 7 logic
  before interpreting every panel as a realizable patient profile.
- The original MATLAB code uses intercept=0. Unless CVD_INTERCEPT is set to
  the SPSS Constant, outputs are model scores from that specified intercept,
  NOT calibrated absolute clinical risks.
- This is a research visualization, not a clinical decision-support tool.

Usage:
    python src/07_risk_chart.py

Optional:
    Windows PowerShell: $env:CVD_INTERCEPT="-X.XXXX"
    macOS/Linux:        CVD_INTERCEPT="-X.XXXX" python src/07_risk_chart.py

Outputs:
    results/risk_chart_diabetes_model_score.png
    results/risk_chart_no_diabetes_model_score.png
"""
from itertools import product
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# Coefficients transcribed from thesis Table 3-11.
AGEC_COEFFS = [-2.257, -1.453, -1.267, -0.894, 0.0]  # Agec(5) reference
SBP_COEFFS = [-1.261, -0.578, -0.294, 0.0]           # sbp(4) reference
BETA_OTHER = {
    "DMHx": 1.045,
    "sms2cat": 0.227,
    "pANDDMHX": -0.354,
    "pORsms2cat": 0.230,
    "sex": 0.190,
}
# The source appendix specifies zero. Set CVD_INTERCEPT to the SPSS Constant
# only after verifying it against the original SPSS output.
INTERCEPT = float(os.environ.get("CVD_INTERCEPT", "0"))
INTERCEPT_VERIFIED = "CVD_INTERCEPT" in os.environ


def risk(agec, sbp, cond):
    """Return the logistic model output for one categorical/binary profile."""
    if agec not in range(1, 6):
        raise ValueError("agec must be an integer from 1 to 5")
    if sbp not in range(1, 5):
        raise ValueError("sbp must be an integer from 1 to 4")
    z = INTERCEPT + AGEC_COEFFS[agec - 1] + SBP_COEFFS[sbp - 1]
    z += sum(BETA_OTHER[k] * int(cond[k]) for k in BETA_OTHER)
    # Numerically stable sigmoid
    if z >= 0:
        return 1.0 / (1.0 + np.exp(-z))
    ez = np.exp(z)
    return ez / (1.0 + ez)


def build_condition_sets():
    """Enumerate all 32 combinations of the five binary model inputs."""
    keys = ("sex", "DMHx", "sms2cat", "pANDDMHX", "pORsms2cat")
    return [dict(zip(keys, values)) for values in product((0, 1), repeat=len(keys))]


def draw(condition_sets, out_name, title, ncols=4):
    cmap = LinearSegmentedColormap.from_list(
        "gyr", ["#2e9e4f", "#f2d94e", "#d62728"]
    )
    nrows = int(np.ceil(len(condition_sets) / ncols))
    fig, axes = plt.subplots(
        nrows, ncols, figsize=(4.2 * ncols, 3.4 * nrows), squeeze=False
    )
    axes = axes.ravel()

    all_vals = [
        risk(age, sbp, cond) * 100
        for cond in condition_sets
        for sbp in range(1, 5)
        for age in range(1, 6)
    ]
    vmax = max(all_vals)

    for i, (ax, cond) in enumerate(zip(axes, condition_sets), start=1):
        grid = np.array([
            [risk(age, sbp, cond) * 100 for age in range(1, 6)]
            for sbp in range(1, 5)
        ])
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
        for row in range(4):
            for col in range(5):
                ax.text(col, row, f"{grid[row, col]:.1f}",
                        ha="center", va="center", fontsize=7)
        ax.set_xticks(range(5))
        ax.set_xticklabels([f"A{k}" for k in range(1, 6)], fontsize=7)
        ax.set_yticks(range(4))
        ax.set_yticklabels([f"SBP{k}" for k in range(1, 5)], fontsize=7)
        ax.set_title(
            f"#{i} Sex={cond['sex']} | DM={cond['DMHx']} | "
            f"Smoke={cond['sms2cat']} | AND={cond['pANDDMHX']} | "
            f"OR={cond['pORsms2cat']}",
            fontsize=7,
        )

    for ax in axes[len(condition_sets):]:
        ax.axis("off")

    fig.suptitle(title, fontsize=13)
    fig.supxlabel("Age category (A1–A5)")
    fig.supylabel("Systolic blood pressure category (SBP1–SBP4)")
    fig.tight_layout(rect=[0.02, 0.02, 1, 0.96])
    output_path = RESULTS / out_name
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_path}")


def main():
    condition_sets = build_condition_sets()
    assert len(condition_sets) == 32
    assert len(condition_sets) * 5 * 4 == 640

    if not INTERCEPT_VERIFIED:
        print(
            "WARNING: CVD_INTERCEPT is not set. Using intercept=0 from the "
            "source MATLAB appendix. Treat outputs as model scores, not "
            "calibrated absolute clinical risks."
        )

    for diabetes_value, filename, label in (
        (1, "risk_chart_diabetes_model_score.png", "With diabetes"),
        (0, "risk_chart_no_diabetes_model_score.png", "Without diabetes"),
    ):
        subset = [c for c in condition_sets if c["DMHx"] == diabetes_value]
        draw(
            subset,
            filename,
            f"CVD model-score chart — {label} "
            f"(intercept={INTERCEPT:g}; not necessarily calibrated risk)",
        )


if __name__ == "__main__":
    main()
