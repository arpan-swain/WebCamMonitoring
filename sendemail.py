import smtplib
import imghdr
from email.message import EmailMessage

password = "qvvf acqz vaxb boet"
sender = "arpanswain754@gmail.com"
receiver = "arpanswain754@gmail.com"
def send_email(img):
    # print("email_send start")
    email_msg = EmailMessage()
    email_msg["Subject"] = "New Notification"
    email_msg.set_content("Hey, There is a new customer")

    with open(img,"rb") as file:
        content = file.read()

    email_msg.add_attachment(content, maintype = "image", subtype = imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender,password)
    gmail.sendmail(sender,receiver,email_msg.as_string())
    gmail.quit()
    # print("email sent ended")