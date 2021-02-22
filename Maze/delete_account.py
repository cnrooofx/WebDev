#!/usr/local/bin/python3

from os import environ
from shelve import DbfilenameShelf
from http.cookies import SimpleCookie
from cgi import FieldStorage, escape
import pymysql as db
from hashlib import sha256

from cgitb import enable
enable()

print('Content-Type: text/html')
print()

result = """
   <section>
       <p>You are not logged in.</p>
       <p>
           <a href="login.py">Login</a> &vert; <a href="accounts/register.py">Register</a>
       </p>
   </section>"""

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = DbfilenameShelf('sessions/sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                message = ''
                form_data = FieldStorage()
                username = session_store.get('username')
                form = """<p>
                    Hey, %s. Sorry to see you go.
                </p>
                <p>
                    <strong>Warning! This action is permenant.</strong> All of your scores will be lost.
                </p>
                <form action="delete_account.py" method="post">
                    <label for="pass1">Enter password: </label>
                    <input type="password" name="pass1" id="pass1" placeholder="Enter password" required />
                    <label for="pass2">Reenter password: </label>
                    <input type="password" name="pass2" id="pass2" placeholder="Reenter password" required />
                    <label for="confirm">Confirm Deletion: </label>
                    <input type="checkbox" name="confirm" id="confirm" value="yes" />
                    <input type="submit" value="Delete Account" />
                </form>""" % username
                if len(form_data) != 0:
                    pass1 = escape(form_data.getfirst('pass1', '').strip())
                    pass2 = escape(form_data.getfirst('pass2', '').strip())
                    confirm = escape(form_data.getfirst('confirm', '').strip())
                    if confirm == 'yes':
                        if pass1 == pass2:
                            sha256_password = sha256(pass1.encode()).hexdigest()
                            connection = db.connect('', '', '', '')
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""SELECT * FROM users
                                              WHERE username = %s
                                              AND password = %s""", (username, sha256_password))
                            if cursor.rowcount == 0:
                                message = '<p><strong>Error! Incorrect password.</strong></p>'
                            else:
                                cursor.execute("""DELETE
                                                  FROM users
                                                  WHERE username = %s
                                                  AND password = %s""", (username, sha256_password))
                                connection.commit()
                                cursor.execute("""DELETE
                                                  FROM leaderboard
                                                  WHERE username = %s""", username)
                                connection.commit()
                                session_store['authenticated'] = False
                                form = ''
                                message = '<p>Your account has been successfully deleted.</p>'
                            cursor.close()
                            connection.close()
                        else:
                            message = '<p><strong>Error! Passwords must match.</strong></p>'
                    else:
                        message = '<p><strong>Error! Please check the box to confirm deletion.</strong></p>'
                result = """<section>
                    <h2>Delete Account</h2>"""
                result += form
                result += message
                result += '</section>'
            session_store.close()
except (db.Error, IOError):
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Delete Account</title>
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
                %s
            </main>
        </body>
    </html>""" % (result))
