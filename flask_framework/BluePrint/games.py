from flask import Blueprint, request, session, render_template, jsonify, current_app
from werkzeug.utils import secure_filename
from model import User_data
import functions, configs
from functions import ssh_command
import os

bp = Blueprint("games",__name__,url_prefix='/games')
upload_folder = current_app.config['UPLOAD_FOLDER']


@bp.route('/game1',methods=['GET','POST'])
def Breaking_KASLR():
    if 'file' not in request.files:
        return jsonify({'code':100,'msg':'文件格式错误','data':None})
    else:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
        elif file and functions.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 下面join里的第一个参数与app不同，尝试一下能否成功
            file.save(os.path.join(upload_folder, filename))
            prename = file.filename.rsplit('.', 1)
            functions.upload(file.filename)
            functions.cstruct(prename)
            functions.cpile(f'sudo taskset 0x1 ./{prename}')
            functions.download(prename)
            with open(configs.DOWNLOAD_FOLDER+f'/{prename}.txt', 'r') as file:
                content = file.read()
                return jsonify({'code':200,'msg':"成功上传文件",'data':content})


@bp.route('/game2',methods=['GET','POST'])
def Physical_Reader():
    if 'file' not in request.files:
        return jsonify({'code':100,'msg':'文件格式错误','data':None})
    else:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
        elif file and functions.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 下面join里的第一个参数与app不同，尝试一下能否成功
            file.save(os.path.join(upload_folder, filename))
            prename = file.filename.rsplit('.', 1)
            functions.upload(file.filename)
            functions.cstruct(prename)
            ssh_command('sudo ./secret')
            # 下面的指令仍需修改
            ssh_command()
            functions.cpile(f'taskset 0x1 ./{prename} 0x390fff400 0xffff880000000000')
            functions.download(prename)
            with open(configs.DOWNLOAD_FOLDER+f'/{prename}.txt', 'r') as file:
                content = file.read()
                return jsonify({'code':200,'msg':"成功上传文件",'data':content})


@bp.route('/game3',methods=['GET','POST'])
def Reliability():
    if 'file' not in request.files:
        return jsonify({'code':100,'msg':'文件格式错误','data':None})
    else:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': 300, 'msg': '文件名不能为空', 'data': None})
        elif file and functions.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 下面join里的第一个参数与app不同，尝试一下能否成功
            file.save(os.path.join(upload_folder, filename))
            prename = file.filename.rsplit('.', 1)
            functions.upload(file.filename)
            functions.cstruct(prename)
            # 下面的仍需修改，地址每次运行时不同
            functions.cpile(f'sudo taskset 0x1 ./{prename} -1 {}') #要加入kaslrdemo中的内存偏移
            functions.download(prename)
            with open(configs.DOWNLOAD_FOLDER+f'/{prename}.txt', 'r') as file:
                content = file.read()
                return jsonify({'code':200,'msg':"成功上传文件",'data':content})