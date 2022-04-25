from django.contrib import admin
from .models import Links, Student,Teacher, User
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','user','phone']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name','user','phone']

admin.site.register(User)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Links)