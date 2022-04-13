from datetime import datetime as dt
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import os
import smtplib
import time


class Utils:
    def get_time() -> str:
        # פונקציה המחזירה זמן בצורת סטרינג. לדוגמה:
        # [10:15:20]
        now = dt.now()
        return f"[{now.hour}:{now.minute}:{now.second}]"
    # מחלקה לריכוז פעולות עזר                
    def send_mail() -> None:
        #פונקציה השולחת קובץ טקסט למייל
        # mail a txt file
        while True:
            # חשבון שיצרנו לקבלת ושליחת מסרים
            EMAIL = "Your email here"
            PASSWORD = "Your password here"
            
            now = dt.now()
            if os.path.exists(f"data/{str(int(now.day) - 1)}-{now.month}-{now.year}.txt"):
                # שולחת קובץ טקסט מאתמול אך ורק אם הוא קיים
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(EMAIL, PASSWORD)

                message = MIMEMultipart()
                message["From"] = EMAIL
                message["To"] = EMAIL
                message["Subject"] = f"Data from {str(int(now.day) - 1)}/{now.month}/{now.year}"
                file = f"data/{str(int(now.day) - 1)}-{now.month}-{now.year}.txt"
                attachment = open(file, 'rb')
                obj = MIMEBase('application','octet-stream')
                obj.set_payload((attachment).read())
                encoders.encode_base64(obj)
                obj.add_header('Content-Disposition',"attachment; filename= "+file)
                message.attach(obj)
                my_message = message.as_string()
                email_session = smtplib.SMTP('smtp.gmail.com',587)
                email_session.starttls()
                email_session.login(EMAIL, PASSWORD)
                email_session.sendmail(EMAIL, EMAIL, my_message)
                email_session.quit()
                os.remove(f"data/{str(int(now.day) - 1)}-{now.month}-{now.year}.txt")
            time.sleep((60 * 60 * 24) + 5) # יום אחד, לקבל דוח יומי