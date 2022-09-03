import smtplib
import os
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(addr_to, msg_subj, msg_text, file):
    addr_from = "mail"
    password  = "password"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    process_attachement(msg, file)

    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()

def process_attachement(msg, file):
    for f in file:
        if os.path.isfile(f):
            attach_file(msg,f)
        elif os.path.exists(f):
            dir = os.listdir(f)
            for file in dir:
                attach_file(msg,f+"/"+file)

def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)
        file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)