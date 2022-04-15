try:
    from datetime import datetime as dt
    from sensors import temperature, WaterLevel, weight
    from utils import Utils
    
    import os
    import pywhatkit as pwk
    import threading
    import time
except Exception as err:
    print(f"Some libraries missing! Details: {err}")
    exit() # צא מתתכנית, פונקציה בנויה 



'''
רעיון כללי של הקוד:
התכנית תקבל נתונים בזמן אמת מהחיישנים המותקנים. 
לאחר מכן, התכנית תיצור קובץ טקסט חדש בהתאם לתאריך של היום ותשמור שם את המידע שאספה
פעולה זו תחזור על עצמה כל שעה.
בתחילת כל יום חדש, קובץ הטקסט של אתמול יישלח במייל אוטומטי
וגם ימחוק את הקובץ לאחר מכן כדי לא לגמור את כל המקום בזיכרון
כל קבצי הטקסט יאורגנו בתיקייה חדשה בשם דאטה 
פרטים מלאים על כל פונקציה מצורפים.
'''

# email that will be used to send and receive messages (it will send messages to itself)
EMAIL = 'Your email here'
PASSWORD = 'Your password here'

class ZooManager:
    # המחלקה הראשית לניהול גן החיות
    def setup_needed_files() -> None:
        # פונקציה המתקינה קבצים ותיקיות נדרשות לאחסון המידע
        if not os.path.exists('data'):
            os.mkdir('data') # יצירת תיקיית data
        now = dt.now()
        if not os.path.exists(f"data/{now.day}-{now.month}-{now.year}.txt"):
            with open(f"data/{now.day}-{now.month}-{now.year}.txt", 'w') as f: # יצירת קובץ טקסט
                f.close()
        

    def calculate_temperature():
        # פונקציה המחשבת טמפרטורה
        humidity, tempt = temperature.calculate_temperature()
        
        if tempt>30:
             pwk.send_mail(EMAIL, PASSWORD, 'Temperature alert', 'Temperature over 30!', EMAIL)
             '''
             Function inside the pywhatkit library. Usage:
             pywhatkit.send_mail(sender_email, paswword, subject, message, reciever_email)
             '''
        return tempt, humidity
    
    def calculate_water_level():
        # חישוב רמת המים
        water_level = WaterLevel.calculate_water_level()
        if water_level <= 1:
            pwk.send_mail(EMAIL, PASSWORD, 'Water alert', 'No water left!', EMAIL)

        return water_level
    def calculate_weight():
        # חישוב משקל
        w = weight.calculate_weight()
        if w < 1:
            pwk.send_mail(EMAIL, PASSWORD, 'Food alert', 'No food left!', EMAIL)
        return w
    
    def record_data():
        # פונקציה המתעדת מידע לקובץ הטקסט המתאים
        ZooManager.setup_needed_files()
        while True:
            try:
                tempt, humidity = ZooManager.calculate_temperature()
                water_level  = ZooManager.calculate_water_level()
                w = ZooManager.calculate_weight()
                now = dt.now()
                with open(f"data/{now.day}-{now.month}-{now.year}.txt", 'a') as f:
                    f.write(f"{Utils.get_time()}\n")
                    f.write(f"tempt: {tempt}*C\n")
                    f.write(f'Humidity: {humidity}%\n')
                    f.write(f"water level: {water_level}cm\n")
                    f.write(f"weight: {w}Kg\n")
            except Exception as e:
                pass
            finally:
                time.sleep(3600) # 1 hour


def main():
    t1 = threading.Thread(target=Utils.send_mail)
    t2 = threading.Thread(target=ZooManager.record_data)
    t1.start()
    t2.start()
    # טרדינג:
    # היכולת להריץ כמה פונקציות באותו הזמן
if __name__ == '__main__':
    main()
