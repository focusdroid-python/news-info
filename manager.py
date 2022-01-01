from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, models # 导入modules 让程序知道有modules存在

app = create_app('develop')


# 创建manager对象管理app
manager = Manager(app)

# 使用Migrate 关联app , db
Migrate(app, db)

# 给manager 添加一条操作命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()