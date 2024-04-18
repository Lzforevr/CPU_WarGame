from flask import Blueprint, jsonify
import random

bp = Blueprint("tips", __name__, url_prefix='/tips')


@bp.route('/game1', methods=['POST'])
def Tip1():
    Num = '012345'*6
    num = int(''.join(random.sample(Num,1)))
    all_tips = ['volatile是一个可供跳转循环的起始点','我们将读取到的内核地址上的内容*4KB。再将这个值通过我们\
256页的探测数组间接读取内核地址的内容','访问“页数”为内核地址内容的地址，在cache中\
留下我们访问过此处的印记！这样我们就能用FLush_Reload重新找到这个地方！','哈哈，没有更多提示啦！','可以用如此庞大的数组中，\
可以被访问过内存的位置，来间接确定我们的物理地址','meltdown并不是通常会失败。这是因为我们只有赶在CPU发现异常之前，将内\
核地址读到cache上，才会成功触发。但是我们可以采用提高meltdown次数，以提高成功率','使用%rcx上的内核地址运算时，\
如果被安全检查制止，则会返回“0”。这是一个失败的标志。但是我们可以借此重新实施meltdown']
    rt = {
        "code": 200,
        "msg": all_tips[num]
    }
    return jsonify(rt)


@bp.route('/game2', methods=['POST'])
def Tip2():
    Num = '012'*3
    num = int(''.join(random.sample(Num,1)))
    all_tips = ['将系统读取时间与该值作比较，可以判断出我们指向的区域是否被已经缓存！','记得在最后重新剔除该区域在cache的缓存，\
    用于下次flush_reload探测','可以利用读取内存的前后时间戳计算出读取内存所用的时间！']
    rt = {
        "code": 200,
        "msg": all_tips[num]
    }
    return jsonify(rt)


@bp.route('/game3', methods=['POST'])
def Tip3():
    Num = '0123'*4
    num = int(''.join(random.sample(Num,1)))
    all_tips = ['tip1','tip2','tip3','tip4']
    rt = {
        "code": 200,
        "msg": all_tips[num]
    }
    return jsonify(rt)
