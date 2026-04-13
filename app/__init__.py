# Unicorn
# Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
# Softdev 2026

from flask import Flask, render_template, request, session, redirect, flash, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

import auth
app.register_blueprint(auth.bp)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("auth/login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("auth/register.html")

@app.route('/bar_chart', methods=['GET', 'POST'])
def bar_chart():
    return render_template("bar_chart.html")

@app.route('/bollinger', methods=['GET', 'POST'])
def bollinger():
    return render_template("bollinger.html")

@app.route('/line_chart', methods=['GET', 'POST'])
def line_chart():
    return render_template("line_chart.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
