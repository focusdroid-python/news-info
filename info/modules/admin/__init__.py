from flask import Blueprint, request, jsonify, session

# 1. 创建管理员蓝图对象
admin_blue = Blueprint('admin', __name__, url_prefix='/admin')


# 2. 装饰视图函数
from . import views

# 使用请求钩子，拦截用户请求
# 1. 拦截的是访问飞登录页面
# 2. 拦截的是普通用户

@admin_blue.before_request
def before_request():
    print(request.url)
    if request.url.endswith('/admin/login'):
        pass
    else:
        if session.get('is_admin'):
            pass
        else:
            return jsonify(code='error', data={}, message='该用户不是管理员')