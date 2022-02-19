from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, models # 导入modules 让程序知道有modules存在
from info.models import User

app = create_app('develop')


# 创建manager对象管理app
manager = Manager(app)

# 使用Migrate 关联app , db
Migrate(app, db)

# 给manager 添加一条操作命令
manager.add_command('db', MigrateCommand)

# 定义方法，创建管理员对象 , 会在 python manager 参数中添加一项选项可以设置用户名密码
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_superuser(username, password):
    # 1. 创建用户对象
    admin = User()

    # 2. 设置用户属性
    admin .nick_name = username
    admin.mobile = username
    admin.password = password
    admin.is_admin = True

    # 3. 保存到数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exceprion as e:
        current_app.logger.error(e)
        return '创建失败'

    return '创建成功'

if __name__ == '__main__':
    manager.run()