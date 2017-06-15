import hashlib
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User
from student.models import StudentMessage, Elective
from StudentSystem.customize_messages import flash
from teacher.models import CourseInfo

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


# 学生更新密码
@csrf_exempt
def update_password(request):
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
            return redirect('/student/update_password')

        try:
            user = User.objects.get(username=username, password=old_password)
            user.password = hash_password(new_password)
            user.save()
            return redirect('/student')
        except ObjectDoesNotExist:
            flash(request, 'error', u'旧密码错误！请重新输入')

    return render(request, 'student/update_password.html')


# 学生查询所有的课程成绩
def get_all_course(request):

    if request.method == "GET":
        try:
            username = request.session["username"]
        except KeyError:
            return 404

        try:
            user = User.objects.get(username=username)
            stu_id = user.eno_id
            electives = Elective.objects.filter(student_id=stu_id)
            if electives:
                return render(request, 'student/stu_show_grade.html', {"electives": electives})
            else:
                flash(request, 'error', u'没有查询到信息')
        except ObjectDoesNotExist:
            flash(request, 'error', u'没有查询到信息')

    return render(request, 'student/stu_show_grade.html')


# 学生通过课程名查询该课程的成绩
def stu_find_course_by_name(request):

    if request.method == "POST":
        try:
            course_name = request.POST['course_name']
            course_id = CourseInfo.objects.get(course_name=course_name)

            try:
                elective = Elective.objects.get(course_id_id=course_id)
                return render(request, 'student/stu_show_single_grade.html', {'elective': elective})
            except ObjectDoesNotExist:
                flash(request, 'error', u'您没有选择该课程！')
        except KeyError:
            pass
        except ObjectDoesNotExist:
            flash(request, 'error', u'您输入的课程名不存在！')
    return render(request, 'student/stu_find_course_by_name.html')


# 学生展示自己选的课程  跟查询成绩类似了
def get_all_chose_course(request):

    if request.method == "GET":
        try:
            username = request.session["username"]
        except KeyError:
            return 404

        try:
            user = User.objects.get(username=username)
            stu_id = user.eno_id
            electives = Elective.objects.filter(student_id=stu_id)
            if electives:
                return render(request, 'student/stu_show_course.html', {"electives": electives})
            else:
                flash(request, 'error', u'没有查询到信息')
        except ObjectDoesNotExist:
            flash(request, 'error', u'没有查询到信息')

    return render(request, 'student/stu_home.html')


# 学生选择新课程
def stu_chose_new_course(request):

    try:
        courses = CourseInfo.objects.all()
        if courses:
            return render(request, 'student/stu_show_pub_courses.html', {'courses': courses})
        else:
            flash(request, 'error', u'教师还没有发布课程信息！')
    except ObjectDoesNotExist:
        flash(request, 'error', u'没有该课程')
        pass
    return render(request, 'student/stu_home.html')


# 学生进行选择
def stu_do_chose(request, course_id):
    """
    通过超链接进行选课的操作
    :param request:
    :param course_id:  被选课程的ID
    :return:
    """
    if request.method == "GET":
        try:
            username = request.session["username"]
        except KeyError:
            return 404

        try:
            user = User.objects.get(username=username)
            stu_id = user.eno_id
            elective = Elective.objects.filter(student_id_id=stu_id, course_id_id=course_id)
            if elective:
                flash(request, 'error', u'您已经选择该课程！')
            else:
                my_elective = Elective.objects.create(
                    course_id_id=course_id,
                    student_id_id=stu_id,
                    score=60
                )
                my_elective.save()
                flash(request, 'success', u'您已经选课成功！')
        except ObjectDoesNotExist:
            pass
    return render(request, 'student/stu_home.html')


# 学生推选课程
def stu_del_course(request, course_id):
    """
    学生退选课程
    :param request:
    :param course_id: 课程ID
    :return:
    """
    try:
        username = request.session["username"]
    except KeyError:
        return 404

    try:
        user = User.objects.get(username=username)
        stu_id = user.eno_id

        elective = Elective.objects.get(student_id_id=stu_id, course_id_id=course_id)
        elective.delete()
        flash(request, 'success', u'退选课程成功！')
    except ObjectDoesNotExist:
        flash(request, 'error', u'退选课程失败！')

    return render(request, 'student/stu_home.html')


# 添加hash密码
def hash_password(password):
    password_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hashed
