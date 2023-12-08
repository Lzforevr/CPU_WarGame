from flask import Blueprint, request, session, render_template, jsonify
from model import User_data

bp = Blueprint("main", __name__, url_prefix=None)
required_login = ['/games', '/rank', '/library']


@bp.after_request
def after_request(response):
    response.headers.add('Content-Type', 'application/json')
    return response


# 闯关题目路由
@bp.route('/games', methods=['GET', 'POST'])
def Games():
    if request.method == 'GET':
        return bp.send_static_file('index.html')
    else:
        pass


# 排行榜路由
@bp.route('/leaderboard')
def leaderboard():
    users = User_data.query.order_by(User_data.score.desc()).limit(10).all()
    result = [user.to_json() for user in users]
    return jsonify(result)


# 知识库路由
@bp.route('/library')
def Library():
    pass



