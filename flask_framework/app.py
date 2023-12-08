import os
from flask import Flask, request, render_template, flash, redirect, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
# 以下用于学习文件上传
from werkzeug.utils import secure_filename

import configs, functions
from BluePrint.main_screen import bp as main_bp
from BluePrint.user import bp as user_bp
from BluePrint.games import bp as game_bp
from exts import db, mail  # 从扩展中导入对象

app = Flask(__name__)
CORS(app)

#  绑定配置文件
app.config.from_object(configs)
# 将该路径上传到flask配置中，在其他文件使用路径时可通过current_app导入
app.config['UPLOAD_FOLDER'] = configs.UPLOAD_FOLDER

#  绑定db\mail扩展
db.init_app(app)
mail.init_app(app)

#  绑定blueprint中的对象
app.register_blueprint(user_bp)
app.register_blueprint(main_bp)
app.register_blueprint(game_bp)
# 数据库迁移
migrate = Migrate(app, db)

# 以下配置用于https协议，暂未完成
# 指定CA证书与密钥文件位置
app.config['SSL_CERTIFICATE'] = 'D:/Pycharm/CPU_wargame/flask_framework/server.crt'
app.config['SSL_PRIVATE_KEY'] = 'D:/Pycharm/CPU_wargame/flask_framework/server.key'
with app.app_context():
    db.create_all()


# 响应getProjects路由
@app.route('/getProjects', methods=['GET'])
def get_projects():
    data = {
        "Meltdown:熔断漏洞": [
            {
                "id": 1,
                "name": "Game 1",
                "desc": "Description 1",
                "imgUrl": "static/games_picture/meltdown.png"
            },
            {
                "id": 2,
                "name": "Game 2",
                "desc": "Description 2",
                "imgUrl": "url_to_image_2"
            }
        ],
        "Knight:骑士漏洞": [
            {
                "id": 3,
                "name": "Game 3",
                "desc": "Description 3",
                "imgUrl": "url_to_image_3"
            }
        ]
    }

    return jsonify(data)


# 文件上传测试
@app.route('/upload', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    else:
        if request.method == 'POST':
            # 检查文件是否存在
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            #   return jsonify({'code':100,'msg':'文件格式错误','data':None})
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
                # return jsonify({'code':300,'msg':'文件不能为空','data':None})
            if file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                prename = file.filename.rsplit('.', 1)
                upload = f'scp D:/Pycharm/CPU_wargame/flask_framework/C_Files/{file.filename} cpu@10.122.218.87:/home' \
                         f'/cfiles'
                cstrut = f'cd /home/cfiles && touch {prename[0]}.txt'
                cpile = f'gcc /home/cfiles/{file.filename} -o /home/cfiles/{prename[0]} && /home/cfiles/./{prename[0]} > /home/cfiles/{prename[0]}.txt'
                download = f"scp cpu@10.122.218.87:/home/cfiles/{prename[0]}.txt D:/Pycharm/CPU_wargame" \
                           f"/flask_framework" \
                           f"/Rturnfiles"
                os.system(upload)
                functions.ssh_command(cstrut)
                functions.ssh_command(cpile)
                os.system(download)
                # return jsonify({'code':200,'msg':'文件上传成功','data':None})
                return 'OK'
            elif functions.allowed_file(file.filename) == 0:
                return 'Invalid Filename'
                # return jsonify({"code":505,"msg":"无效文件格式","data":None})


if __name__ == '__main__':
    app.run(debug=True)
