import subprocess
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
msg = MIMEMultipart()
count = 3

msg['From'] = '@gmail.com'
msg['To'] = '@gmail.com'
msg['Subject'] = 'Trading Bot Started'
msg.attach(MIMEText('The trading bot has started and will now be trading/backtesting.'))
try:
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('@gmail.com', '')
    mailserver.sendmail('@gmail.com', '@gmail.com', msg.as_string())
    print('Email notification about bot start sent')
    mailserver.quit()
except Exception as e:
    print(f"Failed to send email: {e}")

while count > 0:
    try:
        # Start the trading bot
        process = subprocess.Popen(['python', 'tradingbot.py'], stdout=sys.stdout, stderr=sys.stderr)
        # Wait for the process to finish
        process.wait()
    except Exception as e:
        print(f"An error occurred: {e}")
        count = count - 1 
        msg['From'] = '@gmail.com'
        msg['To'] = '@gmail.com'
        msg['Subject'] = 'Trading Bot Error'
        message = f'The trading bot has crashed. Attempting to restart. {count} attempts remaining'
        msg.attach(MIMEText(message))

        try:
            mailserver = smtplib.SMTP('smtp.gmail.com', 587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.login('@gmail.com', '')
            mailserver.sendmail('@gmail.com', '@gmail.com', msg.as_string())
            print('Email notification sent')
            mailserver.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

if count == 0:
    print('The trading bot has crashed and will not restart')
    msg['From'] = '@gmail.com'
    msg['To'] = '@gmail.com'
    msg['Subject'] = 'Trading Bot Error'
    msg.attach(MIMEText('The trading bot has crashed and is not restarting.'))
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login('@gmail.com', '')
        mailserver.sendmail('@gmail.com', '@gmail.com', msg.as_string())
        print('Email notification sent')
        mailserver.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")