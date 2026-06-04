"""Generate report-ready confusion matrix from the Skill Lantern model flow."""

from __future__ import annotations

import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.dirname(SCRIPT_DIR)
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

import train_model  # noqa: E402


def main() -> None:
    data_path = os.path.join(BACKEND_ROOT, "app", "data", "career_recommender.csv")
    output_dir = os.path.join(BACKEND_ROOT, "app", "data")
    os.makedirs(output_dir, exist_ok=True)

    df = train_model.load_and_preprocess_data(data_path)
    X, y, feature_cols, le_career, *_ = train_model.prepare_features(df)
    model, _X_train, X_test, _y_train, y_test = train_model.train_model(X, y, feature_cols)

    y_pred = model.predict(X_test)
    labels = np.arange(len(le_career.classes_))
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # Full multiclass matrices are often unreadable in a report. Use the
    # highest-support classes for the figure and save the complete matrix as CSV.
    support = cm.sum(axis=1)
    top_n = min(12, len(labels))
    top_indices = np.argsort(support)[::-1][:top_n]
    top_indices = np.sort(top_indices)

    cm_top = cm[np.ix_(top_indices, top_indices)]
    class_names = [str(le_career.classes_[i]) for i in top_indices]
    cm_norm = cm_top.astype(float)
    row_sums = cm_norm.sum(axis=1, keepdims=True)
    cm_norm = np.divide(cm_norm, row_sums, out=np.zeros_like(cm_norm), where=row_sums != 0)

    fig_path = os.path.join(output_dir, "confusion_matrix_top_classes.png")
    csv_path = os.path.join(output_dir, "confusion_matrix_full.csv")

    plt.figure(figsize=(12, 10))
    im = plt.imshow(cm_norm, interpolation="nearest", cmap="Blues", vmin=0, vmax=1)
    plt.title("Skill Lantern Confusion Matrix - Top Career Classes")
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Normalised by true class")
    plt.xticks(np.arange(top_n), class_names, rotation=45, ha="right", fontsize=8)
    plt.yticks(np.arange(top_n), class_names, fontsize=8)
    plt.xlabel("Predicted Career")
    plt.ylabel("Actual Career")

    threshold = cm_norm.max() / 2 if cm_norm.size else 0
    for i in range(top_n):
        for j in range(top_n):
            count = cm_top[i, j]
            if count == 0:
                continue
            text = f"{count}\n{cm_norm[i, j]:.2f}"
            color = "white" if cm_norm[i, j] > threshold else "black"
            plt.text(j, i, text, ha="center", va="center", color=color, fontsize=7)

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["actual\\predicted", *le_career.classes_])
        for idx, row in enumerate(cm):
            writer.writerow([le_career.classes_[idx], *row.tolist()])

    print("CONFUSION_MATRIX_IMAGE=" + fig_path)
    print("CONFUSION_MATRIX_CSV=" + csv_path)


if __name__ == "__main__":
    main()
