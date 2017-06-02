from django.contrib import admin
from .models import User

# Register your models here.


# 将用户的model注册到admin上
admin.site.register(User)
