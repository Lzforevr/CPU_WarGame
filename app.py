import os
from flask import Flask, request, render_template, flash, redirect, jsonify, url_for
from flask_cors import CORS
from flask_migrate import Migrate
# 设置自定义命令
from flask_script import Manager, Server
from flask_script.commands import ShowUrls
# 以下用于文件上传
from werkzeug.utils import secure_filename
import configs, functions
# 设置全双工服务，实时更新
from functions import socket_io
# 导入蓝图
from BluePrint.main_screen import bp as main_bp
from BluePrint.user import bp as user_bp
from BluePrint.games import bp as game_bp
from BluePrint.library import bp as lib_bp
from BluePrint.tips import bp as tips_bp
from BluePrint.videos import bp as videos_bp
from exts import db, mail

app = Flask(__name__)
CORS(app,resources=r'/*')
manager = Manager(app)

#  绑定配置文件
app.config.from_object(configs)
# 将该路径上传到flask配置中，在其他文件使用路径时可通过current_app导入
app.config['UPLOAD_FOLDER'] = configs.UPLOAD_FOLDER

#  绑定db\mail扩展
db.init_app(app)
mail.init_app(app)
socket_io.init_app(app)
#  绑定blueprint中的对象
app.register_blueprint(user_bp)
app.register_blueprint(main_bp)
app.register_blueprint(game_bp)
app.register_blueprint(lib_bp)
app.register_blueprint(tips_bp)
app.register_blueprint(videos_bp)
# 数据库迁移
migrate = Migrate(app, db)

# 以下配置用于https协议，暂未完成
# 指定CA证书与密钥文件位置
app.config['SSL_CERTIFICATE'] = 'D:/Pycharm/CPU_wargame/flask_framework/server.crt'
app.config['SSL_PRIVATE_KEY'] = 'D:/Pycharm/CPU_wargame/flask_framework/server.key'
with app.app_context():
    db.create_all()


# ssl_crt='C:/Users/86189/server.crt',ssl_key='C:/Users/86189/server.key' 用以在Server方法中配置https
manager.add_command("runserver", Server(use_debugger=True))
manager.add_command("show-url", ShowUrls())


if __name__ == '__main__':
    socket_io.run(app, host=configs.IPV6, port=9000)
