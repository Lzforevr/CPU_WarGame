import hashlib
import os
import fabric
from flask import current_app
import configs


def get_md5(pwd):
    """MD5加密处理"""
    md5 = hashlib.md5()  # 创建md5对象
    key = current_app.config.get('SECRET_KEY')
    pwd += key
    md5.update(pwd.encode("utf-8"))
    return md5.hexdigest()  # 返回密文w


def allowed_file(filename):
    # 通过rsplit方法拆分文件名，得到扩展名的小写，判断是否存在于config里，返回0/1
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in configs.ALLOWED_EXTENSIONS

##########################
# 暂时使用虚拟机进行测试
##########################
# cpu@10.122.218.87:/home/cpu/meltdown_long为靶机IP及目录
# lz@10.21.162.136:/home/lz/meltdown 为虚拟机IP及目录


def ssh_command(command):
    with fabric.Connection(user=configs.USER_V, host=configs.IP_V,connect_kwargs={'key_filename':'C:/Users/86189/.ssh/virtual_machine'}) as conn:
        result = conn.run(command, hide=True)
        print(result.stderr)
        return result.ok


def upload(filename):
    with fabric.Connection(user=configs.USER_V,host=configs.IP_V,connect_kwargs={'key_filename':configs.PRIVATE_KEY_V}) as conn:
        conn.put(f'D:/Pycharm/CPU_wargame/flask_framework/C_Files/{filename}','/home/lz/meltdown')
        print('c文件上传成功')


def cstruct(prename):
    construct = f'cd /home/lz/meltdown && touch {prename[0]}.txt'
    result = ssh_command(construct)
    if result:
        print('成功创建远程文件')
    else:
        print('创建远程文件失败')


# 通过这一复杂命令利用libkdump库编译成可执行文件
def make_file(prename):
    make = f'gcc -o /home/lz/meltdown/{prename[0]} /home/lz/meltdown/{prename[0]}.c -L/home/lz/meltdown/libkdump -Ilibkdump -lkdump -static -O3 -pthread ' \
           f'-Wno-attributes -m64'
    return make


def execute(pre_task, prename):
    compile_words = f'{pre_task} > /home/lz/meltdown/{prename[0]}.txt'
    result = ssh_command(compile_words)
    if result:
        print(f'{prename[0]}成功运行')
    else:
        print(f'{prename[0]}运行失败')


# 注意使用fabric.put
def download(prename0):
    with fabric.Connection(user=configs.USER_V,host=configs.IP_V,connect_kwargs={'key_filename':'C:/Users/86189/.ssh/virtual_machine'}) as conn:
        conn.get(f'/home/lz/meltdown/{prename0}.txt',local=f'D:/Pycharm/CPU_wargame/flask_framework/Rturnfiles/{prename0}.txt')
        print(f'成功下载输出:{prename0}')


def return_content(file):
    lines = file.readlines()
    content = ''.join(lines[-5:])
    print(content)  # 打印 content
    return content


def final_line(file):
    lines = file.readlines()
    content = ''.join(lines[-1:])
    return content


def out_line(file):
    lines = file.readlines()
    content = ''.join(lines[-3:])
    return content
