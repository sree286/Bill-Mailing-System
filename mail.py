import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_mail(receiver_email,file):
   
   subject = "Study Comrade Payment Invoice"
   body = """
Hey,
Thanks for registering for the course on Study Comrade. Your registration has been confirmed. Here is the payment invoice, keep this for future reference.
Discord is the platform we'll be using for all communications and any general talks. You can have all your doubts cleared there.
Follow the steps below:
1. Click on the link below and join the server.
(Download the application if you don't have it.)
2. If you are already using discord, You must set your nickname as your real name.
3. Go through various channels available. After joining the server, our team will add you to your course-related channels. It may take at least 2 to 3 hrs after joining the server.

https://discord.gg/85kzrZbb

Join the server as soon as possible.Once you join the server, you'll be assigned a role based on the course you've taken. You can reply back to this mail if you have any issues. 
If you have joined with your friends, they should also have received the same mail. Please help them to set up and join soon.
Thank you.


--
Team,
Study Comrade.
https://linktr.ee/studycomrade
   """
   sender_email = "gnaneshwarreddy456@gmail.com"
   cc_email = "admin@studycomrade.com"
   #receiver_email = "r170641@rguktrkv.ac.in"
   #print(receiver_email)
   #password = input("Type your password and press enter:")
   filename = file.split('/')[-1]
   password = 'Kondreddy@456'
   # Create a multipart message and set headers
   message = MIMEMultipart()
   message["From"] = sender_email
   message["To"] = receiver_email
   message["CC"] = cc_email
   message["Subject"] = subject
   #message["Bcc"] = receiver_email  # Recommended for mass emails

   # Add body to email
   message.attach(MIMEText(body, "plain"))

   #filename = "invoice.pdf"  # In same directory as script

   # Open PDF file in binary mode
   with open(file, "rb") as attachment:
       # Add file as application/octet-stream
       # Email client can usually download this automatically as attachment
       part = MIMEBase("application", "octet-stream")
       part.set_payload(attachment.read())

   # Encode file in ASCII characters to send by email    
   encoders.encode_base64(part)

   # Add header as key/value pair to attachment part
   part.add_header(
       "Content-Disposition",
       f"attachment; filename= {filename}",
   )

   # Add attachment to message and convert message to string
   message.attach(part)
   text = message.as_string()

   # Log in to server using secure context and send email
   context = ssl.create_default_context()
   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
       server.login(sender_email, password)
       server.sendmail(sender_email, receiver_email, text)

#send_mail("gnaneshwarreddy456@gmail.com",'Receipts/19203031.pdf')