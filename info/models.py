from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from info import constants
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


# 用户收藏表，建立用户与其收藏新闻多对多的关系
tb_user_collection = db.Table(
    "info_user_collection",
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),  # 新闻编号
    db.Column("news_id", db.Integer, db.ForeignKey("info_news.id"), primary_key=True),  # 分类编号
    db.Column("create_time", db.DateTime, default=datetime.now)  # 收藏创建时间
)

tb_user_follows = db.Table(
    "info_user_fans",
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)  # 被关注人的id
)


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(db.String(10),  # 订单的状态
        db.Enum(
            "M",  # 男
            "F"  # 女
        ),
        default="M")

    # 当前用户收藏的所有新闻
    collection_news = db.relationship("News", secondary=tb_user_collection, lazy="dynamic")  # 用户收藏的新闻
    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    followers = db.relationship('User',
                                secondary=tb_user_follows,
                                primaryjoin=id == tb_user_follows.c.followed_id,
                                secondaryjoin=id == tb_user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')

    # 当前用户所发布的新闻
    news_list = db.relationship('News', backref='user', lazy='dynamic')

    # 使用@property装饰的方法，可以当成书醒来使用，比如print(user.password)
    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        # 使用系统加密算法
        self.password_hash = generate_password_hash(value)

    # 传递密文和明文方法返回时True或者False
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
            "mobile": self.mobile,
            "gender": self.gender if self.gender else "M",
            "signature": self.signature if self.signature else "",
            "followers_count": self.followers.count() if self.followers else "",
            "news_count": self.news_list.count() if self.news_list else ""
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict


class News(BaseModel, db.Model):
    """新闻"""
    __tablename__ = "info_news"

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    category_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"))  # 当前新闻的作者id
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    # 当前新闻的所有评论
    comments = db.relationship("Comment", lazy="dynamic")

    def to_review_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "static": self.status,
            "reason": self.reason if self.reason else ""
        }
        return resp_dict

    def to_basic_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "index_image_url": self.index_image_url,
            "clicks": self.clicks,
        }
        return resp_dict

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "comments_count": self.comments.count(),
            "clicks": self.clicks,
            "status": self.status,
            "category": self.category.to_dict() if self.category else None,
            "index_image_url": self.index_image_url,
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict


class Comment(BaseModel, db.Model):
    """评论"""
    __tablename__ = "info_comment"

    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("info_news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("info_comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "news_id": self.news_id,
            "like_count": self.like_count
        }
        return resp_dict


class CommentLike(BaseModel, db.Model):
    """评论点赞"""
    __tablename__ = "info_comment_like"
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("info_comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True)  # 用户编号


class Category(BaseModel, db.Model):
    """新闻分类"""
    __tablename__ = "info_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    status = db.Column(db.String(10), db.Enum(
            "0",  # 删除
            "1"  # 正常显示
        ),
        default="1")
    news_list = db.relationship('News', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict

# from datetime import datetime
# from info import constants
# from werkzeug.security import generate_password_hash, check_password_hash
#
# from . import db
#
# class BaseModel(object):
#     """模型基类 为每个模型补充创建时间和更新时间"""
#     __abstract__ = True
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # 记录更新时间
#
#
# tb_user_collection = db.Table(
#     'info_user_collection',
#     # db.Column('user_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True), # 新闻编号
#     # db.Column('news_id', db.Integer, db.ForeignKey('info_news_id'), primary_key=True), # 分类编号
#     db.Column('create_time', db.DateTime, default=datetime.now) # 收藏创建时间
# )
#
# ta_user_follows = db.Table(
#     'info_user_fans',
#     # db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True), # 粉丝ID
#     # db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True) # 被关注的人
#     db.Column('create_time', db.DateTime, default=datetime.now) # 收藏创建时间
# )
#
# class User(BaseModel, db.Model):
#     '''用户'''
#     __tablename__ = 'info_user'
#     __table_args__ = {"extend_existing": True}
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 用户编号
#     nick_name = db.Column(db.String(32), unique=True, nullable=False) # 用户昵称
#     password_hash = db.Column(db.String(128), nullable=False) # 加密的密码
#     mobile = db.Column(db.String(11),  unique=True, nullable=False) # 手机号
#     avatar_url = db.Column(db.String(256)) # 用户头像
#     last_login = db.Column(db.DateTime, default=datetime.now) # 最后一次登录时间
#     is_admin = db.Column(db.Boolean, default=False) #
#     signature = db.Column(db.String(512)) # 用户签名
#     gender = db.Column(
#         db.Enum(
#             'M',
#             'F'
#         ), default="M"
#     )
#
#     # 当前用户收藏所有新闻
#     collection_news = db.relationship('News', secondary=tb_user_collection, lazy='dynamic') # 用户收藏的新闻
#
#     # 用户所有的粉丝，添加饭洗那个引用followed，代表用户关注了那些人
#     # followers = db.relationship('User',
#     #                             secondary=tb_user_follows,
#     #                             primaryjoin=id == tb_user_followed.c.followed_id,
#     #                             secondaryjoin=id == tb_user_followed.c.followed_id,
#     #                             backref=db.backref('followed', lazy='dynamic'),
#     #                             lazy='dynamic'
#     #                             )
#
#     # 当前用户所发布的新闻
#     new_list = db.relationship('News', backref='user', lazy='dynamic')
#
#     @property
#     def password(self):
#         raise AttributeError('当前属性不可读')
#
#     def password(self, value):
#         self.password_hash = generate_password_hash(value)
#
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def to_dict(self):
#         resq_dict = {
#             'id': self.id,
#             'nick_name': self.nick_name,
#             'avatar_url': constants.QINIU_DOMAIN_PREFIX+self.avatar_url if self.avatar_url else '',
#             'mobile': self.mobile,
#             'gender': self.gender if self.gender else 'M',
#             'signature': self.signature if self.signature else '',
#             'followers': self.followers.count(),
#             'news_count': self.news_list.count(),
#         }
#         return resq_dict
#
#
#     def to_admin_dict(self):
#         resq_dict = {
#             'id': self.id,
#             'nick_name': self.nick_name,
#             'mobile': self.mobile,
#             'register': self.create_time.strptime('%Y-%m-%s %H:%M:%S'),
#             'last_login': self.last_login.strptime('%Y-%m-%s %H:%M:%S'),
#         }
#         return resq_dict
#
#
# class News(BaseModel, db.Model):
#     '''新闻'''
#     __tablename__ = 'info_news'
#     __table_args__ = {"extend_existing": True}
#
#     id = db.Column(db.Integer, primary_key=True) # 新闻编号
#     title = db.Column(db.String(256), nullable=False) # 新闻标题
#     source = db.Column(db.String(64), nullable=False) # 新闻来源
#     digest = db.Column(db.String(512), nullable=False) # 新闻摘要
#     content = db.Column(db.Text, nullable=False) # 新闻内容
#     clicks = db.Column(db.Integer, default=0) # 浏览量
#     index_image = db.Column(db.String(256)) # 新闻列表图片路径
#     # category_id = db.Column(db.Integer, db.ForeignKey('info_category.id')) # 新闻分类
#     user_id = db.Column(db.String(128), nullable=False) # 用户编号
#     status = db.Column(db.Enum('OFF','LINE'), default='OFF') # 新闻状态
#
#
#
