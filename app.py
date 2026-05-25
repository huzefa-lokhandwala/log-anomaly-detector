from flask import Flask, render_template
from src.database import get_all_anomalies, get_scan_history, get_summary, get_chart_data
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    summary = get_summary()
    anomalies = get_all_anomalies()
    history = get_scan_history()
    chart_rows = get_chart_data()

    labels = [row[0][:16] for row in chart_rows]
    error_rates = [round(row[1] * 100, 2) for row in chart_rows]
    scores = [round(row[2], 2) for row in chart_rows]

    return render_template('dashboard.html',
                         summary=summary,
                         anomalies=anomalies,
                         history=history,
                         labels=json.dumps(labels),
                         error_rates=json.dumps(error_rates),
                         scores=json.dumps(scores))

if __name__ == '__main__':
    app.run(debug=True)