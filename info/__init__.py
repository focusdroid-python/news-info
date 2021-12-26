import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config_dict


# 定义redis变量
redis_store = None

def create_app(config_name):
    # 调用日志方法，记录程序运行信息
    log_file()
    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    # 调用日志方法方法记录程序运行信息
    log_file(config.LEVEL_NAME)

    app.config.from_object(config)

    db = SQLAlchemy(app)

    # 创建redis对象
    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 创建session对象， 读取session配置信息
    Session(app)

    # 使用CSRFProtect 保护应用
    CSRFProtect(app)

    # 将蓝图注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    return app

def log_file(LEVEL_NAME):
    logging.basicConfig(level=LEVEL_NAME)
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=100)
    formatter = logging.Formatter('levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)

