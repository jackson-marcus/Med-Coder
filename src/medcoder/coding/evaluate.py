"""Top-k accuracy eval on the synthetic note set -> MLflow.

Usage:
    python -m medcoder.coding.evaluate
"""

from __future__ import annotations

import logging

import mlflow
import pandas as pd

from medcoder.coding.suggest import suggest_codes
from medcoder.settings import get_config, get_settings, resolve_path

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = get_config()
    notes = pd.read_parquet(resolve_path(cfg["data"]["processed_dir"]) / "notes.parquet")

    mlflow.set_tracking_uri(get_settings().mlflow_tracking_uri)
    mlflow.set_experiment(cfg["eval"]["experiment_name"])

    top1 = top3 = top5 = 0
    for _, row in notes.iterrows():
        suggestions = [s["code"] for s in suggest_codes(row["note"], top_k=5)]
        if suggestions[:1] == [row["true_code"]]:
            top1 += 1
        if row["true_code"] in suggestions[:3]:
            top3 += 1
        if row["true_code"] in suggestions[:5]:
            top5 += 1

    n = len(notes)
    metrics = {"top1_accuracy": top1 / n, "top3_accuracy": top3 / n, "top5_accuracy": top5 / n}
    with mlflow.start_run(run_name="hybrid-retrieval"):
        mlflow.log_params({"n_notes": n, "n_codes": notes["true_code"].nunique()})
        mlflow.log_metrics(metrics)
    logger.info("top1 %.3f | top3 %.3f | top5 %.3f", *metrics.values())


if __name__ == "__main__":
    main()
