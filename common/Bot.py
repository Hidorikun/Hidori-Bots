import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Bot:

    def __init__(self, credentials_file='common/credentials.txt'):
        self.__email_address, self.__password = self.__read_credentials(credentials_file)
        self.__receivers = set()

    def add_receivers(self, receivers):
        for receiver_address in receivers:
            self.__receivers.add(receiver_address)

    def send_email(self, subject, email):

        message = MIMEMultipart("alternative")
        message["From"] = self.__email_address
        message["Subject"] = subject

        part1 = MIMEText(email.plain_content, "plain")
        part2 = MIMEText(email.html_content, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.__email_address, self.__password)

            for receiver_address in self.__receivers:
                message["To"] = receiver_address
                server.sendmail(
                    self.__email_address, receiver_address, message.as_string()
                )

    def __read_credentials(self, credentials_file):
        with open(credentials_file, 'r') as file:
            return file.readline(), file.readline()
