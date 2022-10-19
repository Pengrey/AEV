from flask import redirect, request, send_from_directory, render_template, make_response
from app import app
import sqlite3
from base64 import b64decode,b64encode
import re

def checkSecret(_username, _password):	
    # connection object
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
  
    # cursor object
    cursor_obj = connection_obj.cursor()
    
    cursor_obj.execute(f"SELECT * FROM USERS WHERE username = ? AND password = ?", (_username, _password))
    result = cursor_obj.fetchone()

    if result:
        return True
    else:
        return False

def checkUser(_username):
    # connection object
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
  
    # cursor object
    cursor_obj = connection_obj.cursor()
    
    cursor_obj.execute(f"SELECT * FROM USERS WHERE username = ?", (_username))
    result = cursor_obj.fetchone()

    if result:
        return True
    else:
        return False

def strxor(a, b):     
    # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def generateCookie(username):
    return b64encode(strxor(app.config['SECRET_KEY'], username).encode('ascii')).decode('ascii')

def decodeCookie(cookie):
    try:
        return strxor(app.config['SECRET_KEY'], b64decode(cookie).decode('ascii'))
    except:
        return ""

@app.route('/', methods=['GET'])
def home():
    # Check if user is already logged in
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            return render_template('home.html') if user != "admin" else redirect("/admin")
        else:
            res.set_cookie('value', '', expires=0)
            return redirect("/login")
    else:
        return redirect("/login")

@app.route('/login', methods=['GET'])
def login():
    # Check if user is already logged in
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            return redirect("/") if user != "admin" else redirect("/admin")
        else:
            res = make_response(redirect("/login"))
            res.set_cookie('value', '', expires=0)
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    # Check if user is already logged in
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            return redirect("/") if user != "admin" else redirect("/admin")
        else:
            res = make_response(redirect("/register"))
            res.set_cookie('value', '', expires=0)
    return render_template('register.html')

# robots.txt file
@app.route('/robots.txt', methods=['GET'])
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404