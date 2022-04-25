from django.db import models
from  user.models import Student, Teacher, User
from datetime import datetime
import random,string
# Create your models here.

class Classroom(models.Model):
    className = models.CharField(verbose_name = 'Name',max_length=100,null=False,blank = False,unique=True)
    classSection = models.CharField(verbose_name='Section', max_length=20,null = False,blank = False)
    classDescription = models.TextField(verbose_name='Description')
    classCode = models.CharField(unique=True,max_length=6,editable=False)
    lecturesConducted = models.IntegerField(verbose_name='No. of Lectures conducted',default=0)
    assignmentsPosted = models.IntegerField(verbose_name='No. of Assignments Posted',default=0)
    studentCount = models.IntegerField(verbose_name='Number Of Students',default=0)
    teacherCount = models.IntegerField(verbose_name = 'No of Teachers',default = 1)

    def getCode(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))

    def __str__(self):
        return self.className
    
    def save(self, *args, **kwargs):
        if self.classCode == '':
            self.classCode = self.getCode()
        super(Classroom,self).save(*args,**kwargs)

class classStudents(models.Model):
    class Meta:
        unique_together = ('classroom','student')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    classesAttended = models.IntegerField(default=0)
    assignmentSubmitted = models.IntegerField(verbose_name = 'No. Of Assignment Submitted', default=0)


class classTeachers(models.Model):
    class Meta:
        unique_together = ('classroom','teacher')
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

class classStream(models.Model):
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,null = False,blank=False,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time']

class streamComment(models.Model):
    stream = models.ForeignKey(classStream,on_delete=models.CASCADE)
    reply = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    time = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['time']

class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    marks = models.IntegerField(null = True,blank = True)
    deadline = models.DateTimeField(null=True,blank=True)
    description = models.TextField(default = '',null = True,blank = True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['deadline']

def upload_path_handler(instance,filename):
    return instance.assignment.classroom.className + "/"+instance.assignment.title + "/"+filename

class StudentWork(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    work = models.FileField(upload_to=upload_path_handler)
    uploaded_at = models.DateTimeField(auto_now=True)
    plagCheck = models.BooleanField(default=False,null = True, blank = True)
    
    class Meta:
        ordering = ['uploaded_at']
