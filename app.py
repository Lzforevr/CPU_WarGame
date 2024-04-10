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
from exts import db, mail  # 从扩展中导入对象

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


# 获取游戏
@app.route('/lib/getProjects', methods=['GET'])
def get_projects():
    data = [
        {
            "typename": "Meltdown:熔断漏洞",
            "games": [
                {
                    "id": 0,
                    "name": "示例1：内核地址破坏者(KASLR Breaker)",
                    "desc": "从Linux内核4.12开始，默认情况下KASLR（内核地址空间布局随机化）处于活动状态。\n这意味着内核的位置（以及映射整个物理内存的直接物理映射）随着每次重新启动而变化。"
                            "在这一示例中，你将尝试使用Meltdown来泄露直接物理映射的（秘密）随机化，当你修改的代码运行成功后，将会显示一段文字：\n"
                            "[+] Direct physical map offset: 0xffff880000000000（例）\n"
                            "其中这串十六进制的数字就是通过漏洞直接得到的随机化地址偏移量！\n"
                            "值得注意的是，你在后面游戏中实现的Poc都需要基于这一串地址~",
                    "imgUrl": "https://tse1-mm.cn.bing.net/th/id/OIP-C.2hvpP-dB3A9PL2s9m5eZTgAAAA?rs=1&pid=ImgDetMain"
                },
                {
                    "id": 1,
                    "name": "示例2：揭露内存的面纱(Physical Memory Reader)",
                    "desc": "这个示例通过直接读取物理内存从不同的进程中读取内存的值。\n"
                            "原则上，这个程序应该可以读取任意的物理地址。然而，由于物理内存包含许多非人类可读的数据，\n我们将在你提交游戏文件后，自动运行一个测试文件（secret.c"
                            "），它将人类可读的字符串放入内存，并直接提供此字符串的物理地址。\n"
                            "此后，如果你的程序运行成功，将返回类似下面的内容：\n"
                            "[+] Physical address : 0x390fff400 	 //真正的物理地址\n"
                            "[+] Physical offset : 0xffff880000000000 //内核地址偏移量\n"
                            "[+] Reading virtual address: 0xffff880390fff400\n"
                            "If you can read this, this is really bad //secret.c所写入的可读字符串",
                    "imgUrl": "https://roqstar.s3.amazonaws.com/users/22682/items/1945-64vaxNrZ.jpg"
                },
                {
                    "id": 2,
                    "name": "示例3：可靠度vs命中率(Reliability Test)",
                    "desc": "众所周知，物理内存的可靠性与Poc代码读取这一内存的命中率是呈负相关的！\n"
                            "此程序的目的是通过不断重复进行内存读取，利用缓存侧信道攻击来泄露 secret "
                            "变量的值（secret变量在每次运行时随机生成）。\n在攻击中，每个循环迭代都会读取一个物理地址中的数据，并检查是否与 secret "
                            "的值相等。根据攻击结果，会增加相应的计数器，并输出攻击成功率和读取的数值数量。\n"
                            "假如你的代码运行成功，它的最后一行会输出：\n"
                            "[-] Success rate: 99.93% (read 1354 values) （例）\n"
                            "该结果表明通过meltdown漏洞得到真实物理内存的成功率高达99.93%！",
                    "imgUrl": "D:/Pycharm/CPU_wargame/flask_framework/static/games_picture/meltdown.png"
                }
            ]
        },
        {
            "typename": "Knight:骑士漏洞",
            "games": [
                {
                    "id": 3,
                    "name": "示例4:来日方长……",
                    "desc": "骑士漏洞暂未开发",
                    "imgUrl": "url_to_image_3"
                }
            ]
        }
    ]

    return jsonify({"code": 200, "data": data})


# ssl_crt='C:/Users/86189/server.crt',ssl_key='C:/Users/86189/server.key' 用以在Server方法中配置https
manager.add_command("runserver", Server(use_debugger=True))
manager.add_command("show-url", ShowUrls())


if __name__ == '__main__':
    socket_io.run(app, host=configs.IPV6, port=9000)
