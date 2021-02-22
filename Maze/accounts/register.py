#!/usr/local/bin/python3

from cgi import FieldStorage, escape
from hashlib import sha256
import pymysql as db
from passwordgen import generate_password
from send_email import password_email

from cgitb import enable
enable()

print('Content-Type: text/html')
print()

form_data = FieldStorage()
username = ''
email = ''
result = ''

if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    email = escape(form_data.getfirst('email', '').strip())
    if not username or not email:
        result = '<p>Sorry! All fields are required.</p>'
    elif len(username) > 10:
        result = '<p>Sorry! Username must be less than 10 characters.</p>'
    else:
        try:
            connection = db.connect('localhost', 'cf26', 'pecah', 'cs6503_cs1106_cf26')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT *
                              FROM users
                              WHERE username = %s""", (username))
            if cursor.rowcount == 0:
                password = generate_password()
                sha256_password = sha256(password.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, email, password)
                                  VALUES (%s, %s, %s)""", (username, email, sha256_password))
                connection.commit()
                password_email(username, email, password)
                result = """<p>You have been successfully registered! Please check your email to get your password</p>
                    <p><a href="../login.py">Login Here</a></p>"""
            else:
                result = """<p>Sorry! That username is already taken.</p>
                            <p>Choose another username or <a href='../login.py'>Click here</a> to sign in.</p>"""
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please try again later.</p>'

print("""
    <!DOCTYPE html>
    <html lang='en'>
        <head>
            <meta charset='utf-8' />
            <link rel="stylesheet" href="../styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Register</title>
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
                    <h2>Register Account</h2>
                    <p>Your temporary password will be sent to your email address</p>
                    <form action='register.py' method='post'>
                        <label for='username'>Username: </label>
                        <input type='text' name='username' id='username' value='%s' placeholder="Enter username" required />
                        <label for='email'>Email: </label>
                        <input type='email' name='email' id='email' value='%s' placeholder="Enter email" required />
                        <input type='submit' value='Register' />
                    </form>
                    %s
                </section>
            </main>
        </body>
    </html>""" % (username, email, result))
