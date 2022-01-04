from flask import request, jsonify, current_app, abort
from info.models import News
from info.utils.response_code import RET
from . import new_blue


@new_blue.route('/newList')
def new_list():
    news_id = request.args.get('id')
    # 1. 根据新闻编号查询新闻对象

    try:
        news = News.query.get(int(news_id))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询失败')

    if not news:
        abort(404)

    # 2. 写到数据渲染页面
    return jsonify(code=RET.DBERR, data = {'news_info': news.to_dict() if news else {}},  message='查询失败')