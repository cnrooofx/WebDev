#!/usr/local/bin/python3

from os import environ
from shelve import DbfilenameShelf
from http.cookies import SimpleCookie
from cgitb import enable
enable()

print('Content-Type: text/html')
print()

result = '<p>You are already logged out</p>'
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = DbfilenameShelf('sessions/sess_' + sid, writeback=True)
            session_store['authenticated'] = False
            session_store.close()
            result = """<p>You are now logged out.</p>
                    <p>
                        <a href="login.py">Login again</a>
                    </p>"""
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Logout</title>
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
    </html>""" % (result))
