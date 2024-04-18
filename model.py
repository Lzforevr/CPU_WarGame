from exts import db


# 配置数据库，涉及用户名、密码、邮箱、积分、验证码
class User_data(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    pwd = db.Column(db.String)
    email = db.Column(db.String(20), unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

    def to_json(self,rank):
        return {
            'id': rank,
            'name': self.username,
            'score': self.score
        }


class Captcha_data(db.Model):
    __tablename__ = 'captcha_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable=False)
    captcha = db.Column(db.String(4), nullable=False)
