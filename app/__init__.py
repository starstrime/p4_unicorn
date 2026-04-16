# Unicorn
# Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
# Softdev 2026

from flask import Flask, render_template, request, session, redirect, flash, url_for, jsonify
from flask_cors import CORS
import yfinance as yf
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
CORS(app)

import auth
app.register_blueprint(auth.bp)

@app.get('/')
def home_get():
    return render_template("home.html")

@app.get('/barChart')
def barChart_get():
    return render_template("bar_chart.html")

@app.get('/bollinger')
def bollinger_get():
    return render_template("bollinger.html")

@app.get('/lineChart')
def lineChart_get():
    return render_template("line_chart.html")

@app.route('/data')
def get_data():
    tickers = ['AAPL', 'NVDA', 'TSLA', 'MSFT', 'AMZN', 'META']
    rows = []
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(period='10y', interval='3mo')
        shares_outstanding = yf.Ticker(ticker).info['sharesOutstanding']
        hist['Market_cap'] = hist['Close'] * shares_outstanding
        for date, row in hist.iterrows():
            rows.append({
                'date': date.strftime('%Y-%m-%d'),
                'name': ticker,
                'category': 'Technology',
                'value': round(row['Market_cap'], 2)
            })

    rows.sort(key=lambda x: x['date'])
    return jsonify(rows)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
