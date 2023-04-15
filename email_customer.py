import smtplib, ssl
from dotenv import load_dotenv
import os
from email.message import EmailMessage
load_dotenv()


def send_email(receiver_email, time, date):
    msg = EmailMessage()

    msg.set_content('Thank you for your purchase \nYour order is at ' + date + ' ' + time)
    msg['Subject'] = 'Sayious Adventure Park'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = receiver_email
    port = os.getenv('EMAIL_PORT')
    password = os.getenv('EMAIL_PASSWORD')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("marios.charalambidis1996@gmail.com",password)
        server.send_message(msg)