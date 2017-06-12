# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('course_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('for_grade', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherMessage',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(default='MAN', max_length=10)),
                ('college', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='courseinfo',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_teacher', to='teacher.TeacherMessage'),
        ),
    ]
