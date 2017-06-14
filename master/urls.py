from django.conf.urls import url
from .views import master_home, master_add_master, master_alter_password, master_teacher_import, master_student_import

urlpatterns = [
    url(r'^$', master_home),
    url(r'^master_add_master', master_add_master),
    url(r'^master_alter_password', master_alter_password),
    url(r'^master_teacher_import', master_teacher_import),
    url(r'^master_student_import', master_student_import),
]
