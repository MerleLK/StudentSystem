import hashlib
from django.shortcuts import render, render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from StudentSystem.customize_messages import flash
from accounts.models import User
from .models import TeacherMessage

# Create your views here.


def tea_home(request):
    return render(request, 'teacher/tea_home.html')


# 教师个人信息的处理
@csrf_exempt
def tea_personal_info(request):
    try:
        username = request.session['username']
    except KeyError:
        return 404

    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            teacher = TeacherMessage.objects.get(id=user.eno_id)
            return render_to_response('teacher/tea_personal_info.html', {'teacher': teacher})
        except ObjectDoesNotExist:
            return render(request, 'teacher/tea_home.html')

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            teacher = TeacherMessage.objects.get(id=user.eno_id)
            teacher.age = request.POST['age']
            teacher.sex = request.POST['sex']
            teacher.college = request.POST['college']

            teacher.save()
            return redirect('/teacher/tea_personal_info')

        except ObjectDoesNotExist:
            flash(request, 'error', u'修改出错！获得没有获得您的信息')
            return render(request, 'teacher/tea_home.html')


# 教师对自己密码的处理
def tea_update_password(request):
    try:
        username = request.session["username"]
        print(username)
    except KeyError:
        return 404

    if request.method == "POST":

        old_password = hash_password(request.POST['old_password'])
        new_password = request.POST['new_password']

        try:
            user = User.objects.get(username=username, password=old_password)
            user.password = hash_password(new_password)
            user.save()
            return redirect('/teacher')
        except ObjectDoesNotExist:
            flash(request, 'error', u'旧密码错误！请重新输入')

    return render(request, 'teacher/tea_update_password.html')


def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
