import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def get_star_rating(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    raw_rating = ((compound + 1) / 2) * 4 + 1

    final_rating = round(raw_rating)

    return max(1, min(5, final_rating))


def send_otp(otp, receiver_email="waytoalameen8802@gmail.com"):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "waytoalameen8802@gmail.com"
    app_password = "PUT YOUR KEY"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email

    message["Subject"] = "RateMyShow OTP"

    with open("rate_app/templates/otp.html") as file:
        body = file.read().replace("otp_placeholder", str(otp))
    message.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error: {e}")
