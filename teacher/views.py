import hashlib
from django.shortcuts import render, render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from StudentSystem.customize_messages import flash
from accounts.models import User
from .models import TeacherMessage, CourseInfo
from student.models import Elective

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


# 教师添加课程
def tea_add_course(request):
    try:
        username = request.session['username']
    except KeyError:
        return 404

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            teacher_id = user.eno_id
            course_name = request.POST['course_name']
            description = request.POST['description']
            for_grade = request.POST['for_grade']

            last_course = CourseInfo.objects.last()
            if not last_course:
                new_course_id = 50000000
            else:
                new_course_id = last_course.course_id + 1

            course = CourseInfo.objects.create(
                course_id=new_course_id,
                teacher_id_id=teacher_id,
                course_name=course_name,
                description=description,
                for_grade=for_grade,
            )
            course.save()
            flash(request, 'success', u'创建新课程成功')
            return render(request, 'teacher/tea_add_course.html')
        except ObjectDoesNotExist:
            return 404
        except KeyError:
            return 404
    else:
        return render(request, 'teacher/tea_add_course.html')


# 教师查询课程
def tea_find_course(request):
    try:
        username = request.session['username']
    except KeyError:
        return 404

    if request.method == "GET":
        user = User.objects.get(username=username)
        teacher_id = user.eno_id
        courses = CourseInfo.objects.filter(teacher_id=teacher_id).order_by('course_id')

        return render_to_response('teacher/tea_show_all_course.html', {'courses': courses})


# 教师删除课程
def tea_del_course(request, course_id):
    """

    :param request: 请求
    :param course_id: 课程号
    :return: 渲染后界面
    先把对应的数据得到，判断是否存在被选中，有就提示无法删除课程，否则就删除。  注意页面点击的时候使用js进行点击确认。
    """
    try:
        course = CourseInfo.objects.get(course_id=course_id)
        elective = Elective.objects.filter(course_id=course_id)
        if elective:
            flash(request, 'error', u'存在学生选择该课程，无法删除！')
            return render(request, 'teacher/tea_home.html')
        else:
            course.delete()
    except ObjectDoesNotExist:
        flash(request, 'error', u'没有检索到信息！')
        return render(request, 'teacher/tea_home.html')
    return redirect('/teacher/tea_find_course')


# 教师修改课程
def tea_alter_course(request, course_id):

    """
    :param request: 请求
    :param course_id: 课程编号
    :return:
    """
    if request.method == "POST":
        try:
            course_id = request.POST['course_id']
            course = CourseInfo.objects.get(course_id=course_id)
            if course:
                course_name = request.POST['course_name']
                description = request.POST['description']
                for_grade = request.POST['for_grade']

                course.course_name = course_name
                course.description = description
                course.for_grade = for_grade
                course.save()

                flash(request, 'success', u'修课程改信息成功')
                return render(request, 'teacher/tea_alter_course.html', {'course': course})
        except ObjectDoesNotExist:
            return 404
    elif request.method == "GET":
        try:
            course = CourseInfo.objects.get(course_id=course_id)
            return render(request, 'teacher/tea_alter_course.html', {'course': course})
        except ObjectDoesNotExist:
            return 404
    return


# 教师通过名称查询到课程
def tea_find_course_by_name(request):
    pass


def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
