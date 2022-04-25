from twilio.rest import Client
import smtplib

ACCOUNT_SID = "ACCOUNT SID"
AUTH_TOKEN = "AUTH TOKEN"

MY_EMAIL = "EMAIL"
MY_PASSWORD = "PASSWORD"


class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_="+17622274791",
            to="NUMBER"
        )
        print(message.sid)

    def send_emails(self, emails, message, link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL,
                             password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=emails,
                                msg=f"Subject: Cheap Flight Offer!\n\n{message}\n{link}".encode('utf-8')
                                )
