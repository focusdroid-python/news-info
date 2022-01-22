from flask import Blueprint

# 1. 创建用户对象
user_blue = Blueprint('user', __name__, url_prefix='/user')

# 装饰视图函数
from . import views