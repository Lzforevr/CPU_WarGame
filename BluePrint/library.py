import os
import re

from flask import Blueprint, request, render_template, jsonify, g, send_file
from werkzeug.utils import secure_filename

import configs
import functions
from functions import ssh_command, make_file, return_content, final_line, upload, cstruct, execute, download,out_line


bp = Blueprint("library", __name__, url_prefix='/lib')
upload_folder = configs.UPLOAD_FOLDER
global kaslr, secret


@bp.route('/example1', methods=['GET', 'POST'])
def Breaking_KASLR():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': 400, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            # 对文件格式（包括扩展名）进行检查
            if file.filename == '':
                return jsonify({'code': 401, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                print(f'用户已上传：{file.filename}')
                upload(file.filename)
                # os.system(f'del D:/Pycharm/CPU_wargame/flask_framework/C_Files/{file.filename}')
                cstruct(prename)
                ssh_command(make_file(prename))
                ##############################################
                # 当使用虚拟机运行kaslr时偶尔会出现无法停止找不到的bug
                ##############################################
                execute(pre_task=f'sudo taskset 0x1 /home/lz/meltdown/{prename[0]}', prename=prename)
                ssh_command(f'rm /home/lz/meltdown/{prename[0]}')
                # 现在下载出问题，必须找到functions中的原因
                download(prename[0])
                ssh_command(f'rm /home/lz/meltdown/{prename[0]}.txt')
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r') as sh_file:
                    contents = final_line(sh_file)
                    # 使用正则表达式匹配指定格式的内容
                    pattern = r'0x[a-fA-F\d]+'
                    matches = re.findall(pattern, contents)
                    # 将匹配到的内容保存到变量
                    kaslr = matches[0] if matches else None
                    print(f'地址偏移量为:{kaslr}')
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r') as c_file:
                    content = return_content(c_file)
                    print(f'{content}')
                    if c_file:
                        return jsonify({'code':200,'msg':"成功上传文件",'data':content})
                    else:
                        return jsonify({'code':402,'msg':"文件错误",'data':'代码运行失败，请检查代码问题！'})


@bp.route('/example2', methods=['GET', 'POST'])
def Physical_Reader():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': 400, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'code': 401, 'msg': '文件名不能为空', 'data': None})
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


@bp.route('/example3', methods=['GET', 'POST'])
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


# 用于下载示例代码，根据字典键值对下载
@bp.route('/download',methods=['GET','POST'])
def Download_examples():
    if request.method == 'POST':

        filename = request.form['file']
        example_route = {
            'kaslr':'D:/大创/meltdown/kaslr_test2.c',
            'physical_reader':'D:/Pycharm/meltdown/physical_reader_test.c',
            'reliability':'D:/Pycharm/meltdown/reliability2.c'
        }
        return send_file(example_route[filename],as_attachment=True)
    else:
        return render_template('test_download.html')
