from flask import request, jsonify, current_app, abort
from info.models import News
from info.utils.response_code import RET
from . import new_blue
import json
from info import db

@new_blue.route('/addNew', methods=['POST'])
def add_news():
    '''添加新闻接口'''
    json_data = request.data
    dict_json = json.loads(json_data)
    title = dict_json.get('title')
    content = dict_json.get('content')
    source = dict_json.get('source')
    digest = dict_json.get('digest')
    print(title, content)

    news = News()
    news.title = title
    news.source = source
    news.digest = digest
    news.content = content

    try:
        db.session.add(news)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='插入失败')

    return jsonify(code=RET.OK, data=True, message='success')

@new_blue.route('/newList')
def new_list():
    news_id = request.args.get('id')
    print(news_id)
    # 1. 根据新闻编号查询新闻对象
    try:
        news = News.query.get(int(news_id))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询失败')

    if not news:
        abort(404)

    # 2. 写到数据渲染页面
    return jsonify(code=RET.DBERR, data = {'news_info': news.to_dict() if news else {}},  message='success')