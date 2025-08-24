import os
import email
import imaplib
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_ACCOUNT = "sainiaanchal313@gmail.com"
APP_PASSWORD = "xahq ljtj zctr lhxx"
ATTACHMENT_DIR = "attachments"
 
os.makedirs(ATTACHMENT_DIR,exist_ok=True)

def fetch_unread_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT,APP_PASSWORD)
        mail.select("inbox")
        status,message = mail.search(None,'From','"anchalsaini595@gmail.com"')
        email_ids = message[0].split()
        print(f"📨 Checked inbox. Found {len(email_ids)} unread emails.")
        for e_ids in email_ids:
            status,msg_data = mail.fetch(e_ids,"(RFC822)")
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            sender = msg["From"]
            subject = msg["Subject"]
            print(f"\n📩 New email from: {sender} | Subject: {subject}")
            for part in msg.walk():
                if part.get_content_disposition()== 'attachment':
                    file_name= part.get_filename()
                    if file_name:
                        file_path = os.path.join(ATTACHMENT_DIR,file_name)
                        with open(file_path,'wb') as f:
                            f.write(part.get_payload(decode=True))
                            print(f"📎 Saved attachment: {file_name}")
                
            send_auto_reply(sender, subject)
        mail.logout()

    except Exception as e:
        print("Error",str(e))

def send_auto_reply(receiver,subject):
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER,465)
        server.login(EMAIL_ACCOUNT,APP_PASSWORD)
        reply = MIMEMultipart()
        reply["From"]= EMAIL_ACCOUNT
        reply["To"]=receiver
        reply["Subject"]= f"Re: {subject}"
        body = """Hello, 
Thank you for your email. This is an automated reply. 
I’ll get back to you soon!
"""    
        reply.attach(MIMEText(body,"plain"))
        server.sendmail(EMAIL_ACCOUNT,receiver,reply.as_string())
        server.quit()
        print(f"✅ Auto-reply sent to {receiver}")
    except Exception as e:
        print("❌ Failed to send reply:", str(e))

def run_scheduler():
    schedule.every(0.5).minutes.do(fetch_unread_emails)

    print("⏳ Email bot started. Checking inbox every 5 minutes...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)    

if __name__ == "__main__":
    run_scheduler()    