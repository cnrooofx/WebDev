#!/usr/local/bin/python3

from cgi import FieldStorage, escape
from os import environ
from shelve import DbfilenameShelf
from time import time
from hashlib import sha256
from random import randint
import pymysql as db
from http.cookies import SimpleCookie

from send_email import reset_email

from cgitb import enable
enable()

form_data = FieldStorage()

form = """<form action="forgot.py" method="post">
    <label for="username">Username: </label>
    <input type="text" name="username" id="username" value="" />
    <input type="submit" value="Reset Password" />
</form>"""
result = ''

if len(form_data) != 0:
    try:
        cookie = SimpleCookie()
        http_cookie_header = environ.get('HTTP_COOKIE')
        if not http_cookie_header:
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['reset'] = sid
        else:
            cookie.load(http_cookie_header)
            if 'reset' not in cookie:
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['reset'] = sid
            else:
                sid = cookie['reset'].value
        session_store = DbfilenameShelf('../sessions/reset_' + sid, writeback=True)
        if session_store.get('code'):
            code = escape(form_data.getfirst('code', '').strip())
            if code:
                form = """<form action="forgot.py" method="post">
                        <label for="code">Code: </label>
                        <input type="number" name="code" id="code" min="0" max="99999" value="%s" required />
                        <label for="pass1">Enter new password: </label>
                        <input type="password" name="pass1" id="pass1" required />
                        <label for="pass2">Reenter password: </label>
                        <input type="password" name="pass2" id="pass2" required />
                        <input type="submit" />
                    </form>""" % code
                if session_store.get('code') == code:
                    pass1 = escape(form_data.getfirst('pass1', '').strip())
                    pass2 = escape(form_data.getfirst('pass2', '').strip())
                    if len(pass1) < 8 or len(pass2) < 8:
                        result = """<p>
                            <strong>Error! Password must be at least 8 characters long.</strong>
                            </p>"""
                    elif pass1 == pass2:
                        sha256_password = sha256(pass1.encode()).hexdigest()
                        username = session_store.get('username')
                        connection = db.connect('', '', '', '')
                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""UPDATE users
                                          SET password = %s
                                          WHERE username = %s""", (sha256_password, username))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        form = ''
                        result = """<p>Your password has been successfully reset.</p>
                            <p><a href="../login.py">Click Here</a> to Login</p>"""
                    else:
                        result = '<p><strong>Error! Passwords must match.</strong></p>'
                else:
                    '<p><strong>Error! Incorrect code.</strong></p>'
            else:
                form = """<form action="forgot.py" method="post">
                        <label for="code">Code: </label>
                        <input type="number" name="code" id="code" min="0" max="99999" required />
                        <label for="pass1">Enter new password: </label>
                        <input type="password" name="pass1" id="pass1" required />
                        <label for="pass2">Reenter password: </label>
                        <input type="password" name="pass2" id="pass2" required />
                        <input type="submit" />
                    </form>"""
        else:
            username = escape(form_data.getfirst('username', '').strip())
            if not username:
                result = '<p><strong>Error! Please enter a username.</strong></p>'
            else:
                connection = db.connect('', '', '', '')
                cursor = connection.cursor(db.cursors.DictCursor)
                cursor.execute("""SELECT email
                                  FROM users
                                  WHERE username = %s""", username)
                if cursor.rowcount != 0:
                    email = cursor.fetchone()['email']
                    code = ''
                    for i in range(5):
                        code += str(randint(0, 9))
                    session_store['username'] = username
                    session_store['code'] = code
                    reset_email(username, email, code)
                form = """<form action="forgot.py" method="post">
                    <label for="code">Code: </label>
                    <input type="number" name="code" id="code" />
                    <label for="pass1">Enter new password: </label>
                    <input type="password" name="pass1" id="pass1" required />
                    <label for="pass2">Reenter password: </label>
                    <input type="password" name="pass2" id="pass2" required />
                    <input type="submit" />
                </form>"""
                result = '<p>Please check your email for the password reset code.</p>'
                cursor.close()
                connection.close()
        print(cookie)
        session_store.close()
    except (db.Error, IOError):
        result = '<p>Sorry! We are experiencing problems at the moment. Please try again later.</p>'

print('Content-Type: text/html')
print()

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="../styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Forgot Password</title>
        </head>
        <body>
            <header>
                <h1>a-MAZE-ing</h1>
                <nav>
                    <ul>
                        <li>
                            <a href="../index.html">Home</a>
                        </li>
                        <li>
                            <a href="../game.py">Play</a>
                        </li>
                        <li>
                            <a href="../leaderboard.py">Leaderboard</a>
                        </li>
                        <li>
                            <a href="../account.py">Account</a>
                        </li>
                    </ul>
                </nav>
            </header>
            <main>
                <section>
                    <h2>Reset Password</h2>
                    %s
                    %s
                </section>
            </main>
        </body>
    </html>""" % (form, result))
