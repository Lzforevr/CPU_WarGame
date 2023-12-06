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


def ssh_command(command):
    with fabric.Connection(configs.USER + configs.IP) as conn:
        result = conn.run(command, hide=False)
        print(result.stdout)
        return result.ok
        

def upload(filename):
    upload = f'scp D:/Pycharm/CPU_wargame/flask_framework/C_Files/{filename} cpu@10.122.218.87:/home' \
                         f'/cfiles'
    os.system(upload)
    print('c文件上传成功')


def cstruct(prename):
    construct = f'cd /home/cfiles && touch {prename[0]}.txt'
    result = ssh_command(construct)
    if result:
        print('成功创建远程文件')
    else:
        print('创建远程文件失败')


def cpile(pre_task):
    compile_words = pre_task+{'> /home/cfiles/{prename[0]}.txt 2>&1'}
    result = ssh_command(compile_words)
    if result:
        print('成功编译运行')
    else:
        print('编译运行失败')
    
    
def download(prename):
    download = f"scp cpu@10.122.218.87:/home/cfiles/{prename[0]}.txt D:/Pycharm/CPU_wargame" \
               f"/flask_framework" \
               f"/Rturnfiles"
    os.system(download)
    print('成功下载输出文件')


