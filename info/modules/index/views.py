from flask import session, current_app, jsonify, request
from . import index_blue
from info.models import User, News, Category
from info.utils.response_code import RET

@index_blue.route('/newall')
def newList():
    '''
    1. 获取参数
    2. 参数类型转换
    3. 分页查询
    4. 获取到分页对象中的属性，总页数，当前页的对象列表
    5. 将对象列表转成字典列表
    6. 写到参数返回响应
    :return:
    '''
    # 1.获取参数
    categorys_id = request.args.get('categorys', '1')
    page_num = request.args.get('page_num', '1')
    page_size = request.args.get('page_size', '10')
    if not categorys_id:
        return jsonify(code=RET.NODATA, message='参数不完整')

    # 2.参数类型转换
    try:
        page_num = int(page_num)
        page_size = int(page_size)
    except Exception as e:
        page_num = 1
        page_size = 10

    # 3.分页查询
    try:
        # 查询全部分类中指定id的分类，分组，排序，分页
        filters = ''
        if int(categorys_id) != 1:
            filters = (News.category_id == int(categorys_id))
        paginate = News.query.filter(filters).order_by(News.create_time.desc()).paginate(page_num, page_size, False)  # paginate 分页查询

        # if int(categorys_id) == 1:
        #     paginate = News.query.filter().order_by(News.create_time.desc()).paginate(page_num, page_size, False) # paginate 分页查询
        # else:
        #     paginate = News.query.filter(News.category_id == int(categorys_id)).order_by(News.create_time.desc()).paginate(page_num, page_size, False)  # paginate 分页查询
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询新闻列表异常')

    # 4.获取到分页对象中的属性，总页数，当前页的对象列表
    total = paginate.pages
    current = paginate.pages
    items = paginate.items

    # 5.将对象列表转成字典列表
    news_list = []
    for item in items:
        news_list.append(item.to_dict())
    # 6.写到参数返回响应
    return jsonify(code=RET.OK, total=total, current=current, data={'news_list': news_list}, message='success')


@index_blue.route('/itemize')
def itemize():
    """分类"""
    try:
        categorys = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询错误')

    itemizeList = []
    for item in categorys:
        itemizeList.append(item.to_dict())

    return jsonify(code=RET.OK, data={'itemizeList': itemizeList}, message='success')


@index_blue.route('/hot', methods=['GET'])
def hotNew():
    '''
    热门数据
    :return:
    '''
    # 根据点击量查询热门数据
    try:
        news = News.query.order_by(News.clicks.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询错误')

    news_list = []
    for item in news:
        news_list.append(item.to_dict())


    return jsonify(code=RET.OK, data={'data': news_list}, message='success')

@index_blue.route('/home', methods=['GET'])
def home():
    # 获取用户的登录信息
    user_id = session.get('user_id')

    # 2. t通过user_id取出用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, message='用户信息查询失败')

    # 3. 拼接用户数据
    data = {
        'user_info': user.to_dict() if user else ''
    }
    return jsonify(code=RET.OK, data=data, message='用户信息')
