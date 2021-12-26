from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config_dict
from info.modules.index import index_blue

def create_app(config_name):
    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    app.config.from_object(config)

    db = SQLAlchemy(app)

    # 创建redis对象
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 创建session对象， 读取session配置信息
    Session(app)

    # 使用CSRFProtect 保护应用
    CSRFProtect(app)

    # 将蓝图注册到app中
    app.register_blueprint(index_blue)

    return app