import hashlib
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Role
from StudentSystem.customize_messages import flash
from student.models import StudentMessage
from teacher.models import TeacherMessage


# Create your views here.


# 注册登录的首页
def index(request):
    return render(request, 'accounts/index.html')


# 注册的视图
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        emp_no = request.POST['emp_no']
        if User.objects.filter(username=username):
            flash(request, 'error', u'该用户名已被使用！')
            # return HttpResponse('<h1>用户已存在</h1>')
        # 验证学生表和教师表是否有信息
        elif not (StudentMessage.objects.filter(id=emp_no) or TeacherMessage.objects.filter(id=emp_no)):
            flash(request, 'error', u'您无法注册，当前系统没有您的信息.')
        else:
            password = add_password(request.POST['password'])
            email = request.POST['email']
            phone = request.POST['phone']
            role_id = request.POST['role_id']
            user = User.objects.create(
                username=username,
                password=password,
                email=email,
                phone=phone,
                eno_id=emp_no,
                role_id=Role.objects.get(id=role_id),
            )
            flash(request, 'success', u'注册成功！请您登陆')
            return render(request, 'accounts/login.html', locals())

    return render(request, 'accounts/register.html', locals())


# 登录的视图
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = add_password(request.POST['password'])
        # print(password, "登录的密码")
        user_obj = User.objects.filter(username=username, password=password)

        if len(user_obj) == 1:
            user = user_obj[0]
            request.session['username'] = user.username

            if user.role_id.role_name == 'teacher':
                return redirect('/teacher')
            elif user.role_id.role_name == 'student':
                return redirect('/student')
            else:
                return redirect('/accounts')
        else:
            flash(request, 'error', u'用户名不存在或者密码错误')
            return render(request, 'accounts/login.html', locals())
    else:
        return render(request, 'accounts/login.html', locals())


# 注销登录的视图
def logout_view(request):
    del request.session
    return render(request, 'accounts/index.html', locals())


# 添加hash密码
def add_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
