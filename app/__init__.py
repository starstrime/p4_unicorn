# Unicorn 
# Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
# Softdev 2026

from flask import Flask, render_template, request, session, redirect, flash, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

import auth
app.register_blueprint(auth.bp)

@app.get('/')
def home_get():
    # return ("hi")
   return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

