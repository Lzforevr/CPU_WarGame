from flask import Blueprint, jsonify
import random

bp = Blueprint("tips", __name__, url_prefix='/tips')


@bp.route('/game1', methods=['POST'])
def Tips():
    Num = '0123'*4
    num = int(''.join(random.sample(Num,1)))
    all_tips = ['tip1','tip2','tip3','tip4']
    rt = {
        "code": 200,
        "msg": all_tips[num]
    }
    return jsonify(rt)

