import smtplib

SUBJECT = 'Your Secret Code from the Stock Trading App'
SENDER_EMAIL = 'stock.trading.app.osu@gmail.com'
SENDER_PASSWORD = '!Password'
HOST = 'smtp.gmail.com'


def send_email(dest_email=None, num=None):
    """ Sends an email from stock.trading.app.osu@gmail.com to dest_email.
    Args:
        dest_email: email address to send to
        num: secret number to send                                    """

    text = 'Secret code is: ' + str(num)
    email_text = 'Subject: {}\n\n{}'.format(SUBJECT, text)

    server = smtplib.SMTP_SSL(HOST, 465)
    server.ehlo()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, dest_email, email_text)
    server.close()

    print('Email sent!')
