### 本文件仅用于单一功能测试 ###

# import os,subprocess
# uploads = 'scp D:/Pycharm/CPU_wargame/flask_framework/C_Files/pwn1.c cpu@10.122.243.55:/home/cfiles '
# def upload(uploads):
#     os.system(uploads)
#     return 'ok'
with open('Rturnfiles/kaslr_test.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    total_lines = len(lines)
    lines = [line for line in lines]
    content = ''.join(lines[-5:])
    print(content)  # 打印 content
