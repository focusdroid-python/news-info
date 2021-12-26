from info import redis_store
from . import index_blue


@index_blue.route('/', methods=['POST', 'GET'])
def hello_world():
    # 测试redis村数据
    redis_store.set("name", "focusdroid")
    print(redis_store.get("name"))
    #
    # # 测试session存储
    # session['age'] = 30
    # session['address'] = 'shanghai'

    return 'hello'