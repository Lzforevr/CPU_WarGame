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


@bp.route('/game1', methods=['GET', 'POST'])
def GAME_ONE():
    if request.method == 'GET':
        return render_template('sockettest2.html')


@socket_io.on('client_send', namespace='/game1')
def socket_io_test1(Input):
    # id = request.cookies.get('id')
    # 正式版根据用户id差异化文件名
    # game_name = f'game1_{id}'
    game_name = 'game1_1'
    # 将用户代码插入到libkdump.c中
    with open('./static/libkdump1.c', 'r') as refer_file:
        lines = refer_file.readlines()
        lines.insert(59,Input)
    with open(f'Writein_files/{game_name}.c', 'w') as file:
        file.writelines(lines)
    emit('response', '.c文件写入成功！', namespace='/game1')
    print(f'用户id,已上传游戏一代码！')
    # 上传源文件
    oc1 = functions.game_upload('game1.c', configs.ROUTE_ST + f'/{game_name}.c')
    print(oc1)
    emit('response', oc1, namespace='/game1')
    # 构建txt
    oc2 = cstruct('kaslr_game')
    print(oc2)
    # 指定库编译
    ssh_command(functions.customed_make('kaslr_game', 'ST'))
    emit('response',oc2,namespace='/game1')
    oc3 = execute(pre_task='sudo taskset 0x1 /home/bupt/hjl/meltdown/kaslr_game', prename=['kaslr_game','c'])
    emit('response',oc3,namespace='/game1')
    ssh_command('rm /home/bupt/hjl/meltdown/kaslr_game')
    oc4 = download("kaslr_game")
    emit('response',oc4,namespace='/game1')
    ssh_command('rm /home/bupt/hjl/meltdown/kaslr_game.txt')
    with open(f'{configs.DOWNLOAD_FOLDER}/kaslr_game.txt', 'r') as sh_file:
        contents = final_line(sh_file)
        # 使用正则表达式匹配指定格式的内容
        pattern = r'0x[a-fA-F\d]+'
        matches = re.findall(pattern, contents)
    if matches:
        emit('response', f"成功基于您的源文件编译得到kaslr：{matches[0]}", namespace='/game1')
        emit('outcome','非常顺利，您的库源文件能够正常使用！')
    else:
        emit('response', '编译失败，请检查您的源文件是否正确！', namespace='/game1')
        emit('outcome', '非常遗憾，您的库源文件无法正常使用！')


@bp.route('/game2', methods=['GET', 'POST'])
def GAME_TWO():
    if request.method == 'GET':
        return render_template('sockettest2.html')


# 问题：upload到远程机的文件为空，导致cstruc错误；
@socket_io.on('client_send', namespace='/game2')
def socket_io_test2(Input):
    # id = request.cookies.get('id')
    # 正式版根据用户id差异化文件名
    # game_name = f'game2_{id}'
    game_name = 'game2_2'
    # 将用户代码插入到libkdump.c中
    with open('./static/libkdump2.c', 'r') as refer_file:
        lines = refer_file.readlines()
        lines.insert(185,Input)
    with open(f'Writein_files/{game_name}.c', 'w') as file:
        file.writelines(lines)
    emit('response', '游戏二.c文件写入成功！', namespace='/game2')
    print(f'用户id,已上传游戏二代码！')
    # 上传源文件
    oc1 = functions.game_upload(f'{game_name}.c', configs.ROUTE_ND + f'/{game_name}.c')
    print(oc1)
    emit('response', oc1, namespace='/game2')
    # 构建txt
    oc2 = cstruct('kaslr_game2')
    print(oc2)
    # 指定库编译
    ssh_command(functions.customed_make('kaslr_game2', 'ND'))
    emit('response',oc2,namespace='/game2')
    oc3 = execute(pre_task='sudo taskset 0x1 /home/bupt/hjl/meltdown/kaslr_game2', prename=['kaslr_game2','c'])
    emit('response',oc3,namespace='/game2')
    ssh_command('rm /home/bupt/hjl/meltdown/kaslr_game2')
    oc4 = download("kaslr_game2")
    emit('response',oc4,namespace='/game2')
    ssh_command('rm /home/bupt/hjl/meltdown/kaslr_game2.txt')
    with open(f'{configs.DOWNLOAD_FOLDER}/kaslr_game2.txt', 'r') as sh_file:
        contents = final_line(sh_file)
        # 使用正则表达式匹配指定格式的内容
        pattern = r'0x[a-fA-F\d]+'
        matches = re.findall(pattern, contents)
    if matches:
        emit('response', f"成功基于您的源文件编译得到kaslr：{matches[0]}", namespace='/game2')
        emit('outcome','非常顺利，您的库源文件能够正常使用！')
    else:
        emit('response', '编译失败，请检查您的源文件是否正确！', namespace='/game2')
        emit('outcome', '非常遗憾，您的库源文件无法正常使用！')

# 游戏一：乱序脱逃
@bp.route('/get_game1')
def get_game1():
    data = {
        'code': 200,
        'desc': '本游戏核心在于利用cpu乱序执行机制，逃脱检查机制的“追捕。”由于meltdown的逻辑符合CPU底层逻辑。所以我们用底层的汇编代码，实施meltdown攻击。\n\
               你需要知道：1.数据的格式： b-字节(8 bit)，w-字(16 bit)，l-双字(32 bit)，q-四字(64 bit)\n 2.Linux进程的虚拟\
内存结构，知道不可读写的内核地址处于哪个区域。\n3.理解内联汇编的扩充内容，即变量如何与寄存器的值相联系。\n4.明白汇编指令的跳转与循环。\n\
所用变量说明：%%rcx寄存器上，存储着我们的想要非法读取“内核地址”。\n%%rbx寄存器上，存储着我们的探针数组的起始地址。\
(极为庞大，为4KB*256，即256“页”。我们通过观测256页中是否有一页被访问过，间接读取内核地址的内容)\n\
内联汇编参考：https://blog.csdn.net/lyndon_li/article/details/118471845\nhttps://blog.csdn.net/littlehedgehog/article/details/2259665\n\
温馨提示：您需要在代码每行末尾添加符号\\以符合内联汇编格式',
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
        'part2':'}'
    }
    return jsonify(data)