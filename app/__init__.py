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

def check_logged_in():
    return 'username' in session

@app.get('/')
def home_get():
    return render_template("home.html", logged_in=check_logged_in())

@app.get('/barChart')
def barChart_get():
    return render_template("bar_chart.html", logged_in=check_logged_in())

@app.get('/bollinger')
def bollinger_get():
    return render_template("bollinger.html", logged_in=check_logged_in())

@app.get('/lineChart')
def lineChart_get():
    return render_template("line_chart.html", logged_in=check_logged_in())

@app.route("/bar_chart_data")
def bar_chart_data():
    tickers = request.args.get("tickers", "AAPL,MSFT,GOOGL,AMZN,META,TSLA,NVDA,JPM,V,WMT").split(",")
    start   = request.args.get("start", "2015-01-01")
    end     = request.args.get("end",   "2024-01-01")

    records = []
    for ticker in tickers:
        tk = yf.Ticker(ticker)

        # shares outstanding is a scalar
        shares = tk.info.get("sharesOutstanding", None)
        if shares is None:
            continue

        # quarterly price history at 3mo interval
        hist = tk.history(start=start, end=end, interval="3mo")
        if hist.empty:
            continue

        for date, row in hist.iterrows():
            market_cap = row["Close"] * shares / 1e9   # in $B
            records.append({
                "date":  date.strftime("%Y-%m-%d"),
                "name":  ticker,
                "value": round(market_cap, 2)
            })

    return jsonify(records)

@app.route("/stock_data")
def get_stock():
    ticker = request.args.get("ticker", "AAPL")
    start  = request.args.get("start",  "2020-01-01")
    end    = request.args.get("end",    "2024-01-01")

    df = yf.download(ticker, start=start, end=end)
    df.columns = df.columns.get_level_values(0)
    df = df.reset_index()[["Date", "Close"]]
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["Close"] = df["Close"].astype(float)

    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
