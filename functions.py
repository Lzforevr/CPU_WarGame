import hashlib
import os
import fabric
import paramiko
from flask import current_app
from flask_socketio import SocketIO
from numpy.core.defchararray import rsplit

import configs


socket_io = SocketIO(cors_allowed_origins='*')


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


def ssh_command(command):
    with fabric.Connection(user=configs.USER, host=configs.IP,connect_kwargs={'key_filename':'C:/Users/86189/.ssh/id_rsa'}) as conn:
        result = conn.run(command, hide=True)
        print(result.stderr)
        return result.ok


# 游戏代码文件上传到远程机，paramiko库不失为另一种支持sftp的ssh连接方法
def game_upload(filename,remote_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=configs.IP, port=22, username=configs.USER, key_filename=configs.PRIVATE_KEY)
    local_path = f'D:/Pycharm/CPU_wargame/flask_framework/Writein_files/{filename}'
    sftp = ssh.open_sftp()

    try:
        sftp.put(local_path, remote_path)
        sftp.close()
        ssh.close()
        return f'文件:{filename} 上传成功'
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sftp.close()
        ssh.close()
        return f'文件上传失败：File not found: {e}'
    except IOError as e:
        print(f"IOError occurred: {e}")
        sftp.close()
        ssh.close()
        return f'文件上传失败：IOError occurred: {e}'
    except paramiko.SSHException as e:
        print(f"SSH exception: {e}")
        sftp.close()
        ssh.close()
        return f'文件上传失败：SSH exception: {e}'
    except Exception as e:
        print(f"Unexpected error: {e}")
        sftp.close()
        ssh.close()
        return f'文件上传失败：Unexpected error: {e}'


# 自定义libkdump.c的编译命令
def customed_make(name,cnt):
    if cnt == 'ST':
        make = f'gcc /home/bupt/hjl/meltdown/{name}.c -o /home/bupt/hjl/meltdown/{name} -m64 -L/home/bupt/hjl/meltdown/customc -I/home/bupt/hjl/meltdown/customc -lkdump -static -O3 -pthread ' \
               f'-Wno-attributes -m64'
        return make
    elif cnt == 'ND':
        make = f'gcc /home/bupt/hjl/meltdown/{name}.c -o /home/bupt/hjl/meltdown/{name} -m64 -L/home/bupt/hjl/meltdown/customh -I/home/bupt/hjl/meltdown/customh -lkdump -static -O3 -pthread ' \
               f'-Wno-attributes -m64'
        return make


# 示例代码上传函数
def upload(filename):
    with fabric.Connection(user=configs.USER,host=configs.IP,connect_kwargs={'key_filename':configs.PRIVATE_KEY}) as conn:
        result = conn.put(f'D:/Pycharm/CPU_wargame/flask_framework/C_Files/{filename}','/home/bupt/hjl/meltdown')
        print(result)
    if result:
        print('c文件上传成功')
        return f'文件:{filename} 上传成功'
    else:
        return 'c文件上传失败！'


def cstruct(prename):
    construct = f'cd /home/bupt/hjl/meltdown && touch {prename}.txt'
    result = ssh_command(construct)
    if result:
        print('成功创建远程文件')
        return f'成功创建远程文件:{prename}'
    else:
        print('创建远程文件失败')
        return '创建远程文件失败！'


# 通过这一复杂命令利用libkdump库编译成可执行文件
def make_file(prename):
    make = f'gcc /home/bupt/hjl/meltdown/{prename}.c -o /home/bupt/hjl/meltdown/{prename} -m64 -L/home/bupt/hjl/meltdown/libkdump -I/home/bupt/hjl/meltdown/libkdump -lkdump -static -O3 -pthread ' \
           f'-Wno-attributes -m64'
    return make


def execute(pre_task, prename):
    compile_words = f'{pre_task} > /home/bupt/hjl/meltdown/{prename[0]}.txt'
    result = ssh_command(compile_words)
    if result:
        print(f'{prename[0]}成功运行')
        return f'{prename[0]}成功运行'
    else:
        print(f'{prename[0]}运行失败')
        return '代码远程执行失败！'


# 注意使用fabric.put
def download(prename0):
    with fabric.Connection(user=configs.USER,host=configs.IP,connect_kwargs={'key_filename':'C:/Users/86189/.ssh/id_rsa'}) as conn:
        result = conn.get(f'/home/bupt/hjl/meltdown/{prename0}.txt',local=f'D:/Pycharm/CPU_wargame/flask_framework/Rturnfiles/{prename0}.txt')
        if result:
            print(f'成功下载输出:{prename0}')
            return f'成功下载输出{prename0}'
        else:
            return '执行结果下载失败！'


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
