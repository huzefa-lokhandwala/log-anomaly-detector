import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
)

def parse_log_file(filepath):
    records = []

    with open(filepath, 'r', errors='ignore') as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if match:
                records.append(match.groupdict())

    if not records:
        print("No lines matched. Check your log file format.")
        return None

    df = pd.DataFrame(records)

    df['time'] = pd.to_datetime(df['time'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df['status'] = pd.to_numeric(df['status'])
    df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0)

    df = df.dropna(subset=['time'])
    df = df.sort_values('time').reset_index(drop=True)

    return df

def extract_features(df, window='1h'):
    df = df.copy()
    df = df.set_index('time')

    features = pd.DataFrame()

    features['total_requests'] = df['status'].resample(window).count()
    features['error_count'] = df[df['status'] >= 400]['status'].resample(window).count()
    features['error_500_count'] = df[df['status'] == 500]['status'].resample(window).count()
    features['unique_ips'] = df['ip'].resample(window).nunique()
    features['avg_size'] = df['size'].resample(window).mean()

    features = features.fillna(0)
    features['error_rate'] = features['error_count'] / features['total_requests'].replace(0, 1)

    return features
