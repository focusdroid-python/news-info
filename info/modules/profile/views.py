import random

# from ronglian_sms_sdk import SmsSDK
from datetime import datetime

from flask import make_response, request, current_app, jsonify, session, g
from info import redis_store, constants, db
from info.models import User, News

from . import profile_blue
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
import json
import re
from info.utils.common import user_login_data

# - 实现思路
# 1.
# 获取参数
# - 2.
# 参数类型扎古换
# - 分页查询用互关注列表的人
# - 取出分页对象的数据，总页数，当前页对象
# - 将对象列表转成对象
@profile_blue.route('/user_follow')
@user_login_data
def user_follow():
    '''
    # 1.获取参数
    # 2.参数类型扎古换
    # 3.分页查询用互关注列表的人
    # 4.取出分页对象的数据，总页数，当前页对象
    # 5.将对象列表转成对象
    :return:
    '''

    # 1.获取参数
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')
    # 2.参数类型装换
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exceprion as e:
        page_num = int(page_num)
        page_size = int(page_size)
        current_app.logger.error(e)
    # 3.分页查询用互关注列表的人
    try:
        # paginate = g.user.collection_news.order_by(News.create_time.desc()).paginate(page_num, page_size, False)
        paginate = g.user.followed.paginate(page_num, page_size, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg='获取新闻失败')

    # 4.取出分页对象的数据，总页数，当前页对象
    total = paginate.total
    current_page = paginate.page
    items = paginate.items

    follow_list = []
    for item in items:
       follow_list.append(item.to_dict())


    # 5.将对象列表转成对象
    data = {
        'total': total,
        'current_page': current_page,
        'follow_list': follow_list
    }

    return jsonify(error=RET.OK, data=data, errmsg='success')


# 用户新闻列表
# 请求路径 /user/news_list
# 请求方式： get
# 请求参数：p
# 返回值get 请求渲染user_news_listu

@profile_blue.route('/news_list')
@user_login_data
def news_list():
    '''
    # 1. 获取参数
    # 2. 校验参数，不能为空
    # 3. 查询用户发布的新闻，分页
    # 4. 接口返回数据
    # 5.
    # 6.
    # 7.
    :return:
    '''
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')


    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = int(page_num)
        page_size = int(page_size)

    paginate = News.query.filter(News.user_id == g.user.id).order_by(News.create_time.desc()).paginate(page_num, page_size, False)

    total = paginate.total
    current = paginate.page
    items = paginate.items

    list = []
    for item in items:
        list.append(item.to_dict())

    data = {
        'list': list,
        'total': total,
        'current': current,
    }
    return jsonify(code=200, data=data, message='success')