import smtplib
from flask import url_for

class VerificationEmail:

    def sendto(self,email_addr,verificationcode):
        error = None

        gmail_sender = 'MyStockFetch@gmail.com'
        gmail_passwd = 'stock4920'
        to = email_addr

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)

        message = """From: %s
To: %s
MIME-Version: 1.0
Content-type: text/html
Subject: Fetch Account Verfication

<a href="%s">Click here to verify your Fetch account</a>
<p>Alternatively, copy the following into your browser:</p>
<p>%s</p>
"""
        url = url_for('verify_email', email=to, code=verificationcode, _external=True)
        try:
            server.sendmail(gmail_sender, [to], message % (gmail_sender, to, url, url))
        except:
            error = -1

        server.quit
        return error
