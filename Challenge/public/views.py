from flask import redirect, request, send_from_directory, render_template, make_response,send_file
from app import app
import sqlite3
from base64 import b64decode,b64encode
import os

def checkSecret(_email, _password):	
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
  
    cursor_obj = connection_obj.cursor()
    
    cursor_obj.execute(f"SELECT * FROM USERS WHERE email = ? AND password = ?", (_email, _password))
    result = cursor_obj.fetchone()

    if result:
        return True
    else:
        return False

def registerAccount(_email, _password):
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
    
    connection_obj.execute("INSERT INTO USERS (email,password) VALUES (?, ?)", (_email, _password))
    connection_obj.commit()
    
    connection_obj.close()

def checkUser(_email):
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
  
    cursor_obj = connection_obj.cursor()
    
    cursor_obj.execute(f"SELECT * FROM USERS WHERE email = ?", [_email])
    result = cursor_obj.fetchone()

    if result:
        return True
    else:
        return False

def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def generateCookie(email):
    return b64encode(strxor(os.environ['SECRET_KEY'], email).encode('ascii')).decode('ascii')

def decodeCookie(cookie):
    try:
        user = strxor(os.environ['SECRET_KEY'], b64decode(cookie).decode('ascii'))
        return user
    except:
        return ""

@app.route('/', methods=['GET'])
def home():
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            return render_template('home.html') if user != "admin@ua.pt" else redirect("/admin")
        else:
            res = make_response(redirect("/login"))
            res.set_cookie('value', '', expires=0)
            return res
    else:
        return redirect("/login")

@app.route('/admin', methods=['GET'])
def admin():
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            return redirect("/") if user != "admin@ua.pt" else render_template('admin.html')
        else:
            res = make_response(redirect("/login"))
            res.set_cookie('value', '', expires=0)
            return res
    else:
        return redirect("/login")

@app.route('/admin', methods=['POST'])
def malware_sample():
    cookie = request.cookies.get('value')
    if cookie:
        user = decodeCookie(cookie)
        if user and checkUser(user):
            if user == "admin@ua.pt":
                filename=request.form.get("file")
                filename = filename.replace("../","")
                if filename:
                    try:
                        return send_file('/challenge/app/data/'+filename, as_attachment=False)
                    except FileNotFoundError:
                        return redirect("/admin")
                else:
                    return redirect("/admin")
            else:
                return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        cookie = request.cookies.get('value')
        if cookie:
            user = decodeCookie(cookie)
            if user and checkUser(user):
                return redirect("/") if user != "admin@ua.pt" else redirect("/admin")
            else:
                res = make_response(redirect("/login"))
                res.set_cookie('value', '', expires=0)
                return res

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if checkSecret(email, password):
            res = make_response(redirect("/"))
            res.set_cookie("value", generateCookie(email))
            
            return res

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        cookie = request.cookies.get('value')
        if cookie:
            user = decodeCookie(cookie)
            if user and checkUser(user):
                return redirect("/") if user != "admin@ua.pt" else redirect("/admin")
            else:
                res = make_response(redirect("/register"))
                res.set_cookie('value', '', expires=0)
                return res

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        if not checkUser(email):
            registerAccount(email, password)
            res = make_response(redirect("/"))
            res.set_cookie("value", generateCookie(email))

            return res
    
    return render_template('register.html')

@app.route('/robots.txt', methods=['GET'])
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout', methods=['GET'])
def logout():
    res = make_response(redirect("/login"))
    res.set_cookie('value', '', expires=0)
    return res