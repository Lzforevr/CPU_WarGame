import os
import re

from flask import Blueprint, request, render_template, jsonify, g, send_file, session
from werkzeug.utils import secure_filename
import string
import configs
import functions
from exts import db
from functions import ssh_command, make_file, return_content, final_line, upload, cstruct, execute, download, out_line
from functions import socket_io
from model import User_data

bp = Blueprint("library", __name__, url_prefix='/lib')
upload_folder = configs.UPLOAD_FOLDER


# socket-io测试部分
# @bp.route('/test',methods=['GET','POST'])
# def Test():
#     if request.method == 'GET':
#         return render_template('socket_test.html')


# @socket_io.on('server_response')
# def test(data):
#     print(f'Data is:{data}')
#     if data:
#         socket_io.emit('server_response', {'data': data})
#
#
# @socket_io.on('client')
# def process(data):
#     print(data)


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
            if file.filename == string.whitespace:
                return jsonify({'code': 401, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                print(f'用户已上传：{file.filename}')
                upload(file.filename)
                cstruct(prename[0])
                ssh_command(make_file(prename[0]))
                execute(pre_task=f'sudo taskset 0x1 /home/bupt/hjl/meltdown/{prename[0]}', prename=prename)
                ssh_command(f'rm /home/bupt/hjl/meltdown/{prename[0]}')
                download(prename[0])
                ssh_command(f'rm /home/bupt/hjl/meltdown/{prename[0]}.txt')
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r') as sh_file:
                    contents = final_line(sh_file)
                    # 使用正则表达式匹配指定格式的内容
                    pattern = r'0x[a-fA-F\d]+'
                    matches = re.findall(pattern, contents)
                    # 将匹配到的内容保存到变量
                    configs.KASLR = matches[0] if matches else None
                    kaslr = configs.KASLR
                    print(f'地址偏移量为:{kaslr}')
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r') as c_file:
                    content = return_content(c_file)
                    print(f'{content}')
                    if c_file:
                        user_id = session.get('user_id')
                        user = User_data.query.filter_by(id=user_id).first()
                        if not user:
                            return jsonify({'code':400,'msg':"用户不存在",'data':'用户不存在,请登录后重试！'})
                        else:
                            user.score = user.score+10
                            db.session.commit()
                        return jsonify({'code':200,'msg':"示例代码运行成功，奖励10积分！",'data':content})

                    else:
                        return jsonify({'code':402,'msg':"文件错误",'data':'代码运行失败，请检查代码问题！'})


@bp.route('/example2', methods=['GET', 'POST'])
def Physical_Reader():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': 400, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == string.whitespace:
                return jsonify({'code': 401, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                upload(file.filename)
                cstruct(prename[0])
                ssh_command('cd /home/bupt/hjl/meltdown && sudo ./secret2 > sec.txt')
                download('sec')
                with open( f'{configs.DOWNLOAD_FOLDER}/sec.txt', 'r') as sec_file:
                    # 先利用函数保存文件最后一行
                    sec_content = sec_file.read()
                    print(sec_file.read())
                    # 再利用正则表达式匹配secret值，保存为全局变量
                    pattern = r'0x[0-9a-fA-F]+'
                    matches = re.findall(pattern, sec_content)
                    secret = matches[0] if matches else print('secret值获取失败')
                    configs.SEC = secret
                    print(f'secret:{secret}')
                ssh_command(make_file(prename[0]))
                execute(pre_task=f'taskset 0x1 /home/bupt/hjl/meltdown/{prename[0]} {secret} {configs.KASLR}', prename=prename)
                print('exe ok')
                download(prename[0])
                print('download ok')
                with open(configs.DOWNLOAD_FOLDER + f'/{prename[0]}.txt', 'r') as file:
                    content = return_content(file)
                    print(content)
                    if file:
                        user_id = session.get('user_id')
                        user = User_data.query.filter_by(id=user_id).first()
                        if not user:
                            return '用户不存在，请登录后重试！'
                        else:
                            user.score = user.score+10
                            db.session.commit()
                        return jsonify({'code': 200, 'msg': "示例代码运行成功，奖励10积分！", 'data': content})


@bp.route('/example3', methods=['GET', 'POST'])
def Reliability():
    if request.method == 'GET':
        return render_template('test_sendfiles.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': 100, 'msg': '文件格式错误', 'data': None})
        else:
            file = request.files['file']
            if file.filename == string.whitespace:
                return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
            elif file and functions.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                prename = file.filename.rsplit('.', 1)
                upload(file.filename)
                cstruct(prename[0])
                ssh_command(make_file(prename[0]))
                execute(f'sudo taskset 0x1 /home/bupt/hjl/meltdown/{prename[0]} -1 {configs.KASLR}',prename)
                download(prename[0])
                with open(f'{configs.DOWNLOAD_FOLDER}/{prename[0]}.txt', 'r', encoding='utf-8') as c_file:
                    content = return_content(c_file)
                    print(content)
                    if c_file:
                        user_id = session.get('user_id')
                        user = User_data.query.filter_by(id=user_id).first()
                        if not user:
                            return '用户不存在，请登录后重试！'
                        else:
                            user.score = user.score+10
                            db.session.commit()
                        return jsonify({'code': 200, 'msg': "示例代码运行成功，奖励10积分！", 'data': content})


# 用于下载示例代码，根据字典键值对下载
@bp.route('/download',methods=['GET','POST'])
def Download_examples():
    if request.method == 'POST':

        filename = request.form['file']
        example_route = {
            'kaslr':'D:/大创/meltdown/kaslr_test2.c',
            'physical_reader':'D:/Pycharm/meltdown/physical_reader.c',
            'reliability':'D:/Pycharm/meltdown/reliability2.c'
        }
        return send_file(example_route[filename],as_attachment=True)
    else:
        return render_template('test_download.html')


@bp.route('/getImage')
def getImage():
    data = [
        'http://[2001:da8:215:8f02:1fef:98a1:ddf1:de5e]:9000/static/KASLR.png',
        'http://[2001:da8:215:8f02:1fef:98a1:ddf1:de5e]:9000/static/Physical_Reader.png',
        'http://[2001:da8:215:8f02:1fef:98a1:ddf1:de5e]:9000/static/Realiability.png'
    ]
    return jsonify({"code":200,"data":data})


@bp.route('checkImage')
def Image():
    return render_template("test_writein.html")
