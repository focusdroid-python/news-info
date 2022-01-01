from flask import Blueprint


# 创建认证蓝图对象
passport_blue = Blueprint('passport', __name__, url_prefix='/passport')

# 导入view装饰视图对象
from . import views