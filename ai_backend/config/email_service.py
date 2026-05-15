from flask_mail import Message
from config.services.extensions import mail
import os

def send_verification_email(name, recipient, code):

    msg = Message(
        subject="Verify Your TekJuice AI Account",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[recipient]
    )

    msg.html = f"""
    <div style="
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        padding: 30px;
    ">
        <div style="
            max-width: 600px;
            margin: auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        ">

            <!-- Header -->
            <div style="
                background: #2596be;
                color: white;
                padding: 20px;
                text-align: center;
            ">
                <h1>TekJuice AI</h1>
            </div>

            <!-- Content -->
            <div style="padding: 30px; color: #333;">

                <h2>Hello {name}, </h2>

                <p>
                    Welcome to <strong>TekJuice AI</strong>.
                </p>

                <p>
                    You registered using this email:
                    <strong>{recipient}</strong>
                </p>

                <p>
                    Your email verification code is:
                </p>

                <div style="
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 5px;
                    background: #f3f4f6;
                    padding: 15px;
                    text-align: center;
                    border-radius: 8px;
                    margin: 20px 0;
                    color: #111827;
                ">
                    {code}
                </div>

                <p>
                    This code expires in
                    <strong>10 minutes</strong>.
                </p>

                <p style="margin-top: 30px;">
                    If you did not create this account,
                    please ignore this email.
                </p>

            </div>

            <!-- Footer -->
            <div style="
                background: #f9fafb;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 14px;
            ">
                © 2026 TekJuice AI — All Rights Reserved
            </div>

        </div>
    </div>
    """

    mail.send(msg)