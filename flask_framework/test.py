import os,subprocess
uploads = 'scp D:/Pycharm/CPU_wargame/flask_framework/C_Files/pwn1.c cpu@10.122.243.55:/home/cfiles '
def upload(uploads):
    os.system(uploads)
    return 'ok'