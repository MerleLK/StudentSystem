import hashlib
import xlrd
import os
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from StudentSystem.settings import MEDIA_ROOT
from accounts.models import User, Role
from StudentSystem.customize_messages import flash
from teacher.models import TeacherMessage
from student.models import StudentMessage

# Create your views here.


# 进入管理员首页
def master_home(request):
    return render(request, 'master/master_home.html')


# 管理员添加管理员
def master_add_master(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone']

            if User.objects.filter(username=username):
                flash(request, 'error', u'该用户名已被使用！')
            else:
                user = User(
                    username=username,
                    password=password,
                    email=email,
                    phone=phone,
                    eno_id=1,
                    role_id=Role.objects.get(id=0),
                )
                user.save()
                flash(request, 'success', u'增加管理员成功!')
        except KeyError:
            flash(request, 'error', u'请求的数据有误')
        except ObjectDoesNotExist:
            flash(request, 'error', u'数据库查询错误！')
    return render(request, 'master/master_add_master.html')


# 管理员修改密码
def master_alter_password(request):
    try:
        username = request.session["username"]
    except KeyError:
        return 404

    if request.method == "POST":
        try:
            old_password = hash_password(request.POST['old_password'])
            new_password = request.POST['new_password']
        except KeyError:
            flash(request, 'error', u'请您输入相关信息')
            return render(request, 'master/master_update_password.html')

        try:
            user = User.objects.get(username=username, password=old_password)
            user.password = hash_password(new_password)
            user.save()
            flash(request, 'success', u'密码修改成功')
            return render(request, 'master/master_home.html')
        except ObjectDoesNotExist:
            flash(request, 'error', u'旧密码错误！请重新输入')

    return render(request, 'master/master_update_password.html')


# 管理员导入教师信息
def master_teacher_import(request):

    if request.method == "POST":
        my_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(my_file.name, my_file)
        file_url = MEDIA_ROOT + "\\" + filename
        if teacher_file_import(file_url):
            flash(request, 'success', u'教师信息导入成功！')
        else:
            flash(request, 'error', u'教师信息导入失败！请重新导入')
        os.remove(file_url)
    return render(request, 'master/master_teacher_import.html')


# 管理员导入学生信息
def master_student_import(request):
    if request.method == "POST":
        my_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(my_file.name, my_file)
        file_url = MEDIA_ROOT + "\\" + filename
        if student_file_import(file_url):
            flash(request, 'success', u'学生信息导入成功！')
        else:
            flash(request, 'error', u'学生信息导入失败！请重新导入')
        os.remove(file_url)
    return render(request, 'master/master_student_import.html')


# 添加hash密码
def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed


# 教师信息文件处理
def teacher_file_import(filename):
    my_file = xlrd.open_workbook(filename)
    sheet = my_file.sheet_by_index(0)
    try:
        for row in range(sheet.nrows):
            if row != 0:
                tea_id, name, age, sex, college = sheet.row_values(row)
                teacher = TeacherMessage(
                    id=int(tea_id),
                    name=name,
                    age=int(age),
                    sex=sex,
                    college=college
                )
                teacher.save()
            else:
                pass
        return True
    except:
        return False


# 学生信息文件处理
def student_file_import(filename):
    my_file = xlrd.open_workbook(filename)
    sheet = my_file.sheet_by_index(0)
    try:
        for row in range(sheet.nrows):
            if row != 0:
                stu_id, name, age, sex, grade, discipline, class_code = sheet.row_values(row)
                student = StudentMessage(
                    id=int(stu_id),
                    name=name,
                    age=int(age),
                    sex=sex,
                    grade=str(int(grade)),
                    discipline=discipline,
                    class_code=str(int(class_code))
                )
                student.save()
            else:
                pass
        return True
    except:
        return False
