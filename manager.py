from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)


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