# Log Anomaly Detector

A command-line tool that analyzes web server logs, extracts time-series features,
and automatically flags anomalous windows using statistical detection.

Built with Python, pandas, and Z-score based anomaly scoring.

---

## What it does

- Parses Apache Combined Log Format files
- Aggregates requests into configurable time windows (1h, 30min, 2h, etc.)
- Extracts features: error rate, error count, request volume, unique IPs
- Flags windows that deviate significantly from baseline (Z-score ≥ threshold)
- Generates a clean HTML report with severity classification

---

## Example output

| Time window | Requests | Errors | Error rate | Score | Severity |
|---|---|---|---|---|---|
| 2015-05-20 09:00 | 125 | 15 | 12.0% | 5.16 | CRITICAL |
| 2015-05-19 06:00 | 130 | 9 | 6.9% | 2.66 | WARNING |

---

## Setup

```bash
git clone https://github.com/huzefa-lokhandwala/log-anomaly-detector
cd log-anomaly-detector
pip install pandas
```

## Usage

```bash
python3 main.py --file data/apache.log --window 1h --threshold 2.5
```

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--file` | required | Path to log file |
| `--window` | `1h` | Time window size (1h, 30min, 2h) |
| `--threshold` | `2.5` | Z-score threshold for flagging |
| `--output` | `reports/report.html` | Output report path |

---

## Project structure

```
log-anomaly-detector/
├── data/           ← place log files here
├── reports/        ← HTML reports saved here
├── src/
│   ├── parser.py   ← log ingestion and feature extraction
│   ├── detector.py ← Z-score anomaly detection
│   └── reporter.py ← HTML report generation
└── main.py         ← CLI entry point
```

---

## How it works

Raw log lines → parsed into structured rows → aggregated into hourly windows →
Z-score computed per feature → windows exceeding threshold flagged → HTML report generated.

---

## Roadmap

- [ ] V2: SQLite persistence for anomaly history
- [ ] V2: Pattern clustering to group similar error types
- [ ] V2: Flask web dashboard with charts
- [ ] V3: Real-time log monitoring with file watchers
- [ ] V3: NLP on log messages using embeddings
- [ ] V3: Alert routing via Slack/email webhooks

---

## Sample data

Tested on public Apache log dataset (9,999 requests, 4-day window).
Download: https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs

---

Built by Huzefa Lokhandwala
B.Tech CSE (AI)
