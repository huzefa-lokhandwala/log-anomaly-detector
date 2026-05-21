import pandas as pd

FEATURES_TO_CHECK = ['error_rate', 'error_count', 'total_requests', 'unique_ips']
Z_THRESHOLD = 2.5

def compute_zscore(series):
    mean = series.mean()
    std = series.std()
    if std == 0:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - mean) / std


def detect_anomalies(features, threshold=2.5):
    results = features.copy()

    for col in FEATURES_TO_CHECK:
        results[f'z_{col}'] = compute_zscore(features[col])

    z_cols = [f'z_{col}' for col in FEATURES_TO_CHECK]
    results['anomaly_score'] = results[z_cols].max(axis=1)
    results['is_anomaly'] = results['anomaly_score'] >= threshold

    return results