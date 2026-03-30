from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.get('/')
def home():
    return "temp"

if __name__ == '__main__':
    app.run(debug=True) #disable true later
