import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import random
from accounts.models import User


def send_otp_via_email(email):
    try:
        otp = random.randint(100000, 999999)
        subject = "Your account verification OTP"
        message = f"Your OTP is: {otp}"
        print(otp)

        # Create a multipart message object
        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_HOST_USER
        msg["To"] = email
        msg["Subject"] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())

        # Update OTP in the user object
        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()

        return otp
    except Exception as e:
        print("Error sending email:", e)
        return None
