import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email_template


def send_email(sender, size, expires, download_link, reciver):
    sender_email = "your email"
    receiver_email = reciver
    password = "your email password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Download File !!!"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = email_template.EmailTemplate(sender, size, expires, download_link)
    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
