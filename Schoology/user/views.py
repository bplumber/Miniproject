from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from .forms import *
from .models import Student,Teacher
from classroom.models import *
from googlesearch import search
from classroom.views import createStream

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('dash')
    return render(request,'index.html')


def dashboard(request):
    classDetails = []
    if request.user.is_student:
        classes = classStudents.objects.all().filter(student = Student.objects.get(user = request.user))
        print(classes)
        
        for i in classes:
            teachers = classTeachers.objects.all().filter(classroom = i.classroom)
            classDetails.append((i.classroom,teachers))
            
    elif request.user.is_teacher:
        classes = classTeachers.objects.all().filter(teacher = Teacher.objects.get(user = request.user))
        for i in classes:
            teachers = classTeachers.objects.all().filter(classroom = i.classroom)
            classDetails.append((i.classroom,teachers))
    else:
        return redirect('login')

    return render(request,'dashboard.html',{'classes':classDetails})

global results

def explore(request):
    if request.user.is_teacher:
        classDetails = []
        classes = classTeachers.objects.all().filter(teacher = Teacher.objects.get(user = request.user))
        for i in classes:
            classDetails.append(i.classroom)
        results = []
        savedLinks = Links.objects.filter(teacher=Teacher.objects.get(user = request.user))
        if request.method == 'POST':
            qry = request.POST.get('query')
            print("qry = {}".format(request.POST))
            # qry = 'Cloud Computing filetype: pdf'
            # results = 'A B C D E F G H I J'.split()
            qry += ' filetype: pdf'
            for x in search(qry, num=10, stop=10, pause=5):
                results.append(x)
            return render(request,'explore.html',{'savedLinks':savedLinks,'results':results,'classes':classDetails})
        # elif request.method == 'GET':
        #     val = request.GET.get('val')
        #     if val == 'share':
        #         classname = request.GET.get('class')
        #         stream = classStream()
        #         stream.classroom = Classroom.objects.get(className = classname)
        #         stream.message = request.GET.get('url')
        #         stream.user = request.user
        #         stream.save()
        #     elif val == 'save':
        #         link = Links()
        #         link.teacher = Teacher.objects.get(user = request.user)
        #         link.url = request.GET.get('url')
        #         link.save()
        #     elif val == 'del':
        #         link = Links.objects.filter(url = request.GET.get('url')).first()
        #         link.delete()
        #     return render(request,'explore.html',{'savedLinks':savedLinks,'results':results,'classes':classDetails})
        else:
            return render(request,'explore.html',{'savedLinks':savedLinks})
    else:
        return redirect('dash')   
    

def saveresult(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            link = Links()
            link.teacher = Teacher.objects.get(user = request.user)
            link.url = request.GET.get('url')
            link.save()
            return redirect('explore')
        else:
            return redirect('dash')
    else:
        return redirect('login')

def shareresult(request):
    classname = request.GET.get('class')
    stream = classStream()
    stream.classroom = Classroom.objects.get(className = classname)
    stream.message = request.GET.get('url')
    stream.user = request.user
    stream.save()
    return redirect('explore')

def deleteLink(request):
    if request.user.is_authenticated:
        link = Links.objects.filter(url = request.GET.get('url')).first()
        if link:
            link.delete()
        return redirect('explore')

def register(request):
    
    if request.method == 'POST':
        if 'teacherform' in request.POST:
            print("In teacher form")
            teacherForm = TeacherForm(request.POST)
            print(request.POST)
            if teacherForm.is_valid():
                print('formValid')
                username = teacherForm.cleaned_data['email']
                pass1 = teacherForm.cleaned_data['password1']
                name = teacherForm.cleaned_data['name']
                auth_info ={
                    'email':username,
                    'password':make_password(pass1)
                }
                user = User(**auth_info)
                user.is_teacher = True
                user.save()
                print('userSaved')
                user_obj = Teacher(user=user,name = name )
                user_obj.save()
                messages.success(request,'Thanks for Signing !!, Login to Continue')
                return redirect ('login')
            else:
                return render(request,'register.html',{'studentForm':StudentForm(),'teacherForm':teacherForm})
        elif 'studentform' in request.POST:
            studentForm = StudentForm(request.POST)
            if studentForm.is_valid():
                print('formValid')
                username = studentForm.cleaned_data['email']
                pass1 = studentForm.cleaned_data['password1']
                name = studentForm.cleaned_data['name']
                photo = request.FILES.get('photo')
                auth_info ={
                    'email':username,
                    'password':make_password(pass1)
                }
                user = User(**auth_info)
                user.is_student = True
                user.save()
                print('userSaved')
                user_obj = Student(user=user,name = name,photo = photo)
                user_obj.save()
                messages.success(request,'Thanks for Singing !!, Login to Continue')
                return redirect ('login')
            else:
                return render(request,'register.html',{'studentForm':studentForm,'teacherForm':TeacherForm()})
    else:
        studentForm = StudentForm()
        teacherForm = TeacherForm()
    return render(request,'register.html',{'studentForm':studentForm,'teacherForm':teacherForm})

