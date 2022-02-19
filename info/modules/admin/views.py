from . import admin_blue


@admin_blue.route('/login')
def admin_login():
    return 'admin_login'