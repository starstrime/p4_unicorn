# Unicorn 
# Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
# Softdev 2026

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
lobbies = {}

@bp.get('/signup')
def signup_get():

    return render_template('auth/signup.html')

@bp.post('/signup')
def signup_post():

    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():

    return render_template('auth/login.html')

@bp.post('/login')
def login_post():

    return redirect(url_for('auth.login_get'))

@bp.get("/logout")
def logout_get():

    return redirect(url_for("auth.login_get"))


