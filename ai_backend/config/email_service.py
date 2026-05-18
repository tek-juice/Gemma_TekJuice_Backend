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



def send_password_reset_email(name, email, reset_url):

    msg = Message(
        subject="Reset Your Password",
        recipients=[email]
    )

    # Plain text fallback
    msg.body = f"""
Hello {name},

You requested to reset your password.

Open the link below to reset it:

{reset_url}

If you did not request this, please ignore this email.

This link expires in 15 minutes.
"""

    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}

            .header {{
                background: #111827;
                color: white;
                padding: 30px;
                text-align: center;
            }}

            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}

            .content {{
                padding: 40px 30px;
                color: #333333;
                line-height: 1.7;
            }}

            .button {{
                display: inline-block;
                padding: 14px 28px;
                margin: 25px 0;
                background-color: #2563eb;
                color: white !important;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }}

            .footer {{
                background: #f9fafb;
                padding: 20px;
                text-align: center;
                font-size: 13px;
                color: #6b7280;
            }}

            .warning {{
                margin-top: 25px;
                padding: 15px;
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                border-radius: 6px;
                color: #92400e;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                <h1>Reset Your Password</h1>
            </div>

            <div class="content">

                <p>Hello <strong>{name}</strong>,</p>

                <p>
                    We received a request to reset your password.
                    Click the button below to create a new password.
                </p>

                <a href="{reset_url}" class="button">
                    Reset Password
                </a>

                <p>
                    Or copy and paste this link into your browser:
                </p>

                <p>
                    <a href="{reset_url}">
                        {reset_url}
                    </a>
                </p>

                <div class="warning">
                    If you did not request a password reset,
                    you can safely ignore this email.
                </div>

            </div>

            <div class="footer">
                © 2026 Plug Sites. All rights reserved.
            </div>

        </div>

    </body>
    </html>
    """

    mail.send(msg)
