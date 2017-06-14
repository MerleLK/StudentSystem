from django.contrib import admin
from .models import TeacherMessage, CourseInfo

# Register your models here.
admin.site.register(TeacherMessage)
admin.site.register(CourseInfo)
