from django.conf.urls import url
from .views import stu_home, personal_info_manage, update_password
from .views import get_all_course, stu_find_course_by_name, get_all_chose_course, stu_chose_new_course
from .views import stu_do_chose, stu_del_course


urlpatterns = [
    url(r'^$', stu_home),
    url(r'^personal_info', personal_info_manage),
    url(r'^update_password', update_password),
    url(r'^get_all_course', get_all_course),
    url(r'^stu_find_course_by_name', stu_find_course_by_name),
    url(r'get_all_chose_course', get_all_chose_course),
    url(r'^stu_chose_new_course', stu_chose_new_course),
    url(r'^stu_do_chose/(.+)', stu_do_chose),
    url(r'^stu_del_course/(.+)', stu_del_course)
]
