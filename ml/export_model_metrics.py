"""Export model metrics in a Looker/BigQuery-friendly long format."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def read_metrics(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    risk = read_metrics(ROOT / "ml" / "artifacts" / "microcut_risk" / "metrics.json")
    diagnosis = read_metrics(ROOT / "ml" / "artifacts" / "metrics.json")
    rows = [
        ("MICROCUT_RISK_5M", "ROC_AUC", risk["test_roc_auc"]),
        ("MICROCUT_RISK_5M", "PR_AUC", risk["test_pr_auc"]),
        ("MICROCUT_RISK_5M", "RECALL", risk["test_recall"]),
        ("MICROCUT_RISK_5M", "PRECISION", risk["test_precision"]),
        ("MICROCUT_RISK_5M", "F1", risk["test_f1"]),
        ("MICROCUT_RISK_5M", "BALANCED_ACCURACY", risk["test_balanced_accuracy"]),
        ("ROOT_CAUSE_DIAGNOSIS", "BALANCED_ACCURACY", diagnosis["test_balanced_accuracy"]),
        ("ROOT_CAUSE_DIAGNOSIS", "MACRO_F1", diagnosis["test_macro_f1"]),
        ("ROOT_CAUSE_DIAGNOSIS", "ACCURACY", diagnosis["test_accuracy"]),
    ]
    output = pd.DataFrame(rows, columns=["model_name", "metric_name", "metric_value"])
    output["dataset_type"] = "SYNTHETIC_HOLDOUT"
    output["model_version"] = "2026-10-19"
    output.to_csv(ROOT / "data" / "ml_model_metrics.csv", index=False, encoding="utf-8-sig")
    print(output.to_string(index=False))


if __name__ == "__main__":
    main()
