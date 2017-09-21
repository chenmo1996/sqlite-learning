import pymongo

class MongoDB():
    def __init__(self):
        client = pymongo.MongoClient('localhost',27017)
        db = client['Facebook']
        self.Allsql = db['allsql']
        self.Buyact = db['buyact']

    def add_mail(self,mail_item):
        if self.Allsql.find_one({'mail':mail_item['mail']}) == None:
            self.Allsql.insert_one(mail_item)
            print('-----------------------------------------')
            print('insert_one_search ', mail_item['mail'])
            print('-----------------------------------------')
        else:
            print('-----------------------------------------')
            print('Already have ', mail_item['mail'])
            print('-----------------------------------------')

    def add_info(self,info_item):
        if self.Allsql.find_one({'mail':info_item['mail']}) == None:
            print('-----------------------------------------')
            print('NO ', info_item['mail'])
            print('-----------------------------------------')
        else:
            mail_item = self.Allsql.find_one({'mail':info_item['mail']})
            dictMerged = dict(mail_item, **info_item)
            self.Allsql.update({'mail':info_item['mail']},dictMerged,upsert=True)

    def insert_one_buy(self,mail_item):
        self.Buyact.update({'mail':mail_item['mail']},mail_item,upsert=True)
        print('-----------------------------------------')
        print('insert_one_buy ', mail_item['mail'])
        print('-----------------------------------------')

    def remove_used(self):
        used_mails = self.Allsql.find()
        for used_mail in used_mails:
            rtd = self.Buyact.find_one_and_delete({'mail':used_mail['mail']})
            # print(rtd)
            if rtd == None:
                pass
            else:
                print('deleated ',used_mail['mail'])
        print('buy left',self.Buyact.count())

    def out_buy(self):
        buy_mails = self.Buyact.find()
        with open('/Users/cgj/chen/py/appium/sqlite-learning/out.txt','a') as f:
            for mail in buy_mails:
                line = mail['mail']+'----'+mail['mail_pwd']+'\n'
                f.write(line)

if __name__ == '__main__':
    mail_item = {'mail':'chenmo@yahoo.com','mail_pwd':'123','fb_pwd':'456','weibo':'www','state':0,'finished':0}
    info_item = {'mail':'chenmo@yahoo.com','mail_pwd':'abc','fb_pwd':'efg'}
    # buy_item = {'mail':'buy1@yahoo.com','mail_pwd':'123'}
    mondb = MongoDB()
    # mondb.add_mail(mail_item)
    # mondb.add_info(info_item)
    # mondb.insert_one_buy(buy_item)
    # 删除已经注册成功的邮件
    mondb.remove_used()
    # 导出购买了但是没有成功注册的邮件
    mondb.out_buy()