import pymongo

class MongoDB():
    def __init__(self):
        client = pymongo.MongoClient('localhost',27017)
        db = client['Facebook']
        self.Allsql = db['allsql']

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

if __name__ == '__main__':
    mail_item = {'mail':'chenmo@yahoo.com','mail_pwd':'123','fb_pwd':'456','weibo':'www','state':0,'finished':0}
    info_item = {'mail':'chenmo@yahoo.com','mail_pwd':'abc','fb_pwd':'efg'}
    mondb = MongoDB()
    mondb.add_mail(mail_item)
    mondb.add_info(info_item)
