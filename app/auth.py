# Unicorn 
# Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
# Softdev 2026

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from db import select_query, insert_query #using SQL until mongoDB fleshed out
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

uri = "mongodb://Cluster17576:ZFhsTF5SZmZa@ac-cm2kdg3-shard-00-00.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-01.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-02.b6r6yys.mongodb.net:27017/?ssl=true&replicaSet=atlas-tl4q5z-shard-0&authSource=admin&appName=Cluster17576"
# yes i know mongo yells at me for having this public but what is anyone really going to do with this
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["data"]

@bp.get('/register')
def signup_get():
    return render_template('auth/register.html')

@bp.post('/register')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor = db.profiles.find_one({"name":username})
    if cursor != None:
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.signup_get'))   
    hashed_password = generate_password_hash(password)
    db.profiles.insert_one({"name":username, "password":hashed_password})
    flash('Sign up successful! Please log in.', 'success')
    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():
    return render_template('auth/login.html')

@bp.post('/login')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor = db.profiles.find_one({"name":username})
    if cursor != None and check_password_hash(cursor['password'], password):
        session['username'] = username
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('home_get'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('auth.login_get'))

@bp.get('/logout')
def logout_get():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login_get'))


