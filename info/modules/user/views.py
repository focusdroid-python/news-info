from flask import jsonify, g, request, current_app
from . import user_blue
from info.utils.common import user_login_data
from info.utils.response_code import RET
from info.models import User
from info import db


@user_blue.route('/password', methods=['GET', 'POST'])
@user_login_data
def change_password():
    '''
    修改密码
    # 1. post请求，获取参数
    # 2. 校验参数
    # 3. 旧密码是否正确
    # 4. 设置新密码
    # 5. 返回响应
    :return:
    '''
    # 1. post请求，获取参数
    if not g.user:
        return jsonify(error=RET.NODATA, messgae='用户未登录')
    # 2. 校验参数
    current_password = request.json.get('current_password')
    new_pwd = request.json.get('new_password')
    if not all([current_password, new_pwd]):
        return jsonify(error=RET.DATAERR, messgae='参数不全')
    # 3. 旧密码是否正确
    pwd = User.query.get(g.user.id)
    if not pwd.check_password(current_password):
        return jsonify(error=RET.DATAERR, message='旧密码输入错误')
    # 4. 设置新密码
    pwd.password = new_pwd
    # 5. 返回响应
    return jsonify(errno=RET.OK, data=g.user.to_dict(), message='success')


@user_blue.route('/pic_info', methods=['GET', 'POST'])
@user_login_data
def pic_info():
    '''
    上传头像
    :return:
    '''
    if not g.user:
        return jsonify(error=RET.NODATA, messgae='用户未登录')
    # 1. 获取请求方式get，返回头像链接
    if request.method == 'GET':
        return jsonify(error=RET.OK, data=g.user.to_dict(), message='success')
    # 2. 如果是post请求，就是上传图像
    if request.method == 'POST':
        pass
    # 3. 获取相关参数
    # 4. 校验参数
    # 5. 上传头像判断是否上传成功
    # 6. 将图片设置到用户对象
    # 7. 返回响应

@user_blue.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_userinfo():
    '''
    用户基本信息
        # 1. 判断请求方式，如果是get请求，返回用户数据，如果是post就是提交数据

        # 2. 写到用户数据，渲染页面
        # 3. 如果是post请求
        # 4. 获取参数
        # 5. 校验参数
        # 6. 修改用户数据
        # 7. 返回响应
    :return:
    '''
    if not g.user:
        return jsonify(error=RET.NODATA, messgae='用户未登录')
    # 1. 判断请求方式，如果是get请求，返回用户数据，如果是post就是提交数据
    if request.method == 'GET':
        data = {
            'user_info': g.user.to_dict()
        }
        return jsonify(error=RET.OK, data=data, message='success')
    # 2. 写到用户数据，渲染页面
    # 3. 如果是post请求
    if request.method == 'POST':
        nick_name = request.json.get('nick_name')
        signature = request.json.get('signature')
        gender = request.json.get('gender')
    # 4. 获取参数

    # 5. 校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(error=RET.DATAERR, messgae='参数不全')
    # 6. 修改用户数据
    if not gender in ['F', 'M']:
        return jsonify(error=RET.DATAERR, messgae='性别参数异常')
    # 7. 返回响应
    user = User.query.get(g.user.id)
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender

    # g.user.signature = signature
    # g.user.nick_name = nick_name
    # g.user.gender = gender

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.NODATA, messgae='添加数据异常')
    return jsonify(errno=RET.OK, message='success')

@user_blue.route('/user_index')
@user_login_data
def user_index():
    '''
    用户设置
    :return:
    '''
    if g.user:
        return jsonify(error=RET.NODATA, messgae='用户未登录')

    data = {
        'user_info': g.user.to_dict()
    }
    return jsonify(error=RET.OK, data=data, message='success')
