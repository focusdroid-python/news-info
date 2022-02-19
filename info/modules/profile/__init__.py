from flask import Blueprint


# 创建认证蓝图对象
profile_blue = Blueprint('profile', __name__, url_prefix='/profile')

# 导入view装饰视图对象
from . import views