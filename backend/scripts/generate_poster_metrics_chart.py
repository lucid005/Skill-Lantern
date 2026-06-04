"""Generate poster-ready bar chart from actual Skill Lantern model metrics."""

from __future__ import annotations

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, top_k_accuracy_score

# Allow importing train_model.py from backend root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.dirname(SCRIPT_DIR)
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

import train_model  # noqa: E402


def main() -> None:
    data_path = os.path.join(BACKEND_ROOT, "app", "data", "career_recommender.csv")

    # Run the same preprocessing/training flow used by the project.
    df = train_model.load_and_preprocess_data(data_path)
    X, y, feature_cols, le_career, *_ = train_model.prepare_features(df)

    cv_mean = train_model.cross_validate_model(X, y)
    model, _X_train, X_test, _y_train, y_test = train_model.train_model(X, y, feature_cols)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    test_acc = accuracy_score(y_test, y_pred)
    top3 = top_k_accuracy_score(y_test, y_proba, k=min(3, len(le_career.classes_)))
    top5 = top_k_accuracy_score(y_test, y_proba, k=min(5, len(le_career.classes_)))

    metrics = {
        "CV Mean Accuracy": cv_mean * 100,
        "Test Accuracy": test_acc * 100,
        "Top-3 Accuracy": top3 * 100,
        "Top-5 Accuracy": top5 * 100,
    }

    output_dir = os.path.join(BACKEND_ROOT, "app", "data")
    os.makedirs(output_dir, exist_ok=True)

    # Save numeric values too, so they can be reused in the poster text.
    metrics_json_path = os.path.join(output_dir, "poster_model_metrics.json")
    with open(metrics_json_path, "w", encoding="utf-8") as f:
        json.dump({k: round(v, 2) for k, v in metrics.items()}, f, indent=2)

    chart_path = os.path.join(output_dir, "poster_model_metrics_bar.png")

    labels = list(metrics.keys())
    values = list(metrics.values())
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors)
    plt.ylim(0, 100)
    plt.ylabel("Accuracy (%)")
    plt.title("Skill Lantern Model Performance Metrics")

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{value:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()

    print("CHART_PATH=" + chart_path)
    print("METRICS_JSON=" + metrics_json_path)
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}%")


if __name__ == "__main__":
    main()
