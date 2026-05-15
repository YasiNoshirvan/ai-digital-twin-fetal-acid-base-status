import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
)


def regression_metrics(y_true, y_pred):
    """
    Compute regression metrics.
    """
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": mean_squared_error(y_true, y_pred, squared=False),
        "R2": r2_score(y_true, y_pred),
    }


def classification_metrics(y_true, y_prob, threshold=0.5):
    """
    Compute classification metrics for probabilistic predictions.
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)

    metrics = {
        "AUPRC": average_precision_score(y_true, y_prob),
        "AUROC": roc_auc_score(y_true, y_prob) if len(np.unique(y_true)) == 2 else np.nan,
        "Brier": brier_score_loss(y_true, y_prob),
    }

    return metrics


def expected_calibration_error(y_true, y_prob, n_bins=10):
    """
    Compute a simple Expected Calibration Error.
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        lower, upper = bins[i], bins[i + 1]
        mask = (y_prob >= lower) & (y_prob < upper)

        if mask.sum() == 0:
            continue

        bin_confidence = y_prob[mask].mean()
        bin_accuracy = y_true[mask].mean()
        bin_weight = mask.mean()

        ece += bin_weight * abs(bin_accuracy - bin_confidence)

    return float(ece)
