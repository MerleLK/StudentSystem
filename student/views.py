from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
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
        print(username)
    except KeyError:
        return 404
    user = User.objects.get(username=username)

    if request.method == 'GET':
        student = StudentMessage.objects.get(id=user.eno_id)
        return render_to_response('student/show_person_info.html', {'student': student})

    elif request.method == 'POST':
        student = StudentMessage.objects.get(id=user.eno_id)
        student.age = request.POST['age']
        student.sex = request.POST['sex']
        student.grade = request.POST['grade']
        student.discipline = request.POST['discipline']
        student.class_code = request.POST['class_code']

        student.save()
        return render(request, 'student/stu_home.html')

    else:
        flash(request, 'error', "出错了")
        return render(request, 'student/stu_home.html')

