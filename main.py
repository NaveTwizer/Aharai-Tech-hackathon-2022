try:
    from utils import Utils
    from ZooManager import ZooManager
    import threading
except Exception as err:
    print(f"Some libraries missing! Details: {err}")
    exit() # צא מהתכנית, פונקציה בנויה 


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

def main():
    t1 = threading.Thread(target=Utils.send_mail)
    t2 = threading.Thread(target=ZooManager.record_data)
    t1.start()
    t2.start()
    # טרדינג:
    # היכולת להריץ כמה פונקציות באותו הזמן
if __name__ == '__main__':
    main()
