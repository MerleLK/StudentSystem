from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User
import hashlib

# Create your views here.


# 注册登录的首页
def index(request):
    return render(request, 'accounts/index.html')


# 注册的视图
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            return HttpResponse('<h1>用户已存在</h1>')
        else:
            password = add_password(request.POST['password'])
            email = request.POST['email']
            phone = request.POST['phone']
            user = User.objects.create(
                username=username,
                password=password,
                email=email,
                phone=phone
            )

            request.session["username"] = user.username
            return redirect('/')

    return render(request, 'accounts/register.html', locals())


# 登录的视图
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = add_password(request.POST['password'])
        user_obj = User.objects.filter(username=username, password=password)

        if len(user_obj) == 1:
            user = user_obj[0]
            request.session['username'] = user.username
            return redirect('/accounts')
        else:
            return HttpResponse('<h1>用户名不存在，或者密码错误！</h1>')
    else:
        return render(request, 'accounts/login.html', locals())

    # return render(request, 'accounts/index.html', locals())


# 注销登录的视图
def logout_view(request):
    del request.session
    return render(request, 'accounts/index.html', locals())


# 添加hash密码
def add_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
