from django.contrib import admin
from .models import *
# Register your models here.

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['className','classSection','classCode','studentCount','teacherCount']

admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(classStudents)
admin.site.register(classTeachers)
admin.site.register(classStream)
admin.site.register(streamComment)