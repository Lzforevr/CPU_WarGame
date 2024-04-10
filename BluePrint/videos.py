from flask import Blueprint, render_template, send_from_directory, jsonify

bp = Blueprint("videos",__name__,url_prefix='/videos')


@bp.route('/text')
def Text():
    txt = {
        'text1':'cat1 从内存中读取图片数据',
        'text2':'cat2 从内存中还原图像',
        'text3':'memdump 破解一段内存中的文字',
        'text4':'spy 监听文本缓冲区的输入内容'
    }
    return jsonify(txt)


@bp.route('/v1')
def Video_1():
    return send_from_directory('static',"cat1.mp4")


@bp.route('/v2')
def Video_2():
    return send_from_directory('static',"cat2.mp4")


@bp.route('/v3')
def Video_3():
    return send_from_directory('static',"memdump.mp4")


@bp.route('/v4')
def Video_4():
    return send_from_directory('static',"spy.mp4")

