import os
import re

from flask import Blueprint, request, render_template, jsonify, send_file, session
from werkzeug.utils import secure_filename
import string
import configs
import functions
from exts import db
from functions import ssh_command, make_file, return_content, final_line, upload, cstruct, execute, download, out_line
from model import User_data

bp = Blueprint("library", __name__, url_prefix='/lib')
upload_folder = configs.UPLOAD_FOLDER


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
                print(configs.KASLR)
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
        f'http://[{configs.IPV6}]:9000'+'/static/KASLR.png',
        f'http://[{configs.IPV6}]:9000'+'/static/Physical_Reader.png',
        f'http://[{configs.IPV6}]:9000'+'/static/Realiability.png'
    ]
    return jsonify({"code":200,"data":data})


@bp.route('/getProjects', methods=['GET'])
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