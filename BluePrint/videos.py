from flask import Blueprint, render_template, send_from_directory, jsonify

bp = Blueprint("videos",__name__,url_prefix='/videos')


@bp.route('/text')
def Text():
    txt = {
        'text1':'',
        'text2':'',
        'text3':'',
        'text4':''
    }
    return jsonify(txt)

@bp.route('/v1')
def Video_1():
    return send_from_directory('static',"cat1.mp4")


@bp.route('/v2')
def Video_1():
    return send_from_directory('static',"cat2.mp4")


@bp.route('/v3')
def Video_1():
    return send_from_directory('static',"memdump.mp4")


@bp.route('/v4')
def Video_1():
    return send_from_directory('static',"spy.mp4")

