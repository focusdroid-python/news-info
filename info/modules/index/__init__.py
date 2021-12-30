from flask import Blueprint


# 1. 创建蓝图对象
index_blue = Blueprint('index', __name__)

# 2. 导入view装饰函数
# from info.modules.index import views
from . import views