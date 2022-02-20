import random

# from ronglian_sms_sdk import SmsSDK
from datetime import datetime

from flask import make_response, request, current_app, jsonify, session
from info import redis_store, constants, db
from info.models import User

from . import passport_blue
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
import json
import re

@passport_blue.route('/logout', methods=['POST'])
def logout():
    '''用户退出'''
    # 1. 清楚session信息
    session.pop('user_id', None)
    session.pop('is_admin', None)

    # 2. 返回响应
    return jsonify(code=RET.OK, data={}, message='退出成功')

@passport_blue.route('/login', methods=['POST'])
def login():
    '''
    登陆
    1. 获取参数
    2. 检验参数
    3. 通过手机号到数据库查询用户对象
    4. 确认用户是否存在
    5. 校验密码是否正确
    6. 讲用户登录信息保存在session中
    7. 返回响应
    :return:
    '''
    # 1. 获取参数
    mobile = request.json.get('mobile')
    password = request.json.get('password')
    # 2. 检验参数
    if not all([mobile, password]):
        return jsonify(code=RET.NODATA, message='参数不完整')

    # 2.1 判断手机号
    if not re.match('1[3-9]\d{9}', mobile):
        return jsonify(code=RET.DATAERR, messge='手机格式错误')

    # 3. 通过手机号到数据库查询用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='获取用户信息失败')

    # 4. 确认用户是否存在
    if not user:
        return jsonify(code=RET.NODATA, message='用户不存在')

    # 5. 校验密码是否正确
    if not user.check_password(password):
        return jsonify(code=RET.DATAERR, message='密码输入错误')

    # 6. 讲用户登录信息保存在session中
    session['user_id'] = user.id

    # 6.1记录用户最后一次登录时间
    user.last_login = datetime.now()
    # try:
    #     db.session.commit()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(code=RET.DBERR, data={}, message='时间记录失败')

    # 7. 返回响应
    return jsonify(code=RET.OK, data={}, message='登录成功')

@passport_blue.route('/register', methods=['POST'])
def register():
    '''
    注册
    :params mobile password image_code
    1. 获取参数
    2. 校验参数不能为空
    3. 手机号作为key，取出redis中的短信验证码
    4. 判断短信验证码是否过期
    5. 判断短信验证码是否正确
    6. 删除短信验证码
    7. 创建用户对象
    8. 设置用户对象属性
    9. 保存用户到数据库
    10. 返回响应
    :return:
    '''
    # 1. 获取参数
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')
    sms_code = dict_data.get('sms_code')

    # 2. 校验参数不能为空
    if not all([mobile, password, sms_code]):
        return jsonify(code=RET.PARAMERR, messge='缺少参数')

    if not re.match('1[3-9]\d{9}', mobile):
        return jsonify(code=RET.DATAERR, messge='手机格式错误')

    # 3. 手机号作为key，取出redis中的短信验证码
    try:
        redis_sms_code = redis_store.get(mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='读取验证码失败')

    #4. 判断短信验证码是否过期
    if not redis_sms_code:
        return jsonify(code=RET.NODATA, message='短信验证码已过期')

    # 5. 判断短信验证码是否正确
    if str(sms_code) != redis_sms_code:
        return jsonify(code=RET.PARAMERR, message='短信验证码错误')

    # 6. 删除短信验证码
    try:
        redis_store.delete(mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='no')

    # 7. 创建用户对象
    user = User()
    # 8. 设置用户对象属性
    user.nick_name = mobile
    user.password = password # 使用模型类加密算法
    user.mobile = mobile
    user.signature = '该用户很懒，什么都没写'
    # 9. 保存用户到数据库
    try:
        print(user)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='用户注册失败')
    # 10. 返回响应
    return jsonify(code=RET.OK, message='注册成功')

@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    # accId = '8aaf07087249953401728cd13b4420f1'
    # accToken = '16ef490ff19044788942064de145d1e8'
    # appId = '8a216da87e0e3ea7017e1575947a0121'

    # 获取参数
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')
    print(mobile, image_code, image_code_id)

    # 2. 校验参数
    if not all ([mobile, image_code, image_code_id]):
        return jsonify(code=RET.PARAMERR, message='参数不完整')

    # 3. 校验参数手机格式
    if not re.match('1[3-9]\d{9}', mobile):
        return jsonify(code=RET.DATAERR, messge='手机格式错误')

    # 4.从redis中区出图片验证码CSRF
    try:
        redis_image_code = redis_store.get('image_code%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='操作redis失败')

    # 5. 判断图片验证码是否过期
    if not redis_image_code:
        return jsonify(code=RET.NODATA, message='图片验证码已经过期')

    # 6. 判断图片验证码是否正确
    if image_code != redis_image_code:
        return jsonify(code=RET.NODATA, message='图片验证码错误')

    # 7. 删除图片验证码
    try:
        redis_store.delete('image_code%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 生成随机码
    sms_code = '%06d'%random.randint(0, 999999)

    # # 4. 发送短信调用封装好的发送短信代码， 目前没有短信直接接口返回短信验证码
    # sdk = SmsSDK(accId, accToken, appId)
    # tid = '容联云通讯平台创建的模板'
    # mobile = mobile
    # datas = ('变量1', '变量2')
    # resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)

    # 9. 将短信保存到redis中
    try:
        redis_store.set(mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='短信发送失败')

    # if resp == -1:
    #     return jsonify(code=3000, message='短信发送失败')
    # 5. 返回发送状态
    return jsonify(code=0, data={ 'code': sms_code }, message='短信发送成功')

@passport_blue.route('/image_code')
def image_code():

    # 1. 获取前端的参数
    cur_id = request.args.get('cur_id')

    name, text, image_data = captcha.generate_captcha()
    print(name, text)

    try:
        # 2. 保存到redis
        redis_store.set('image_code%s'%cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return '图片验证码获取失败'

    # 返回图片
    resp = make_response(image_data)

    resp.headers["Content-Type"] = "image/jpg"
    return resp

    # return image_data




