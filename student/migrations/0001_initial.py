# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_elective', to='teacher.CourseInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMessage',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(default='MAN', max_length=10)),
                ('grade', models.CharField(max_length=10)),
                ('discipline', models.CharField(max_length=30)),
                ('class_code', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='elective',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elective_student', to='student.StudentMessage'),
        ),
    ]