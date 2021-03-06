import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import config_dict


# 定义redis变量
redis_store = None

# db = None
db = SQLAlchemy()

def create_app(config_name):
    # 调用日志方法，记录程序运行信息
    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    # 调用日志方法方法记录程序运行信息
    log_file(config.LEVEL_NAME)

    app.config.from_object(config)

    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 创建session对象， 读取session配置信息
    Session(app)

    # 使用CSRFProtect 保护应用
    # if not request.url.endswith('/user/get_csrf_token'):
    # CSRFProtect(app)

    # 将首页蓝图注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    # 将认证蓝图passport_blue注册到app中
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    # 将news认证蓝图注册到app中
    from info.modules.news import new_blue
    app.register_blueprint(new_blue)

    # 将用户蓝图注册到app中
    from info.modules.user import user_blue
    app.register_blueprint(user_blue)

    # 将蓝图注册到app中
    from info.modules.profile import profile_blue
    app.register_blueprint(profile_blue)

    # 将管理员蓝图注册到app中
    from info.modules.admin import admin_blue
    app.register_blueprint(admin_blue)

    # 使用请求钩子拦截所有请求，通过在cookie中设置csrs_token
    # @app.after_request
    # def after_request(resp=None):
    #     csrf_token = generate_csrf() # 获取csrftoken
    #     resp.set_cookie('csrf_token', csrf_token) # 将csrf_token保存在浏览器中
    #     return resp

    # "X-CSRFToken", "X-CSRF-Token" 前端在headers中保存着两个字段

    print(app.url_map)
    return app

def log_file(LEVEL_NAME):
    logging.basicConfig(level=LEVEL_NAME)
    file_log_handler = RotatingFileHandler('logs/logs', maxBytes=1024 * 1024 * 100, backupCount=100)
    formatter = logging.Formatter('levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)

