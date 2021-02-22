
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def password_email(username, email, password):
    context = ssl.create_default_context()
    sender_email = "conorfox.test@gmail.com"
    message = MIMEMultipart('alternative')
    message["To"] = email
    message["From"] = sender_email
    message["Subject"] = "Complete your a-MAZE-ing registration"
    plain_text = """Hey %s,

    Thank you for registering to play a-MAZE-ing.
    Your password is:

    %s

    You can change it later in the account page.

    Click here to login https://cs1.ucc.ie/~cf26/cgi-bin/lab7/login.py

    Thanks,
        Conor
    """ % (username, password)
    html = """
    <html>
        <body>
            <p>Hey %s,<br>
                Thank you for registering to play a-MAZE-ing.</p>
        <p>Your password is:</p>

        <code>%s</code>

        <p>You can change it later in the account page.<p>

        <p>Click here to login <a href="https://cs1.ucc.ie/~cf26/cgi-bin/lab7/login.py">https://cs1.ucc.ie/~cf26/cgi-bin/lab7/login.py</a></p>

        <p>Thanks,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Conor</p>
        </body>
    </html>
    """ % (username, password)
    plain_part = MIMEText(plain_text, "plain")
    html_part = MIMEText(html, "html")
    message.attach(plain_part)
    message.attach(html_part)
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender_email, '+4xmsXrn;Jn2aCQk')
        server.sendmail(sender_email, email, message.as_string())


def reset_email(username, email, code):
    context = ssl.create_default_context()
    sender_email = "conorfox.test@gmail.com"
    message = MIMEMultipart('alternative')
    message["To"] = email
    message["From"] = sender_email
    message["Subject"] = "a-MAZE-ing Password Reset"
    plain_text = """Hey %s,

    A password reset has been requested for the a-MAZE-ing game.

    Your code is:

    %s

    If you didn't request this, you can safely ignore this email.

    Thanks,
        Conor
    """ % (username, code)
    html = """
    <html>
        <body>
            <p>Hey %s,<br>
                A password reset has been requested for the a-MAZE-ing game.</p>
        <p>Your code is:</p>

        <code>%s</code>

        <p>If you didn't request this, you can safely ignore this email.<p>

        <p>Thanks,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Conor</p>
        </body>
    </html>
    """ % (username, code)
    plain_part = MIMEText(plain_text, "plain")
    html_part = MIMEText(html, "html")
    message.attach(plain_part)
    message.attach(html_part)
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender_email, '+4xmsXrn;Jn2aCQk')
        server.sendmail(sender_email, email, message.as_string())
