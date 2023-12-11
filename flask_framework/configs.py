# 配置
# 数据库的配置信息

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
USER = 'cpu'
IP = '@10.122.218.87'
IP_V = '@10.21.162.136'

ROUTE_FOR_V = '/home/cpu/meltdown'
ROUTE_FOR_LINUX = '/home/cpu/meltdown_long'