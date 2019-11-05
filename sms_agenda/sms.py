from twilio.rest import Client
import os


def send_sms(phone, data):
    account_sid = 'AC24dcbb5b34d78ae155eff5a710099aeb'
    auth_token = os.environ.get('TWILIO')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=data,
            from_='+17178260124',
            to=phone
        )

    print(message.sid)
