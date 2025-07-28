import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
msg = MIMEMultipart()
msg['From'] = 'gtworks247@gmail.com'
msg['To'] = 'gttrys247@gmail.com'
msg['Subject'] = 'Trading Bot Error'
msg.attach(MIMEText('The trading bot has crashed and will not restart.'))

try:
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('gtworks247@gmail.com', 'luczzbsakevaaejc')
    mailserver.sendmail('gtworks247@gmail.com', 'gttrys247@gmail.com', msg.as_string())
    print('Email notification sent')
    mailserver.quit()
except Exception as e:
    print(f"Failed to send email: {e}")