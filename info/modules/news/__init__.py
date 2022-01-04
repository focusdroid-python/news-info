from flask import Blueprint


# 1. 创建蓝图对象

new_blue = Blueprint('news', __name__, url_prefix='/news')


from . import views