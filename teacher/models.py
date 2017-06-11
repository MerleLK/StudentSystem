from django.db import models
from django_enumfield import enum

# Create your models here.


# 教师信息表
class TeacherMessage(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, default='MAN')

    college = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 教师发布课程表
class CourseInfo(models.Model):

    course_id = models.BigIntegerField()
    teacher_id = models.ForeignKey(TeacherMessage, related_name="course_teacher")
