#!/usr/local/bin/python3

import pymysql as db
from cgitb import enable
enable()

print('Content-Type: text/html')
print()

result = ''
try:
    connection = db.connect('', '', '', '')
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""SELECT *
                      FROM leaderboard
                      ORDER BY score DESC
                      LIMIT 50""")
    rank = 1
    for row in cursor.fetchall():
        score_date = row['score_date']
        date = '%s/%s/%s' % (score_date.day, score_date.month, score_date.year)
        result += '<tr><td>%i</td><td>%s</td><td>%i</td><td>%s</td></tr>' % (rank, row['username'], row['score'], date)
        rank += 1
    result += '</table>'
    cursor.close()
    connection.close()
except db.Error:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="styles.css" />
            <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            <title>Leaderboard</title>
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
                            <a href="">Leaderboard</a>
                        </li>
                        <li>
                            <a href="account.py">Account</a>
                        </li>
                    </ul>
                </nav>
            </header>
            <main>
                <section>
                    <table>
                        <caption>Leaderboard</caption>
                        <tr>
                            <th scope="col">
                                Rank
                            </th>
                            <th scope="col">
                                Username
                            </th>
                            <th scope="col">
                                Score
                            </th>
                            <th scope="col">
                                Date
                            </th>
                        </tr>
                        %s
                    </table>
                </section>
            </main>
        </body>
    </html>""" % (result))
