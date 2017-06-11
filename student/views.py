import hashlib
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User
from student.models import StudentMessage
from StudentSystem.customize_messages import flash

# Create your views here.


# 学生登录后的首页
def stu_home(request):
    return render(request, 'student/stu_home.html')


# 个人资料管理
@csrf_exempt
def personal_info_manage(request):

    try:
        username = request.session["username"]
    except KeyError:
        return 404

    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            student = StudentMessage.objects.get(id=user.eno_id)
            return render_to_response('student/show_person_info.html', {'student': student})
        except ObjectDoesNotExist:
            flash(request, 'error', u'没有查询到您的信息')
            return render(request, 'student/stu_home.html')

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            student = StudentMessage.objects.get(id=user.eno_id)
            student.age = request.POST['age']
            student.sex = request.POST['sex']
            student.grade = request.POST['grade']
            student.discipline = request.POST['discipline']
            student.class_code = request.POST['class_code']

            student.save()
            return redirect('/student/personal_info_manage')
        except ObjectDoesNotExist:
            flash(request, 'error', u'修改出错！获得没有获得您的信息')
            return render(request, 'student/show_person_info.html')
    else:
        flash(request, 'error', "出错了")
        return render(request, 'student/stu_home.html')


@csrf_exempt
def update_password(request):
    try:
        username = request.session["username"]
        print(username)
    except KeyError:
        return 404

    if request.method == "POST":
        try:
            old_password = hash_password(request.POST['old_password'])
            new_password = request.POST['new_password']
        except KeyError:
            flash(request, 'error', u'请您输入相关信息')
            return redirect('/student/update_password')

        try:
            user = User.objects.get(username=username, password=old_password)
            user.password = hash_password(new_password)
            user.save()
            return redirect('/student')
        except ObjectDoesNotExist:
            flash(request, 'error', u'旧密码错误！请重新输入')

    return render(request, 'student/update_password.html')


# 添加hash密码
def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
