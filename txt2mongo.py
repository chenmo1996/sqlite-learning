import re
from mongobase import MongoDB

NEW_MAIL = re.compile(r"([a-zA-Z0-9\.\-_]+@[\w\d]+\.[\w\d]+)[\||\:|;|\-]+([a-zA-Z0-9]+)")

mondb = MongoDB()

with open('/Users/cgj/chen/py/appium/sqlite-learning/in.txt','r') as f:
    text =  f.read()
    print(text)
    mails = NEW_MAIL.findall(text)
    for mail in mails:
        buy_item = {}
        buy_item['mail'] = mail[0]
        buy_item['mail_pwd'] = mail[1]
        mondb.insert_one_buy(buy_item)
        print(mail)
    # print(mails)
