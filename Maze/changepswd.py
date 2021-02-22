#!/usr/local/bin/python3

from os import environ
from cgi import FieldStorage
from hashlib import sha256
from shelve import DbfilenameShelf
from html import escape
import pymysql as db
from http.cookies import SimpleCookie

from cgitb import enable
enable()

print('Content-Type: text/html')
print()

form_data = FieldStorage()

result = """
   <p><strong>You are not logged in.<strong></p>
   <p>
       <a href="login.py">Login</a> &vert; <a href="accounts/register.py">Register</a>
   </p>"""

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = DbfilenameShelf('sessions/sess_' + sid, writeback=True)
            if session_store.get('authenticated'):
                username = session_store.get('username')
                result = """<h2>Change Password</h2>
                    <form action="changepswd.py" method="post">
                        <label for="cur_pass">Enter current password: </label>
                        <input type="password" name="cur_pass" id="cur_pass" />
                        <label for="pass1">Enter new password: </label>
                        <input type="password" name="pass1" id="pass1" />
                        <label for="pass1">Reenter password: </label>
                        <input type="password" name="pass2" id="pass2" />
                        <input type="submit" />
                    </form>"""
                if len(form_data) != 0:
                    cur_password = escape(form_data.getfirst('cur_pass', '').strip())
                    password1 = escape(form_data.getfirst('pass1', '').strip())
                    password2 = escape(form_data.getfirst('pass2', '').strip())
                    current_sha256 = sha256(cur_password.encode()).hexdigest()
                    connection = db.connect('', '', '', '')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT username
                                      FROM users
                                      WHERE username = %s
                                      AND password = %s""", (username, current_sha256))
                    if cursor.rowcount == 0:
                        result += """<p>
                            <strong>Error! Your password is incorrect.</strong>
                        </p>"""
                    else:
                        if cur_password == password1 or cur_password == password2:
                            result += """<p>
                                <strong>Error! Please choose a new password.</strong>
                            </p>"""
                        elif len(password1) < 8 or len(password2) < 8:
                            result += """<p>
                                <strong>Error! Password must be at least 8 characters long.</strong>
                            </p>"""
                        elif password1 == password2:
                            sha256_password = sha256(password1.encode()).hexdigest()
                            connection = db.connect('localhost', 'cf26', 'pecah', 'cs6503_cs1106_cf26')
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""UPDATE users
                                              SET password = %s
                                              WHERE username = %s""", (sha256_password, username))
                            connection.commit()
                            session_store['authenticated'] = False
                            result = """<p>Password successfully changed. You are now logged out.</p>
                                <p><a href="login.py">Click here</a> to log in again.</p>"""
                        else:
                            result += '<p><strong>Error! Passwords do not match.</strong></p>'
                    cursor.close()
                    connection.close()
            session_store.close()
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please try again later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Change Password</title>
        </head>
        <body>
            <header>
                <h1>a-MAZE-ing</h1>
                <nav>
                    <ul>
                        <li>
                            <a href="index.html">Home</a>
                        </li>
                        <li>
                            <a href="game.py">Play</a>
                        </li>
                        <li>
                            <a href="leaderboard.py">Leaderboard</a>
                        </li>
                        <li>
                            <a href="account.py">Account</a>
                        </li>
                    </ul>
                </nav>
            </header>
            <main>
                <section>
                    %s
                </section>
            </main>
        </body>
    </html>""" % (result))
