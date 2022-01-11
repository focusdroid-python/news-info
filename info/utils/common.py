# 定义登陆装饰器
from functools import wraps

from flask import session, g


# 使用过滤器做登陆限制
def user_login_data(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        print(user_id)
        # 1. 根据新闻编号查询新闻对象
        if user_id:
            try:
                from info.models import User
                user = User.query.get(user_id)
            except Exception as e:
                from flask import current_app
                current_app.logger.error(e)
                # return jsonify(code=RET.DBERR, message='查询失败')
        g.user = user
        return view_func(*args, **kwargs)
    return wrapper