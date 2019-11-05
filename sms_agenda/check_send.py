import sqlite3
import datetime
from sms import send_sms
from agenda import get_agenda

connection = sqlite3.connect("/home/qq88/sms/sms_agenda/users.db")
cursor = connection.cursor()
cursor.execute("SELECT phone, timezone FROM user;")
result = cursor.fetchall()
now = datetime.datetime.utcnow()
now_str = str(now)[11:13]
for phone, timezone in result:
    if int(now_str) + int(timezone) == 20:
        # print(phone, timezone)
        send_sms(phone, get_agenda(int(timezone)))
    else:
        print(int(now_str) + int(timezone))
        print('oops', phone, timezone)

cursor.close()
connection.close()
