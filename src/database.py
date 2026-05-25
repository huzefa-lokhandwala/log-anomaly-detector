import sqlite3
from datetime import datetime

DB_PATH = 'anomalies.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anomalies (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            log_file        TEXT,
            time_window     TEXT,
            total_requests  INTEGER,
            error_count     INTEGER,
            error_rate      REAL,
            anomaly_score   REAL,
            severity        TEXT,
            UNIQUE(log_file, time_window)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            log_file          TEXT,
            scanned_at        TEXT,
            windows_analyzed  INTEGER,
            anomalies_found   INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def save_anomalies(results, log_file):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    anomalies = results[results['is_anomaly'] == True]
    new_count = 0

    for time_window, row in anomalies.iterrows():
        try:
            cursor.execute('''
                INSERT INTO anomalies
                (log_file, time_window, total_requests, error_count, error_rate, anomaly_score, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                log_file,
                str(time_window),
                int(row['total_requests']),
                int(row['error_count']),
                round(row['error_rate'], 4),
                round(row['anomaly_score'], 4),
                'CRITICAL' if row['anomaly_score'] >= 4 else 'WARNING'
            ))
            new_count += 1
        except sqlite3.IntegrityError:
            pass

    cursor.execute('''
        INSERT INTO scan_history
        (log_file, scanned_at, windows_analyzed, anomalies_found)
        VALUES (?, ?, ?, ?)
    ''', (
        log_file,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(results),
        len(anomalies)
    ))

    conn.commit()
    conn.close()
    print(f"New anomalies saved: {new_count}")
    print(f"Scan recorded in history.")

def get_all_anomalies():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM anomalies ORDER BY anomaly_score DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_scan_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scan_history ORDER BY scanned_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM anomalies')
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM anomalies WHERE severity = 'CRITICAL'")
    critical = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM scan_history')
    total_scans = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(DISTINCT log_file) FROM scan_history')
    log_files = cursor.fetchone()[0]

    conn.close()
    return {
        'total_anomalies': total,
        'critical_count': critical,
        'total_scans': total_scans,
        'log_files_analyzed': log_files
    }

def get_chart_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT time_window, error_rate, anomaly_score
        FROM anomalies
        ORDER BY time_window ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows