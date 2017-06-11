from django.conf.urls import url
from .views import stu_home, personal_info_manage


urlpatterns = [
    url(r'^$', stu_home),
    url(r'^personal_info', personal_info_manage),
]
