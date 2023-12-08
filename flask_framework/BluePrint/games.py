from flask import Blueprint, request,  render_template, jsonify, g
from werkzeug.utils import secure_filename
from model import User_data
from exts import db
import functions, configs
from functions import ssh_command, make_file
import os, re

bp = Blueprint("games", __name__, url_prefix='/games')
upload_folder = configs.UPLOAD_FOLDER


@bp.route('/game1', methods=['GET', 'POST'])
def Breaking_KASLR():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    else:
        if 'file' not in request.files:
            return jsonify({'code': 100, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                functions.upload(file.filename)
                functions.cstruct(prename)
                ssh_command(make_file(prename))
                functions.cpile(pre_task=f'sudo taskset 0x1 ./{prename[0]}', prename=prename)
                functions.download(prename[0])
                with open(configs.DOWNLOAD_FOLDER + f'/{prename[0]}.txt', 'r') as file:
                    content = file.read()
                    # 使用正则表达式匹配指定格式的内容
                    pattern = r'0x[a-fA-F\d]+'
                    matches = re.findall(pattern, content)
                    # 将匹配到的内容保存到变量
                    g.kaslr = matches[0] if matches else None
                    # 积分机制
                    # if g.kaslr is not None:
                    #     user = User_data.query.filter_by(id=g.id).first()
                    #     user.score += 10
                    #     db.session.commit()
                    print(g.kaslr)
                    # return jsonify({'code':200,'msg':"成功上传文件",'data':content})
                    return content


@bp.route('/game2', methods=['GET', 'POST'])
def Physical_Reader():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    else:
        if 'file' not in request.files:
            return jsonify({'code': 100, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                functions.upload(file.filename)
                functions.cstruct(prename)
                ssh_command('sudo ./secret2 > sec.txt')
                functions.download('sec.txt')
                with open(configs.DOWNLOAD_FOLDER + f'sec.txt', 'r') as sec_file:
                    sec_content = sec_file.read()
                    pattern = r'0x[0-9a-fA-F]{9,12}'
                    matches = re.findall(pattern, sec_content)
                    g.secret = matches[0] if matches else None
                    print(g.secret)
                # 下面的指令仍需修改
                ssh_command(make_file(prename))
                functions.cpile(f'taskset 0x1 ./{prename[0]} {g.secret} {g.kaslr}')
                functions.download(prename[0])
                with open(configs.DOWNLOAD_FOLDER + f'/{prename[0]}.txt', 'r') as file:
                    content = file.read()
                    return jsonify({'code': 200, 'msg': "成功上传文件", 'data': content})


@bp.route('/game3', methods=['GET', 'POST'])
def Reliability():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    else:
        if 'file' not in request.files:
            return jsonify({'code': 100, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                functions.upload(file.filename)
                functions.cstruct(prename)
                # 下面的仍需修改，地址每次运行时不同
                ssh_command(make_file(prename))
                functions.cpile(f'sudo taskset 0x1 ./{prename} -1 {g.kaslr}')
                functions.download(prename[0])
                with open(configs.DOWNLOAD_FOLDER + f'/{prename}.txt', 'r') as file:
                    content = file.read()
                    return jsonify({'code': 200, 'msg': "成功上传文件", 'data': content})
