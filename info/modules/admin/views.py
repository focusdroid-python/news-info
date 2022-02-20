import json
import time
from datetime import datetime
from . import admin_blue
from flask import request, session, jsonify, current_app
from info.models import User
from info.utils.response_code import RET

@admin_blue.route('/user_count', methods=['GET'])
def user_count():
    '''
    # 1. 获取用户总数
    # 2. 获取月活人数
    # 3。 获取日活人数
    # 4. 获取活跃时间段内，对应的活跃人数
    # 5. 携带数据渲染页面
    :return:
    '''

    # 1. 获取用户总数
    try:
        total_count = User.query.filter(User.is_admin == False).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, data={}, message='获取总人数失败')

    # 2. 获取月活人数
    localtime = time.localtime()
    try:
        # 最后一次登陆的时间大于，本月的1号的0点的人数
        # 2.1获取本月的1号的0点的字符串数据
        month_start_time_str = '%s-%s-01'%(localtime.tm_year, localtime.tm_mon)
        # 2.2 根据字符串格式化对象
        month_start_time_date = datetime.strptime(month_start_time_str, '%Y-%m-%d')

        month_count = User.query.filter(User.last_login >= month_start_time_date).count()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, data={}, message='获取月活失败')
    # 3。 获取日活人数
    try:
        # 最后一次登陆的时间大于，本月的1号的0点的人数
        # 2.1获取当天的时间字符串数据
        day_start_time_str = '%s-%s-%s' % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        # 2.2 根据字符串格式化对象
        day_start_time_date = datetime.strptime(day_start_time_str, '%Y-%m-%d')

        day_count = User.query.filter(User.last_login >= day_start_time_date).count()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, data={}, message='获取月活失败')
    # 4. 获取活跃时间段内，对应的活跃人数
    for i in range(0,7):
        pass
    # 5. 携带数据渲染页面
    data = {
        'total_count': total_count,
        'month_count': month_count,
        'day_count': day_count,
    }
    return jsonify(code=RET.OK, data=json.dumps(data, cls = MyEncoder, indent=4), message='success')

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


@admin_blue.route('/login', methods=['POST'])
def admin_login():
    '''
    # 1. 判断请求方式，如果是get直接渲染页面，
    # 2. 如果是POST请求，获取参数
    # 3. 校验参数，获取参数
    # 4. 根据用户取出管理员对象，判断管理员是否存在
    # 5.判断管理员是的密码是否正确
    # 6。管理员的session信息记录
    # 7.重定向首页
    :return:
    '''

    # 1. 判断请求方式，如果是get直接渲染页面，
    if request.method == 'GET':
        return jsonify(code='', data={}, message='')
    # 2. 如果是POST请求，获取参数
    username = request.json.get('username')
    password = request.json.get('password')

    # 3. 校验参数，获取参数
    if not all([username, password]):
        return jsonify(code='40001', data={}, message='参数不全')
    # 4. 根据用户取出管理员对象，判断管理员是否存在
    try:
        admin = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code='40001', data={}, message='管理员用户查询失败')
    # 5.判断管理员是的密码是否正确
    if not admin:
        return jsonify(code='', data={}, message='管理员不存在')
    # 6。管理员的session信息记录
    if not admin.check_password(password):
        return jsonify(code='', data={}, message='密码错误')
    # 7.重定向首页
    session['user_id'] = admin.id
    session['is_admin'] = True

    return 'admin_login'