from datetime import timedelta

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)


class Config(object):
    # 调试信息
    DEBUG = True
    SECRET_KEY = 'TBSEBFAF8998eb9afenajfv'

    # mysql数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/info'
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    # redis 配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = 'redis' # 设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT) # 指定session存储的redis服务器
    SESSION_USE_SIGNER = True # 设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=10) # 设置session有效期



app.config.from_object(Config)


db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 创建session对象， 读取session配置信息
Session(app)

# 使用CSRFProtect 保护应用
CSRFProtect(app)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    # 测试redis村数据
    redis_store.set("name", "focusdroid")
    print(redis_store.get("name"))

    # 测试session存储
    session['age'] = 30
    session['address'] = 'shanghai'


    return 'hello'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)