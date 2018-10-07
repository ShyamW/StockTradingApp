from twilio.rest import Client

account_sid = 'AC36d4020ee9e2c0ff821a1565d90c856b'
auth_token = 'fc600177f8717ae72914f73e12be31c7'
client = Client(account_sid, auth_token)


def sendloginmessage(number, message):
    message = client.messages \
                    .create(
                        body=message,
                        from_='+17652006134',
                        to='+1' + number
                    )
    print(message.sid)
