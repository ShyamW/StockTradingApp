from twilio.rest import Client

account_sid = 'askinchat'
auth_token = 'askinchat'
client = Client(account_sid, auth_token)


def sendloginmessage(number, message):
    message = client.messages \
                    .create(
                        body=message,
                        from_='+17652006134',
                        to='+1' + number
                    )
    print(message.sid)
