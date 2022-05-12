from django.contrib import admin
from .models import *
# Register your models here.

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['className','classSection','classCode','studentCount','teacherCount']

class classTeachersAdmin(admin.ModelAdmin):
    list_display = ['id','classroom','teacher']

class classStudentAdmin(admin.ModelAdmin):
    list_display = ['id','classroom','student']

# class classTeachersAdmin(admin.ModelAdmin):
#     list_display = ['id','classroom','teacher']


admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(classStudents,classStudentAdmin)
admin.site.register(classTeachers,classTeachersAdmin)
admin.site.register(classStream)
admin.site.register(streamComment)
admin.site.register(Assignment)
admin.site.register(StudentWork)