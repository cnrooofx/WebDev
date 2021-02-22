#!/usr/local/bin/python3

from os import environ
from shelve import DbfilenameShelf
from http.cookies import SimpleCookie

from cgitb import enable
enable()

print('Content-Type: text/html')
print()

script = ''
result = """<section>
       <strong>You are not logged in.</strong>
       <p>Please log in or create an account to play.</p>
       <p>
           <a href="login.py">Login</a> &vert; <a href="accounts/register.py">Register</a>
       </p>
   </section>
   <section>
        <p>
            You can play the first level without an account as a guest.
        </p>
        <p>
            Your scores will not get added to the leaderboard.
        </p>
        <p>
            <a href="guest.html">Play as a Guest!</a>
        </p>
   </section>"""
footer = ''

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = DbfilenameShelf('sessions/sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                script = '<script src="game.js" type="module"></script>'
                result = """<canvas width="750" height="750"></canvas>
                    <p>Level: <span id="level">1</span></p>
                    <label for="health">Health:</label>
                    <progress value="0" max="100" id="health"></progress>
                    <p>
                        Score: <span id="score">0</span> &vert; <span id="username">%s</span>
                    </p>
                    <figure>
                        <figcaption>
                            Use the arrow keys to move around.
                        </figcaption>
                        <img src="media/keys.png" alt="Arrow keys from a computer keyboard" />
                    </figure>
                    <audio src="media/back1.mp3" loop>
                    </audio>""" % session_store.get('username')
                footer = """<footer>
            <small>
                Sprites from OpenGameArt.org courtesy of <a href="https://www.patreon.com/elthen">Elthen</a> &vert; Royalty Free Music by <a href="https://patrickdearteaga.com/royalty-free-music/">Patrick de Artega</a>
            </small>
        </footer>"""
            session_store.close()
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="styles.css" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <title>Play</title>
        %s
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
                        <a href="">Play</a>
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
        %s
    </body>
</html>""" % (script, result, footer))
