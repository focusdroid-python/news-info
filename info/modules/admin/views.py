import json
import time
from datetime import datetime
from . import admin_blue
from flask import request, session, jsonify, current_app
from info.models import User, News, Category
from info.utils.response_code import RET
from info import db

@admin_blue.route('/delete_category', methods=['POST'])
def delete_category():
    '''
    删除新闻分类 逻辑删除
    :return:
    '''
    id = request.json.get('id')

    try:
        cate_query = Category.query.filter(Category.id == id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询失败')

    if not cate_query:
        return jsonify(code=RET.DBERR, message='没有查询到相关数据')


    # cate = Category.query.filter(Category.id == id)

    cate_query.status = 0 # 罗技删除
    try:
        db.session.add(cate_query)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='delete error')

    return jsonify(code=RET.OK, message='delete success')


@admin_blue.route('/add_new_category', methods=['POST'])
def add_new_category():
    '''
    添加新闻分类
    :return:
    '''
    cate_name = request.json.get('cate') # 分类

    cate = Category()
    is_cate = Category.query.filter(Category.name == cate_name, Category.status != 0).first()
    if is_cate:
        return jsonify(code=RET.DBERR, message='改名称已经存在')
    cate.name = cate_name
    db.session.add(cate)
    db.session.commit()

    return jsonify(code=RET.OK, message='success')

@admin_blue.route('/news_category')
def news_category():
    '''
        新闻分类管理
    :return:
    '''
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')

    # 2. 校验参数(参数类型转换)
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = 1
        page_size = 10
        current_app.logger.error(e)

    category = Category.query.filter(Category.status == 1).order_by(Category.create_time.desc()).paginate(page_num, page_size, False)

    total = category.total
    current = category.page
    items = category.items

    category_list = []
    for item in items:
        category_list.append(item.to_dict())

    data = {
        'total': total,
        'current': current,
        'list': category_list
    }
    return jsonify(code=RET.OK, data=data, message='success')



@admin_blue.route('/search_content')
def search_content():
    '''
        # 1. 获取参数
        # 2. 校验参数
        # 3. 查询符合条件的数据，分页
        # 4. 格式化数据
        # 5. 返回数据
    :return:
    '''
    # 1. 获取参数
    value = request.args.get('value')
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')

    # 2. 校验参数(参数类型转换)
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = 1
        page_size = 10
        current_app.logger.error(e)

    filters = [News.status != 0]
    # 2. 校验参数
    if value:
        filters.append(News.title.contains(value))
    # 3. 查询符合条件的数据，分页
    news = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page_num, page_size, False)

    # 4. 格式化数据
    total = news.total
    current = news.page
    items = news.items
    search_list = []
    for item in items:
        search_list.append(item.to_dict())
    # 5. 返回数据
    data = {
        'total': total,
        'current': current,
        'list': search_list
    }
    return jsonify(code=RET.OK, data=data, message='success')


@admin_blue.route('/user_review_detail')
def user_review_detail():
    '''
    # 1.
    :return:
    '''
    id = request.args.get('id')

    try:
        news = News.query.get(int(id))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询数据库失败')

    data = {
        'data': news.to_dict()
    }

    return jsonify(code=RET.OK, data=data, message='success')

@admin_blue.route('/user_review')
def user_review():
    '''
    # 1. 获取参数
    # 2. 查询数据并进行分页
    # 3. 格式化数据
    # 4. 返回数据
    :return:
    '''
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')

    # 2. 校验参数(参数类型转换)
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = 1
        page_size = 10
        current_app.logger.error(e)

    try:
        news = News.query.filter().order_by(News.create_time.desc()).paginate(page_num, page_size, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询数据库失败')

    total = news.total
    current = news.page
    items = news.items

    news_list = []
    for item in items:
        news_list.append(item.to_basic_dict())

    data = {
        'total': total,
        'current': current,
        'list': news_list
    }
    return jsonify(code=RET.OK, data=data, message='cuccess')

@admin_blue.route('/user_list')
def user_list():
    '''
    # 1. 获取
    :return:
    '''
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')

    # 2. 校验参数(参数类型转换)
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = 1
        page_size = 10
        current_app.logger.error(e)

    user = User.query.filter(User.is_admin == 0).order_by(User.create_time.desc()).paginate(page_num, page_size, False)

    total = user.pages
    current = user.page
    items = user.items

    user_list = []
    for item in items:
        user_list.append(item.to_dict())

    data = {
        'total': total,
        'current': current,
        'list': user_list
    }

    return jsonify(code=RET.OK, data=data, message='success')

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
    for i in range(0, 7):
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