import smtplib

    class EmailVerification():

        def sendto(self,email_addr,verificationcode):
            # Gmail Sign In
            gmail_sender = 'MyStockFetch@gmail.com'
            gmail_passwd = 'stock4920'
            to = email_addr

            subject = 'Account Verfication Code'
            text = 'Here is a message from Stock fetch.\n' \
                   'Please check your verification code '+ verificationcode+ ' and active your account'

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_sender, gmail_passwd)

            context = '\r\n'.join(['To: %s' % to,
                                'From: %s' % gmail_sender,
                                'Subject: %s' % subject,
                                '', text])

            try:
                server.sendmail(gmail_sender, [to], context)
                print ('email sent')
            except:
                print ('error sending mail')

            server.quit()