# news-info
flask新闻项目

### flask生成数据库迁移表
```
python manager.py db init
python manager.py db migrate -m 'initial'
python manager.py db upgrade

出现上面错误的原因是，flask-migrate找不到“a1c25fe0fc0e”标识的修订版，我们只要在命令中注明所提示丢失的标识号就行!
我们在shell命令行窗口可以依次使用如下命令：

python app.py db revision --rev-id <将提示的标识号填进这个位置，如上面的a1c25fe0fc0e>
python app.py db migrate
python app.py db upgrade

pip install 包名 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
pip install mysqlclient -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```



### 4. 短信验证码

 - 目的：完善短信接口的编写
 - 操作步骤
 - 1. 获取参数
   2. 参数为空校验
   3. 检验手机格式
   4. 通过图片验证码比那好获取，图片验证码
   5. 判断图片验证码是否过期
   6. 判断图片验证码是否正确
   7. 杉树redis中图片验证码
   8. 生成一个短信验证码，存入redis


### 5. 注册用户
 - 目的：创建一个用户对象，保存在数据库
 - 操作步骤：
   - 1. 获取参数
   - 2. 校验参数不能为空
   - 3. 手机号作为key，取出redis中的短信验证码
   - 4. 判断短信验证码是否过期
   - 5. 判断短信验证码是否正确
   - 6. 删除短信验证码
   - 7. 创建用户对象
   - 8. 设置用户对象属性
   - 9. 保存用户到数据库
   - 10. 返回响应

### 7. 注册用户加密

 - 目的： 使用falsk中提供的安全模块，将密码进行加密
 - 注意点：
   - @property装饰方法可以被属性使用
   - @属性.setter，给方法增加一个设置方式
   - generator_password_hash()系统提供的加密方法
   - check_password_hash()系统提供密码校验方法

### 8. 登陆接口
 - 目的： 完成登陆接口，提供给前端工程师
 - 操作流程
   1. 获取参数
   2. 检验参数
   3. 通过手机号到数据库查询用户对象
   4. 确认用户是否存在
   5. 校验密码是否正确
   6. 讲用户登录信息保存在session中
   7. 返回响应
### 9. 首页右上角用户显示
  - 目的：显示用户登录之后的信息
    1. 登陆用户，将信息存到redis中g
    2. 当我们刷新首页的时候到session中取user_id得知
    3. 然后将用户的自带呢数据，接口发送给你给前端
### 10. 退出用户
  - 目的，用户退出功能
    1. 清除session信息
    2. 返回响应
### 11. 用户最后登录时间

    
### 12. 自动提交
 - 目的：使用sqlalchemy属性配置让那个数据库能自动提交
 - 操作流程
   1. 在config配置文件中，设置sqlalchemy_commit_onteardown = True
   2. 设置好了之后数据库的内容改变之后，视图函数在结束的时候就会自动提交
### 13. CSRFProject校验开启
 - 目的：在前端方中携带csrf_token以便csrf校验能够通过
   1. 校验过程：
      1. 如果是非表单提交
      2. 在请求头中设置csrf_token
      3. 服务器：取出二者进行校验
   2. 表单提交
      1. 在表单设置一个隐藏字段即可
### 14. 热门新闻排行
### 15. 分类数据展示
 - 目的：在首页头部战术分类信息
 - 操作流程
   1. 在跟路径中查询所有的分类依据
   2. 讲分类数据装成字典列表
   3. 写到分类数据渲染页面
### 16. 首页新闻列表战士
  - 目的： 编写新闻战士战士列表获取新闻数据，展示在首页中
  - 操作步骤
    1. 获取参数
    2. 参数类型转换
    3. 分页查询
    4. 获取到分页对象中的属性，总页数，当前页的对象列表
    5. 将对象列表转成字典列表
    6. 写到参数返回响应
### 17. 新闻列表更多加载调试
### 18. 分页切换调试
### 19. 新闻详情页展示

