# 配置
# 数据库的配置信息，只需连接到本地数据库server即可
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'cpu_wargame'
USERNAME = 'root'
PASSWORD = "6666"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4' \
    .format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = False
MAIL_PORT = 587
MAIL_USERNAME = '1446219282@qq.com'
MAIL_PASSWORD = 'djvmixsoedukbagb'
MAIL_DEFAULT_SENDER = 'cpuwargame@qq.com'

# session的盐加密
SECRET_KEY = 'aonisz'

# 文件上传用配置,规定了.c的扩展名限制
UPLOAD_FOLDER = 'C_Files'
DOWNLOAD_FOLDER = 'D:/Pycharm/CPU_wargame/flask_framework/Rturnfiles'
ALLOWED_EXTENSIONS = {'c'}

# ssh登录信息配置
USER = 'bupt'
USER_V = 'lz'
IP = '10.122.228.153'
IP_V = '10.21.162.136'
IPV6 = '2001:da8:215:8f02:1fef:98a1:ddf1:de5e'
PRIVATE_KEY_V = 'C:/Users/86189/.ssh/virtual_machine'
PRIVATE_KEY = 'C:/Users/86189/.ssh/id_rsa'
ROUTE_FOR_V = '/home/cpu/meltdown'
ROUTE_FOR_LINUX = '/home/bupt/hjl/meltdown'
# 自定义libkdump库位置
ROUTE_ST = '/home/bupt/hjl/meltdown/customc'
ROUTE_ND = '/home/bupt/hjl/meltdown/customh'
KASLR = ''
SEC = ''