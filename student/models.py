from django.db import models
from teacher.models import CourseInfo
# Create your models here.


# 学生信息表
class StudentMessage(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, default='MAN')

    grade = models.CharField(max_length=10)
    discipline = models.CharField(max_length=30)
    class_code = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Elective(models.Model):

    course_id = models.ForeignKey(CourseInfo, related_name="course_elective")
    student_id = models.ForeignKey(StudentMessage, related_name="elective_student")
    score = models.FloatField()
