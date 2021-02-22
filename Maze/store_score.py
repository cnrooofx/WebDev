#!/usr/local/bin/python3

from cgi import FieldStorage
from html import escape
import pymysql as db
from time import time, localtime

from cgitb import enable
enable()

print('Content-Type: text/plain')
print()

form_data = FieldStorage()
username = escape(form_data.getfirst('user', '').strip())
if username:
    try:
        date = localtime(time())
        month = date.tm_mon
        day = date.tm_mday
        if int(day) < 10:
            day = '0' + str(day)
        if int(month) < 10:
            month = '0' + str(month)
        score_date = '%s-%s-%s' % (date.tm_year, month, day)
        score = escape(form_data.getfirst('score', '').strip())
        connection = db.connect('', '', '', '')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""INSERT INTO leaderboard (username, score, score_date)
                          VALUES
                          (%s, %s, %s)""", (username, score, score_date))
        connection.commit()
        print('success')
        cursor.close()
        connection.close()
    except db.Error:
        print('problem')
else:
    print('problem')
