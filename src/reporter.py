def generate_report(results, output_path='reports/report.html'):
    anomalies = results[results['is_anomaly'] == True].copy()
    total_windows = len(results)
    total_anomalies = len(anomalies)

    rows = ""
    for time, row in anomalies.iterrows():
        severity = "critical" if row['anomaly_score'] >= 4 else "warning"
        color = "#ff4d4d" if severity == "critical" else "#ffa500"
        rows += f"""
        <tr>
            <td>{time.strftime('%Y-%m-%d %H:%M')}</td>
            <td>{int(row['total_requests'])}</td>
            <td>{int(row['error_count'])}</td>
            <td>{row['error_rate']:.1%}</td>
            <td style="color:{color}; font-weight:bold;">{row['anomaly_score']:.2f}</td>
            <td style="color:{color}; font-weight:bold;">{severity.upper()}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log Anomaly Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f9f9f9; }}
            h1 {{ color: #222; }}
            .summary {{ display: flex; gap: 24px; margin: 24px 0; }}
            .card {{ background: white; border-radius: 8px; padding: 20px 28px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
            .card h2 {{ margin: 0 0 6px; font-size: 14px; color: #666; font-weight: normal; }}
            .card p {{ margin: 0; font-size: 32px; font-weight: bold; color: #222; }}
            table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
            th {{ background: #222; color: white; padding: 12px 16px; text-align: left; font-size: 13px; }}
            td {{ padding: 12px 16px; border-bottom: 1px solid #eee; font-size: 14px; }}
            tr:last-child td {{ border-bottom: none; }}
            tr:hover td {{ background: #f5f5f5; }}
        </style>
    </head>
    <body>
        <h1>Log Anomaly Detection Report</h1>
        <div class="summary">
            <div class="card"><h2>Windows analyzed</h2><p>{total_windows}</p></div>
            <div class="card"><h2>Anomalies detected</h2><p style="color:#ff4d4d">{total_anomalies}</p></div>
            <div class="card"><h2>Detection threshold</h2><p>Z ≥ 2.5</p></div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Time window</th>
                    <th>Total requests</th>
                    <th>Errors</th>
                    <th>Error rate</th>
                    <th>Anomaly score</th>
                    <th>Severity</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"Report saved → {output_path}")