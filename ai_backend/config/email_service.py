from flask_mail import Message
from config.services.extensions import mail
import os

def send_verification_email(recipient, code):

    msg = Message(
        subject="Verify Your Email",
        sender= os.getenv("MAIL_USERNAME"),
        recipients=[recipient]
    )

    msg.body = f"""
Hello,

Your verification code is:

{code}

This code expires in 10 minutes.

If you did not request this, please ignore this email.
"""

    mail.send(msg)