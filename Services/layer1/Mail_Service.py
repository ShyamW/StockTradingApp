import smtplib


SUBJECTS = {
    "Account Creation": "Account Created",
    "Login": "Login Activity",
    "Login Attempt": "Potential Login Attempt",
    "Account Deleted": "Account Deleted",
    "Password Changed": "Password Changed"
}
SENDER_EMAIL = 'stock.trading.app.osu@gmail.com'
SENDER_PASSWORD = '!Password'
HOST = 'smtp.gmail.com'


def send_email(dest_email=None, num=None, user=None, ip=None):
    """ Sends an email from stock.trading.app.osu@gmail.com to dest_email.
    Args:
        dest_email: email address to send to
        num: secret number to send
        user: user info                                 """

    ipaddress = ip
    text = "Hello, " + user.firstname + "\n\nwe just received a request from " + ipaddress + ". If this was not you please log into your account and change your password. \n\nActivity:\n"
    text += SUBJECTS[num]
    email_text = 'Subject: {}\n\n{}'.format(SUBJECTS[num], text)

    server = smtplib.SMTP_SSL(HOST, 465)
    server.ehlo()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, dest_email, email_text)
    server.close()

    print('Email sent!')
