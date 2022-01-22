from flask import request, jsonify, current_app, abort, g
from info.models import News, Comment, CommentLike
from info.utils.response_code import RET
from . import new_blue
import json
from info import db
from info.utils.common import user_login_data


@new_blue.route('/comment_like', methods=['POST'])
@user_login_data
def comment_like():
    '''
    /comment_like
        # 1. 判断用户是否登录
    # 2. 获取参数
    # 3. 校验参数
    # 4. 操作类型进行校验
    # 5. 通过评论编号查询品论对象，并存在是否存在
    # 6. 根据操作类型点赞取消
    # 7. 返回响应
    :return:
    '''
    # 1. 判断用户是否登录
    if not g.user:
        return jsonify(error=RET.NODATA, message='用户未登录')
    # 2. 获取参数
    # news_id = request.json.get('news_id')
    user_id = request.json.get('user_id')
    comment_id = request.json.get('comment_id')
    action = request.json.get('action')
    # 3. 校验参数
    if not all([comment_id, action]):
        return jsonify(error=RET.NODATA, message='参数不全')
    # 4. 操作类型进行校验
    if not action in ['add', 'remove']:
        return jsonify(error=RET.NODATA, message='操作类型有误')
    # 5. 通过评论编号查询品论对象，并存在是否存在

    try:
        comment = Comment.query.get(comment_id)
        # news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, message='查询失败')

    if not comment:
        return jsonify(error=RET.NODATA, message='该新闻或点赞不存在')
    # 6. 根据操作类型点赞取消
    if action == 'add':
        # 判断用户是否对该评论点过赞，
        print(g.user)
        print(g.user.id)
        # comment_like = Comment.query.filter(CommentLike.user_id == g.user.id, CommentLike.comment_id == comment_id).first()
        # comment_like = Comment.query.filter(CommentLike.user_id == user_id, CommentLike.comment_id == comment_id).first()
        comment_like = Comment.query.filter(CommentLike.user_id == user_id, CommentLike.comment_id == comment_id).first()
        print(comment_like)
        if not comment_like:
            # 创建点赞对象
            comment_like = CommentLike()
            comment_like.user_id = g.user.id
            comment_like.comment_id = comment_id

            comment.like_count += 1
            db.session.add(comment_like)
            # 讲该评论的点赞数量+1
            db.session.commit()
    else:
        comment_like = Comment.query.filter(CommentLike.user_id == g.user_id, CommentLike.comment_id == comment_id).first()
        if comment_like:
            # 创建点赞对象
            db.session.delete(comment_like)
            # 讲该评论的点赞数量+1
            if comment.like_count > 0:
                comment.like_count += 1
            db.session.commit()
    # 7. 返回响应
    return jsonify(errno=RET.OK, data=comment_like, message='success')


@new_blue.route('/news_comment', methods=['POST'])
@user_login_data
def news_comment():
    '''评论部分
    # 1. 判断用户是否登录
    # 2. 获取参数
    # 3. 校验参数为空校验
    # 4. 根据新闻编号取出来对象，判断新闻是否存在
    # 5. 创建评论对象
    # 6. 保存评论对象到数据库中
    # 7. 返回响应
    '''
    # 1. 判断用户是否登录
    if not g.user:
        return jsonify(error=RET.NODATA, message='用户未登录')

    # 2. 获取参数
    user_id = request.json.get('user_id')
    news_id = request.json.get('news_id')
    content = request.json.get('content')
    parent_id = request.json.get('comment')

    # 3. 校验参数为空校验
    if not all([news_id, content]):
        return jsonify(error=RET.PARAMERR, message='参数不全')

    # 4. 根据新闻编号取出来对象，判断新闻是否存在
    try:
        new = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, message='数据库查询错误')
    if not new: return jsonify(error=RET.NODATA, message='为查询该条新闻详情')

    # 5. 创建评论对象
    comment = Comment()
    comment.user_id = user_id
    comment.news_id = news_id
    comment.content = content
    if comment.parent_id: comment.parent_id = parent_id
    # 6. 保存评论对象到数据库中
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, message='【评论失败')
    # 7. 返回响应
    return jsonify(error=RET.OK, data=comment.to_dict(), message='评论成功')


@new_blue.route('/news_collect', methods=['POST'])
@user_login_data
def new_collect():
    '''点击收藏'''
    # 1. 判断用户身份是否登陆
    # 2. 获取参数
    # 3. 参数校验，为空校验
    # 4. 操作类型校验
    # 5. 判断新闻对象是否存在
    # 6. 根据类型操作，进行收藏操作
    # 7. 返回响应

    # 1. 判断用户身份是否登陆
    if not g.user:
        return jsonify(error=RET.NODATA, message='用户未登录')
    # 2. 获取参数
    news_id = request.json.get('news_id')
    action = request.json.get('action')


    # 3. 参数校验，为空校验
    if not all([news_id, action]):
        return jsonify(error=RET.PARAMERR, message='参数不完整')

    # 4. 操作类型校验
    if action not in ['collected', 'cancel_collect']:
        return jsonify(error=RET.NODATA, message='action状态错误')
    # 5. 判断新闻对象是否存在
    try:
        new = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, message='数据库查询错误')
    if not new:
        return jsonify(error=RET.NODATA, message='为查询该条新闻详情')
    # 6. 根据类型操作，进行收藏操作
    if action == 'collected':
        # 判断该用户是否收藏
        if not new in g.user.collection_news:
            g.user.collection_news.append(new)
            # return jsonify(errno=RET.OK, message='收藏成功')
    else:
        if new in g.user.collection_news:
            g.user.collection_news.remove(new)
            # return jsonify(errno=RET.OK, message='取消收藏成功')
    # 7. 返回响应
    return jsonify(errno=RET.OK, message='收藏成功')

@new_blue.route('/addNew', methods=['POST'])
@user_login_data
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

@new_blue.route('/newDetail')
@user_login_data
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

    # 判读用户是否收藏过该新闻
    is_collected = False
    if g.user:
        if news in g.user.collection_news:
            is_collected = True

    # 获取新闻的评论
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='查询失败')

    # 讲评论的对象列表转成字典
    comment_list = []
    for comment in comments:
        comment_list.append(comment.to_dict())


    data = {
        'news_info': news.to_dict() if news else {},
        'user_info': g.user.to_dict() if g.user else '',
        'is_collected': is_collected,
        'comment': comment_list
    }

    # 2. 写到数据渲染页面
    return jsonify(code=RET.OK, data = data,  message='success')