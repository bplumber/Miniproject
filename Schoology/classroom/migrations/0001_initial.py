# Generated by Django 4.0.2 on 2022-04-10 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=100, verbose_name='Name')),
                ('classSection', models.CharField(max_length=20, verbose_name='Section')),
                ('classDescription', models.TextField(verbose_name='Description')),
                ('classCode', models.CharField(max_length=6, unique=True)),
                ('lecturesConducted', models.IntegerField(default=0, verbose_name='No. of Lectures conducted')),
                ('assignmentsPosted', models.IntegerField(default=0, verbose_name='No. of Assignments Posted')),
                ('studentCount', models.IntegerField(default=0, verbose_name='Number Of Students')),
                ('teacherCount', models.IntegerField(default=1, verbose_name='No of Teachers')),
            ],
        ),
        migrations.CreateModel(
            name='classStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='streamComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classstream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='classTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teacher')),
            ],
            options={
                'unique_together': {('classroom', 'teacher')},
            },
        ),
        migrations.CreateModel(
            name='classStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classesAttended', models.IntegerField(default=0)),
                ('assignmentSubmitted', models.IntegerField(default=0, verbose_name='No. Of Assignment Submitted')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
            ],
            options={
                'unique_together': {('classroom', 'student')},
            },
        ),
    ]