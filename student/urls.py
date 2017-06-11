from django.conf.urls import url
from .views import stu_home, personal_info_manage, update_password


urlpatterns = [
    url(r'^$', stu_home),
    url(r'^personal_info', personal_info_manage),
    url(r'^update_password', update_password),
]
