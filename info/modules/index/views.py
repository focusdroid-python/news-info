from flask import session, current_app, jsonify
from . import index_blue
from info.models import User, News
from info.utils.response_code import RET


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
