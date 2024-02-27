import os
import re

from flask import Blueprint, request, render_template, jsonify, g
from werkzeug.utils import secure_filename

import configs
import functions
from functions import ssh_command, make_file, return_content, final_line, upload, cstruct, execute, download,out_line

bp = Blueprint("games", __name__, url_prefix='/games')
upload_folder = configs.UPLOAD_FOLDER
global kaslr, secret


# 现用于文件写入测试
@bp.route('/game1', methods=['GET', 'POST'])
def GAME_ONE():
    if request.method == 'GET':
        return render_template('test_writein.html')
    elif request.method == 'POST':
        contents = request.form['data']
        print(contents)
        with open('C_Files/output.c','w',) as file:
            file.write(contents)
            return 'c文件写入成功'


@bp.route('/game2', methods=['GET', 'POST'])
def Physical_Reader():
    if request.method == 'POST':
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
                upload(file.filename)
                cstruct(prename)
                ssh_command('cd /home/cpu/meltdown_long && sudo ./secret2 > sec.txt')
                download('sec')
                with open( f'{configs.DOWNLOAD_FOLDER}/sec.txt', 'r') as sec_file:
                    # 先利用函数保存文件最后一行
                    sec_content = out_line(sec_file)
                    print(sec_file.readlines())
                    # 再利用正则表达式匹配secret值，保存为全局变量
                    pattern = r'^0x[0-9a-fA-F]+$'
                    matches = re.findall(pattern, sec_content)
                    secret = matches[0] if matches else None
                    print(f'secret:{secret}')
                ssh_command(make_file(prename))
                execute(pre_task=f'taskset 0x1 ./{prename[0]} {g.secret} {kaslr}', prename=prename)
                download(prename[0])
                with open(configs.DOWNLOAD_FOLDER + f'/{prename[0]}.txt', 'r', encoding='utf-8') as file:
                    content = return_content(file)
                    print(content)
                    return jsonify({'code': 200, 'msg': "成功上传文件", 'data': content})


@bp.route('/game3', methods=['GET', 'POST'])
def Reliability():
    if request.method == 'POST':
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
                upload(file.filename)
                cstruct(prename)
                ssh_command(make_file(prename))
                execute(f'sudo taskset 0x1 ./{prename[0]} -1 {g.kaslr}')
                download(prename[0])
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r', encoding='utf-8') as c_file:
                    content = return_content(c_file)
                    print(content)
                    return jsonify({'code': 200, 'msg': "成功上传文件", 'data': content})


@bp.route('/sendfile')
def send_file():
    upload('output.c')
    return 'OK'