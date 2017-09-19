import os.path

MAILACCOUNT = "xxxxx"
MAILPWD = "xxxxx"
MAILDOMAIN = "xxxxx"
CHECKSIZE = 2
PROXY_URL = "http://lum-customer-hl_b9fea07e-zone-static:yoa8ajine31i@zproxy.luminati.io:22225"
# PROXY_URL = "http://lum-customer-hl_7608778f-zone-static:ogzwqi0a7qx8@zproxy.luminati.io:22225"
IP_URL = "http://lumtest.com/myip.json"
PROXY_IP = "zproxy.luminati.io"
PROXY_PORT = 22225
PROXY_USERNAME = "lum-customer-hl_b9fea07e-zone-static"
#PROXY_USERNAME = "lum-customer-hl_7608778f-zone-zone1-country-us"
PROXY_PASSWORD = "yoa8ajine31i"
#PROXY_PASSWORD = "lv8fehatoxq2"

PATH_COOKIES = "./cookies.bk"

LOG_NAME = 'sqllog'
LOG_PATH =  os.path.join(os.path.abspath(os.path.dirname(__file__)),'sqllog.log')
LOG_FORMAT = "%(asctime)-15s %(filename)-15s %(process)3d %(funcName)-15s %(lineno)d %(message)s"
LOG_NAME_OPE = "fboperationlog"
LOG_PATH_OPE =  os.path.join(os.path.abspath(os.path.dirname(__file__)),'fboperationlog.log')

IMG_PATH = '/tmp/'


DRIVER_PATH = '/home/ubuntu/chromedriver'
