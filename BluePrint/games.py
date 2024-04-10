import os
import re

from flask import Blueprint, request, render_template, jsonify, g
from flask_socketio import emit
from werkzeug.datastructures.file_storage import FileStorage
import configs
import functions
from functions import ssh_command, make_file, return_content, final_line, upload, cstruct, execute, download, out_line
from functions import socket_io

bp = Blueprint("games", __name__, url_prefix='/games')
upload_folder = configs.UPLOAD_FOLDER


# 现用于文件写入测试
# @bp.route('/game1', methods=['GET', 'POST'])
# def GAME_ONE():
#     if request.method == 'GET':
#         return render_template('test_writein.html')
#     elif request.method == 'POST':
#         contents = request.form['data']
#         print(contents)
#         with open('C_Files/output.c','w',) as file:
#             file.write(contents)
#             return 'c文件写入成功'
@socket_io.on('client_send', namespace='/game1')
def socket_io_test1(Input):
    id = request.cookies.get('id')
    # 正式版根据用户id差异化文件名
    # game_name = f'game1{id}'
    game_name = 'game1'
    with open(f'Writein_files/{game_name}.c', 'w') as file:
        file.write(Input)
    emit('response', 'c文件写入成功！', namespace='/game1')
    print(f'用户id{id},已上传游戏一代码！')
    oc1 = functions.game_upload('game1.c', configs.ROUTE_FOR_LINUX + f'/{game_name}.c')
    print(oc1)
    emit('response', oc1, namespace='/game1')
    oc2 = cstruct('game1')
    # emit('response',oc2,namespace='/game1')


@bp.route('/game2', methods=['GET', 'POST'])
def GAME_TWO():
    if request.method == 'GET':
        return render_template('sockettest2.html')


# 问题：upload到远程机的文件为空，导致cstruc错误；
@socket_io.on('client_send', namespace='/game2')
def socket_io_test(Input):
    with open('Writein_files/game2.c', 'w') as file:
        file.write(Input)
    emit('response', 'c文件写入成功！', namespace='/game2')
    print('用户已上传游戏二代码！')
    oc1 = functions.game_upload('game2.c')
    print(oc1)
    emit('response', oc1, namespace='/game2')
    oc2 = cstruct('game2')
    # emit('response',oc2,namespace='/game2')
    # ssh_command(make_file('game2'))
    # oc3 = execute(pre_task='sudo taskset 0x1 /home/lz/meltdown/game2', prename='game2')
    # emit('response',oc3,namespace='/game2')
    # ssh_command('rm /home/lz/meltdown/game2')
    # oc4 = download('game2')
    # emit('response',oc4,namespace='/game2')
    # ssh_command(f'rm /home/lz/meltdown/game2.txt')
    # with open(f'{configs.DOWNLOAD_FOLDER}/game2.txt', 'r') as sh_file:
    #     contents = final_line(sh_file)
    #     # 使用正则表达式匹配指定格式的内容
    #     pattern = r'0x[a-fA-F\d]+'
    #     matches = re.findall(pattern, contents)
    #     # 将匹配到的内容保存到变量
    #     configs.KASLR = matches[0] if matches else None
    #     kaslr = configs.KASLR
    #     print(f'地址偏移量为:{kaslr}')
    #     emit('response',f'成功得到地址偏移量:{kaslr}',namespace='/game2')
    #     content = return_content(sh_file)
    #     print(f'{content}')
    #     emit('outcome',f'得到运行结果:\n{content}',namespace='/game2')
    #     if sh_file:
    #         # user_id = session.get('user_id')
    #         # user = User_data.query.filter_by(id=user_id).first()
    #         # if not user:
    #         #     return '用户不存在，请登录后重试！'
    #         # else:
    #         #     user.score = user.score+10
    #         #     db.session.commit()
    #         return jsonify({'code': 200, 'msg': "示例代码运行成功，获得10积分！", 'data': content})
    #     else:
    #         return jsonify({'code': 402, 'msg': "文件错误", 'data': '代码运行失败，请检查代码问题！'})


# 游戏一：乱序脱逃
@bp.route('/get_game1')
def get_game1():
    data = {
        'code': 200,
        'desc': '本游戏核心在于利用cpu乱序执行机制，逃脱检查机制的“追捕。”由于meltdown的逻辑符合CPU底层逻辑。所以我们用底层的汇编代码，实施meltdown攻击。\n\
               你需要知道：1.数据的格式： b-字节(8 bit)，w-字(16 bit)，l-双字(32 bit)，q-四字(64 bit)\n 2.Linux进程的虚拟\
内存结构，知道不可读写的内核地址处于哪个区域。\n3.理解内联汇编的扩充内容，即变量如何与寄存器的值相联系。\n4.明白汇编指令的跳转与循环。\n\
所用变量说明：%%rcx寄存器上，存储着我们的想要非法读取“内核地址”。\n%%rbx寄存器上，存储着我们的探针数组的起始地址。\
(极为庞大，为4KB*256，即256“页”。我们通过观测256页中是否有一页被访问过，间接读取内核地址的内容)',
        'part1': '''#define meltdown_nonull\\ \nasm volatile( "1:\\n"\\ \n''',
        'part2': ''': "c"(phys), "b"(mem)\\ \n: "rax");\n'''
    }
    return jsonify(data)


# 游戏二：缓存侧信道的危机
@bp.route('/get_game2')
def get_game2():
    data = {
        'code': 200,
        'desc': '本游戏重在利用cpu缓存侧信道机制，尝试利用meltdown读取cache中的内存值。\n\
    有关缓存侧信道的概念，可以参考：https://blog.csdn.net/zy_zhengyang/article/details/89678501\n\
    所涉及函数说明：1.uint64_trdtsc(void), 它返回当前电脑的时间戳.\n2.void maccess(void ptr), 用于将所指区域的值，加载（缓存）到寄存器中.\n\
    3.void flush(void * ptr), 用于将所指区域的值，清除它在寄存器中的缓存.\n\
    4.size_t config.cache_miss_threshold , 系统中缓存不命中时，读取时间的平均值\n\
    所涉及变量说明：我们用到一个读取电脑配置的结构体变量 config , 包含了主机运行速度、内存格式',
        'part1': '''static int attribute((always_inline))\n flush_reload(void *ptr) {\n\
uint64_t start = 0, end = 0;\n''',
        'part2':''
    }
    return jsonify(data)