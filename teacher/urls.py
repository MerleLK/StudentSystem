from django.conf.urls import url
from .views import tea_home, tea_personal_info, tea_update_password, tea_add_course, tea_find_course, tea_del_course
from .views import tea_alter_course


urlpatterns = [
    url(r'^$', tea_home),
    url(r'^tea_personal_info', tea_personal_info),
    url(r'^tea_update_password', tea_update_password),
    url(r'^tea_add_course', tea_add_course),
    url(r'^tea_find_course', tea_find_course),
    url(r'^tea_del_course/(.+)/$', tea_del_course),
    url(r'^tea_alter_course/(.+)/$', tea_alter_course),
    url(r'^tea_alter_course/(.+)', tea_alter_course),
]
