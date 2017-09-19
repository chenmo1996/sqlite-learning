from database import FBDB
from mongobase import MongoDB

if __name__ == "__main__":
    # initlog()
    db = FBDB()
    mondb = MongoDB()
    # res = db.get_all_info()
    res = db.get_all_account()
    # c.export2file(res)
    # db.renew_table()
    print(res)
    for mail_info in res:
        mail_item = {}
        mail_item['mail'] = mail_info[0]
        mail_item['mail_pwd'] = mail_info[2]
        mail_item['fb_pwd'] = mail_info[3]
        mail_item['weibo'] = mail_info[5]
        mail_item['state'] = mail_info[7]
        mail_item['finished'] = mail_info[8]
        mondb.add_mail(mail_item)



