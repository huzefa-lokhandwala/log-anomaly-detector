from flask import Flask, render_template
from src.database import get_all_anomalies, get_scan_history, get_summary

app = Flask(__name__)

@app.route('/')
def dashboard():
    summary = get_summary()
    anomalies = get_all_anomalies()
    history = get_scan_history()
    return render_template('dashboard.html', 
                         summary=summary, 
                         anomalies=anomalies, 
                         history=history)

if __name__ == '__main__':
    app.run(debug=True)