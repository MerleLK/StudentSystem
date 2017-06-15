import hashlib
import datetime
from accounts.models import Role, User


# 提前运行的脚本文件，用来作为预处理
def run():
    """
    处理相关任务
    :return:
    """
    if pre_role_data():
        print(u'创建角色完毕!')
        if pre_admin_message():
            print(u'加载管理员用户信息成功!')
            print(u'系统初始化完毕!')
        else:
            print(u'加载管理员信息失败!')
    else:
        print(u'创建角色失败!')
        print(u'系统初始化失败!')


# 初始化role表
def pre_role_data():
    names = ['admin', 'teacher', 'student']
    try:
        for i in range(3):
            role = Role(
                id=i,
                role_name=names[i]
            )
            role.save()
        return True
    except Exception as e:
        print(e)
        return False


# 初始化一个admin账户 与超级管理员后台一致
def pre_admin_message():
    try:
        user = User(
            username='admin',
            password=hash_password('admin123456'),
            email='Merle.liukun@gmail.com',
            datetime=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            phone='18838032337',
            image='',
            eno_id=1,
            role_id_id=0
        )
        user.save()
        return True
    except Exception as e:
        print(e)
        return False


# 添加hash密码
def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
