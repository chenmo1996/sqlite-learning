import sqlite3
import csv
from sqllogging import initlog
from config import LOG_NAME
import logging

DB_SUCCESS = 1
DB_FAIL = -1
TABLENAME_INFO = "FBINFO"
TABLENAME_ACCOUNT = "FBACCOUNT"

SET_STATE = '''
update {0} set State={1} where Mail="{2}";
'''
SET_COOKIES = '''
update {0} set Cookies='{1}' where Mail='{2}';
'''
UPDATE_WEIBO = '''
update {0} set Weibo='{1}',Cookies='{2}' where Mail='{3}';
'''
UPDATE_WEIBO2 = '''
update {0} set Weibo='{1}' where Mail='{2}';
'''
SELECT_NOWEIBO = '''
select * from {0} where Weibo='' and state=1 and finished=0;
'''
SELECT_WEIBO = '''
select * from {0} where Weibo='{1}';
'''

TABLEDROPSTATE = """
DROP TABLE IF EXISTS {0};
"""

TABLECREATESTATE_INFO = """
CREATE TABLE {0}(
    Mail char(40),
    Day int(5),
    Month int(4),
    Year int(12),
    Gender boolen,
    Firstname varchar(20),
    Lastname varchar(20),
    IP char(20),
    FOREIGN KEY(Mail) REFERENCES {1}(Mail)
)
""".format(TABLENAME_INFO, TABLENAME_ACCOUNT)

TABLECREATESTATE_ACCOUNT = """
CREATE TABLE {0}(
    Mail char(40) unique primary key,
    Cookies Char(1700) default '',
    Mail_pwd char(15),
    Fb_pwd char(15),
    UserAgent char(150),
    Weibo char(100) default '',
    Session char(20),
    State boolen default 1,
    finished boolen default 0
)
""".format(TABLENAME_ACCOUNT)

TABLEINSERTSTATE_INFO = """
INSERT INTO {} VALUES(
    '{}',{},{},{},{},'{}','{}','{}'
);
"""

TABLEINSERTSTATE_ACCOUNT = """
INSERT INTO {} VALUES(
    '{}','{}','{}','{}','{}','{}','{}',{},{}
);
"""

TABLESELECTSTATE = """
SELECT * from {};
"""

TABLESELECTAVAILABLE = """
SELECT * from {} where state = 1 and finished = 0 ;
"""

TABLEEXISTS = """
SELECT count(*) FROM sqlite_master WHERE type='table' AND name="{}"
"""

TABLESELECTONESTATE = """
SELECT Mail from {} where Mail="{}" 
"""

TABLESELECTSUCCESS = '''
SELECT Mail,Fb_pwd,Mail_pwd where state = 1 and finished = 0;
'''

TABLESETFINISHED = '''
UPDATE {} SET finished=1 where Mail='{}';
'''

# TODO divide into Two table Mail/Mail_pwd/Fb_pwd and other

# sqlite adapter OBJ TO SQL


