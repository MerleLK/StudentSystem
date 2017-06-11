from django.conf.urls import url
from .views import tea_home, tea_personal_info, tea_update_password


urlpatterns = [
    url(r'^$', tea_home),
    url(r'^tea_personal_info', tea_personal_info),
    url(r'^tea_update_password', tea_update_password),
]