#### 新闻收藏功能接口
    - 请求路径 /news/news_collect
    - 请求方式 POST
    - 请求参数： news_id, action, g.user
    - 返回值 error, errmsg
    | ------- | --------|
    参数名     类型      是否必须    参数说明
    news_id   int       是         新闻编号
    action    string    是         收藏或者取消收藏  collect   cancel_collect

#### 新闻评论后端接口
    # 1. 判断用户是否登录
    # 2. 获取参数
    # 3. 校验参数为空校验
    # 4. 根据新闻编号取出来对象，判断新闻是否存在
    # 5. 创建评论对象
    # 6. 保存评论对象到数据库中 
    # 7. 返回响应
    # 5. 
    - 请求路径 /news/news_comment
    - 请求方式 POST
    - 请求参数 news_id  comment   parent_id   g.user
    - 返回值 errno message
    | -------- | -------- |
    news_id   int    是     新闻编号
    comment   string 是     评论内容
    parent_id int    是     回复评论的id

#### 评论点赞
    # 1. 判断用户是否登录
    # 2. 获取参数 
    # 3. 校验参数
    # 4. 操作类型进行校验
    # 5. 通过评论编号查询品论对象，并存在是否存在
    # 6. 根据操作类型点赞取消
    # 7. 返回响应
    # 3.
    # 1. 请求路径 /news/comment_like
    # 2. 请求方式： POST
    # 3. 请求参数： news_id comment_id  action, g.user
    # 4. 参数解释
    | -----------  |  --------------- |
    参数名             类型          是否必须        参数说明
    news_id             string       是              新闻编号
    comment_id          int           True          评论编号
    action              string         True         点赞操作类型，add  remove

### 用户信息修改和展示
    # 1. 判断请求方式，如果是get请求，返回用户数据，如果是post就是提交数据
    # 2. 写到用户数据，渲染页面
    # 3. 如果是post请求
    # 4. 获取参数
    # 5. 校验参数
    # 6. 修改用户数据
    # 7. 返回响应
    # 1. 


### 修改密码
    # 1. post请求，获取参数
    # 2. 校验参数
    # 3. 旧密码是否正确
    # 4. 设置新密码
    # 5. 返回响应
    # 1. 请求路径 /user/password
    # 2. 请求方式： POST
    # 3. 请求参数： current_password new_password
    # 4. 参数解释
    | -----------  |  --------------- |
    参数名             类型          是否必须        参数说明
    current_password   string       是              旧密码
    new_password       string           True        新密码


### 新闻收藏列表
    # 1. get请求，获取参数
    # 2. 校验参数(参数类型转换)
    # 3. 分液参训收藏新闻
    # 4. 获取分页对象属性，总页数，当前页， 当前页对象列表
    # 5. 返回响应
    # 1. 请求路径 /user/collection
    # 2. 请求方式： GET
    # 3. 请求参数： user_id page_num page_size
    # 4. 参数解释
    | -----------  |  --------------- |
    参数名             类型          是否必须        参数说明
    user_id   string       是              旧密码
    page_num       string           True        新密码
    page_size       string           True        新密码


### 用户关注列表
 - 实现思路
   1. 获取参数
   - 2.参数类型扎古换
   - 分页查询用互关注列表的人
   - 取出分页对象的数据，总页数，当前页对象
   - 将对象列表转成对象
   - 

### 获取用户列表
   - 请求路径 /admin/user_list
   - 请求方式 get
   - 请求参数 page_num page_size
   - 返回数据


### 获取/设置新闻审核
   - 请求路径 /admin/user_review
   - 请求方式 get
   - 请求参数 status 0 未审核 1 审核通过 2：正在审核 3 下架
     - page_num page_size
   - 返回数据

### 新闻分类管理 
  - 请求路径  /admin/news_category
  - 请求方式 get
  - 请求参数
  - 返回数据






























