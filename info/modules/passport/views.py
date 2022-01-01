from info import constants

from flask import make_response, request, current_app
from info import redis_store
from . import passport_blue
from utils.captcha.captcha import captcha

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
