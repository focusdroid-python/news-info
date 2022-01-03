import logging
from datetime import timedelta

from flask import Flask
from redis.client import StrictRedis


class Config(object):
    # 调试信息
    DEBUG = True
    SECRET_KEY = 'TBSEBFAF8998eb9afenajfv'

    # mysql数据库配置信息
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/info'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/info'
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 每当改变数据库内容，是凸函数结束的时候都会自动提交

    # redis 配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = 'redis' # 设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT) # 指定session存储的redis服务器
    SESSION_USE_SIGNER = True # 设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=10) # 设置session有效期

# 开发环境配置信息
class DevelopConfig(Config):
    LEVEL_NAME = logging.DEBUG

# 生产环境配置信息
class ProductConfig(Config):
    LEVEL_NAME = logging.ERROR


# 测试环境
class TestConfig(Config):
    DEBUG = False


# 提供统一的访问入口
config_dict = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "test": TestConfig
}




