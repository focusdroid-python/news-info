from datetime import datetime
# from info import constants
from . import db

class BaseModel(object):
    """模型基类 为每个模型补充创建时间和更新时间"""
    __abstract__ = True
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # 记录更新时间


tb_user_collection = db.Table(
    'info_user_collection',
    db.Column('user_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True), # 新闻编号
    db.Column('news_id', db.Integer, db.ForeignKey('info_news_id'), primary_key=True), # 分类编号
    db.Column('create_time', db.DateTime, default=datetime.now) # 收藏创建时间
)

ta_user_follows = db.Table(
    'info_user_fans',
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True), # 粉丝ID
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True) # 被关注的人
)

class User(BaseModel, db.Model):
    '''用户'''
    __tablename__ = 'info_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False) # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False) # 加密的密码
    mobile = db.Column(db.String(11),  unique=True, nullable=False) # 手机号
    avatar_url = db.Column(db.String(256)) # 用户头像
    last_login = db.Column(db.DateTime, default=datetime.now) # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False) #
    signature = db.Column(db.String(512)) # 用户签名
    gender = db.Column(
        db.Enum(
            'M',
            'F'
        )
    )