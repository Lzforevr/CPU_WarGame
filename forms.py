from model import User_data, Captcha_data
from exts import db
import wtforms, email_validator
from wtforms.validators import Email, Length, EqualTo


# 验证前端数据是否符合格式及重复要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码错误！')])
    username = wtforms.StringField(validators=[Length(min=1, max=10, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=8, max=14, message='密码格式错误!')])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 数据库验证邮箱是否已被注册
    def validate_email(self, field):
        email = field.data
        user = User_data.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已被注册')

    # 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = Captcha_data.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')
        else:
            # 验证码一致，正好删除这条数据节省空间，缺点是与数据库打交道减慢网页速度
            db.session.delete(captcha_model)
            db.session.commit()



class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=1,max=15,message='用户名格式错误')])
    password = wtforms.StringField(validators=[Length(min=8,max=14,message='密码格式错误')])

    # def validate_email(self, field):
    #     email = field.data
    #     user =User_data.query.filter_by(email=email).first()
    #     if not user