class FBDB():

    def __init__(self, path="./sqllite.db"):
        self.path = path
        self.conn = sqlite3.connect(path)
        cursor = self.conn.cursor()
        cursor.execute(TABLEEXISTS.format(TABLENAME_INFO))
        res = cursor.fetchone()[0]
        cursor.execute(TABLEEXISTS.format(TABLENAME_ACCOUNT))
        res1 = cursor.fetchone()[0]
        if not res or not res1:
            self.create_table()
        self.conn.close()

    def check_mail_exist(self, mail):
        self.conn = sqlite3.connect(self.path)
        pass

    def get_all_info(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute(TABLESELECTSTATE.format(TABLENAME_INFO))
        res = cursor.fetchall()
        self.conn.close()
        print(res)
        return res

    def get_all_available(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute(TABLESELECTAVAILABLE.format(TABLENAME_ACCOUNT))
        res = cursor.fetchall()
        self.conn.close()
        return res

    def get_all_account(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute(TABLESELECTSTATE.format(TABLENAME_ACCOUNT))
        res = cursor.fetchall()
        self.conn.close()
        return res

    def select_by_weibbo(self, weibo):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            cursor.execute(SELECT_WEIBO.format(TABLENAME_ACCOUNT, weibo))
            res = cursor.fetchone()
            self.conn.close()
            return res
        except Exception as e:
            self.conn.close()
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
            return None

    def set_finished(self, mail):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            cursor.execute(TABLESETFINISHED.format(TABLENAME_ACCOUNT, mail))
            self.conn.commit()
        except Exception as e:
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
        self.conn.close()

    def get_unbind_account(self):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            cursor.execute(SELECT_NOWEIBO.format(TABLENAME_ACCOUNT))
            res = cursor.fetchall()
            self.conn.close()
            return res
        except Exception as e:
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
            self.conn.close()
            return None

    def bind_account(self, mail, weibo, cookies=''):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            if cookies:
                cursor.execute(UPDATE_WEIBO.format(
                    TABLENAME_ACCOUNT, weibo, cookies, mail))
            else:
                cursor.execute(UPDATE_WEIBO2.format(
                    TABLENAME_ACCOUNT, weibo, mail))
            self.conn.commit()
            self.conn.close()
            return 1
        except Exception as e:
            self.conn.close()
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
            return -1

    def set_cookies(self, mail, cookies):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            cursor.execute(SET_COOKIES.format(
                TABLENAME_ACCOUNT, cookies, mail))
            self.conn.commit()
        except Exception as e:
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
        self.conn.close()

    def disable_account(self, mail):
        self.conn = sqlite3.connect(self.path)
        try:
            cursor = self.conn.cursor()
            cursor.execute(SET_STATE.format(TABLENAME_ACCOUNT, 0, mail))
            self.conn.commit()
        except Exception as e:
            log = logging.getLogger(LOG_NAME)
            log.exception(repr(e))
        self.conn.close()

    def insert_info(self, mail=None, mailpwd=None, fbpwd=None, day=None, month=None,
                    year=None, gender=None, firstname=None, lastname=None, ua=None,
                    session=None, ip=None, cookies=None, weibo=None, type=1):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        if mail and mailpwd and fbpwd and day and month and year and firstname\
           and lastname:
            try:
                cookies = cookies if cookies else ''
                weibo = weibo if weibo else ''
                cursor.execute(TABLEINSERTSTATE_ACCOUNT.format(TABLENAME_ACCOUNT, mail, cookies,
                                                               mailpwd, fbpwd, ua, weibo, session, 1, 0))
                self.conn.commit()
                cursor.execute(TABLEINSERTSTATE_INFO.format(TABLENAME_INFO, mail,
                                                            day, month, year, gender, firstname, lastname, ip))
                self.conn.commit()
                self.conn.close()
                return DB_SUCCESS
            except Exception as e:
                log = logging.getLogger(LOG_NAME)
                log.exception(repr(e))
                self.conn.close()
                return DB_FAIL
        elif type == 2 and mail and session:
            cursor.execute(TABLEINSERTSTATE_ACCOUNT.format(TABLENAME_ACCOUNT, mail,
                                                           '', '', '', '', '', session, 0, 0))
            self.conn.commit()
            self.conn.close()
        else:
            log = logging.getLogger(LOG_NAME)
            log.info("some param is None,cause insert fail")
            return DB_FAIL

    def drop_table(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute(TABLEDROPSTATE.format(TABLENAME_INFO))
        cursor.execute(TABLEDROPSTATE.format(TABLENAME_ACCOUNT))
        self.conn.commit()
        self.conn.close()
        return

    def create_table(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        try:
            cursor.execute(TABLECREATESTATE_ACCOUNT)
            cursor.execute(TABLECREATESTATE_INFO)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        self.conn.close()

    def renew_table(self):
        db.drop_table()
        db.create_table()

    def checkexist(self, mail):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        cursor.execute(TABLESELECTONESTATE.format(TABLENAME_ACCOUNT, mail))
        row = cursor.fetchone()
        self.conn.close()
        if row:
            #print(mail, "exist")
            return True
        else:
            return False


class CSV():

    def __init__(self):
        pass

    def export2file(self, data, filename="./data.csv"):
        with open(filename, 'w', newline='\n') as csvfile:
            spamwriter = csv.writer(csvfile)
            for d in data:
                spamwriter.writerow(d)
        return


if __name__ == "__main__":
    initlog()
    db = FBDB()

    res = db.get_all_info()
    # res = db.get_all_account()

    # c.export2file(res)
    # db.renew_table()
    print(res)


    # db.disable_account("111")
    # res = db.get_unbind_account()
    # print(len(res))
    # db.bind_account("111","1")
    # res = db.get_all_available()
    # print(res)
    # db.drop_table()
    # db.create_table()
    # db.renew_table()
    # IntegrityError
    # if db.checkexist("1152761042@qq.com"):
    #    print("mail exist")
    # else:
    # db.insert_info("1152761046@qq.com", "pwd",
    #                "pwwd2", 1, 1, 1, 1, "Qifan", "Liu")
    # c = CSV()