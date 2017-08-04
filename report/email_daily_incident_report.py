import os
import smtplib

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
import ConfigParser



def sendEmail(TO ,
              FROM):
    msg = MIMEMultipart()
    msg["From"] = FROM
    msg["To"] = TO
    msg["Subject"] = "DAILY INCIDENT REPORT"
    msg['Date']    = formatdate(localtime=True)

    # attach a file
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(filePath,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filePath))
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_host)
    server.login(username, password)  # optional

    try:
        failed = server.sendmail(FROM, TO, msg.as_string())
        server.close()
    except Exception, e:
        errorMsg = "Unable to send email. Error: %s" % str(e)

if __name__ == "__main__":
    filePath = 'pgdt_report.csv'
    smtp_host = os.environ['SMTP_HOST']
    smtp_sender = os.environ['SENDER_EMAIL_ADDRESS']
    smtp_reciever = os.environ['RECIEVER_EMAIL_ADDRESS'] 
    username = os.environ['smtp_username']
    password = os.environ['smtp_password']
    
    sendEmail(smtp_sender,smtp_reciever)
