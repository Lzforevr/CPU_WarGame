import random
import string
import functions
import wtforms_json
from flask import Blueprint, request, jsonify, session
from flask import render_template, redirect, url_for
# 以下用于邮箱验证码
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from exts import mail, db
from forms import RegisterForm, LoginForm
from model import User_data, Captcha_data

# 再定义蓝图对象实例，分别设置蓝图名称，网址前缀
bp = Blueprint("user", __name__, url_prefix='/user')
wtforms_json.init()


# /user可作为查看用户个人信息的页面
@bp.route('/')
def Main():
    return 'OK'


@bp.route('/signUp', methods=["POST"])
def Register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    captcha = request.json.get('captcha')
    # 加密
    captcha_check = Captcha_data.query.filter_by(captcha=captcha).first()
    user_check = User_data.query.filter_by(email=email).first()
    if user_check:
        return jsonify({"code": 600, "msg": "该邮箱已被占用！", "data": None})
    elif captcha_check:
        user = User_data(username=username, pwd=generate_password_hash(functions.get_md5(password)), email=email)
        db.session.add(user)
        db.session.delete(captcha_check)
        db.session.commit()
        # 如若删除依次输入：db.session.delete(user), db.session.commit()
        print(f'新用户注册成功:{email}')
        return jsonify({"code": 200, "msg": "注册成功！", "data": None})  # 接口测试用
    else:
        return jsonify({"code": 500, "msg": "验证码错误", "data": None})


# else:
#     print(form.errors)
# return redirect(url_for('user.Register'))


@bp.route('/login', methods=['GET', 'POST'])
def Login():
    # form = LoginForm(request.form)  # 这里存在问题，当加上表单名时报错werkzeug.exceptions.BadRequestKeyError: 400 Bad Request:
    #                                 # The browser (or proxy) sent a request that this server could not understand. KeyError: 'login-form'
    email = request.json.get('email')
    password = request.json.get('password')
    user = User_data.query.filter_by(email=email).first()
    if not user:
        print('用户不存在')
        # return redirect(url_for('user.Login'))
        return jsonify({'code': 300, 'msg': '用户不存在', "data": None})
    elif check_password_hash(user.pwd, functions.get_md5(password)):
        print('登录成功')
        # 设置session加密储存登录状态到cookie里（再次访问域名时，会保持登录状态）
        session['user_id'] = user.id
        # return redirect(url_for('main.Games'))
        return jsonify({"code": 200, "msg": '登录成功', "data": None})

    else:
        print('密码错误')
        return jsonify({'code': 400, 'msg': '密码错误', 'data': None})


# 在js文件中点击“获取验证码”button后设置action属性为该函数路由，即可执行
@bp.route('/send_captcha', methods=['POST'])
def Send_captcha():
    form = request.json.get('email')
    # 选择4/6位数字，digits=‘0123456789’
    str = string.digits * 4
    captcha = random.sample(str, 4)
    # 将验证码转换为字符串形式
    captcha = ''.join(captcha)
    message = Message(subject='CPU_WarGame验证码', recipients=[form], body=f'您的验证码是：{captcha}')
    mail.send(message)
    # 将验证码上传服务器，使用memcached/redis缓存
    # 或用数据库表的方式存储（权宜之计，速度慢）
    email_captcha = Captcha_data(email=form, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # 测试时在导航栏输入？mail=qq邮箱即可，在终端输出验证码
    # 若验证成功
    print('已发送验证码')
    return jsonify({"code": 200, "message": '输入成功', 'data': None})
