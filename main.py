import argparse
from src.parser import parse_log_file, extract_features
from src.detector import detect_anomalies
from src.reporter import generate_report
from src.database import init_db, save_anomalies

def main():
    parser = argparse.ArgumentParser(
        description='Intelligent Log Anomaly Detector',
        epilog='Example: python3 main.py --file data/apache.log --window 1h --threshold 2.5'
    )

    parser.add_argument('--file', required=True, help='Path to log file')
    parser.add_argument('--window', default='1h', help='Time window size')
    parser.add_argument('--threshold', type=float, default=2.5, help='Z-score threshold')
    parser.add_argument('--output', default='reports/report.html', help='Output report path')

    args = parser.parse_args()

    init_db()

    print(f"\n→ Loading log file: {args.file}")
    df = parse_log_file(args.file)

    if df is None:
        print("Failed to parse log file. Exiting.")
        return

    print(f"→ Extracting features (window: {args.window})")
    features = extract_features(df, window=args.window)

    print(f"→ Detecting anomalies (threshold: {args.threshold})")
    results = detect_anomalies(features, threshold=args.threshold)

    anomalies = results[results['is_anomaly'] == True]
    print(f"\n✓ Windows analyzed : {len(results)}")
    print(f"✓ Anomalies found  : {len(anomalies)}")

    save_anomalies(results, args.file)
    generate_report(results, output_path=args.output)
    print(f"✓ Report saved     : {args.output}\n")

if __name__ == '__main__':
    main()