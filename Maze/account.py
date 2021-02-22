#!/usr/local/bin/python3

from os import environ
from shelve import DbfilenameShelf
from http.cookies import SimpleCookie
import pymysql as db

from cgitb import enable
enable()

print('Content-Type: text/html')
print()

result = """
    <section>
        <h2>Your Account</h2>
        <p><strong>You are not logged in.</strong></p>
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
                username = session_store.get('username')
                result = """
                <section>
                    <h2>Your Account</h2>
                    <p>
                        Hey, %s.
                    </p>
                    <ul>
                        <li><a href="logout.py">Logout</a></li>
                        <li><a href="changepswd.py">Change password</a></li>
                        <li><a href="delete_account.py">Delete Account</a></li>
                    </ul>
                </section>""" % username
                connection = db.connect('localhost', 'cf26', 'pecah', 'cs6503_cs1106_cf26')
                cursor = connection.cursor(db.cursors.DictCursor)
                cursor.execute("""SELECT score, score_date
                                  FROM leaderboard
                                  WHERE username = %s
                                  ORDER BY score DESC
                                  LIMIT 25""", username)
                result += '<section>'
                if cursor.rowcount == 0:
                    result += """<h2>Your Scores</h2>
                            <p>You don\'t have any scores. Get playing!</p>"""
                else:
                    result += """<table>
                        <caption>Your Scores</caption>
                        <tr>
                            <th scope="col">Score</th>
                            <th scope="col">Date</th>
                        </tr>"""
                    for row in cursor.fetchall():
                        score_date = row['score_date']
                        date = '%s/%s/%s' % (score_date.day, score_date.month, score_date.year)
                        result += '<tr><td>%i</td><td>%s</td></tr>' % (row['score'], date)
                    result += '</table>'
                result += '</section>'
                cursor.close()
                connection.close()
            session_store.close()
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Account</title>
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
                            <a href="">Account</a>
                        </li>
                    </ul>
                </nav>
            </header>
            <main>
                %s
            </main>
        </body>
    </html>""" % (result))
