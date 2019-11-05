import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from sms_agenda import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset link',
                    sender='88isthenewblack@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password follow the link below.
{url_for('users.reset_token', token=token, _external=True)}

If you did not request it just ignore the email.
'''

    mail.send(msg)
