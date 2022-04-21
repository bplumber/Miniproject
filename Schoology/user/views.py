from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .forms import *
from .models import Student,Teacher
from classroom.models import *

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('dash')
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST['email']
        passwd = request.POST['passwd']
        user = authenticate(request,username = email,password = passwd)
        if user is not None:
            auth_info ={
                'username':email,
                'password':make_password(passwd)
            }
            login(request,**auth_info)
            return redirect('dash')
        else:
            return redirect('login')
    return render(request,'login1.html',{'form':LoginForm})

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
            classDetails.append((i.classroom,))
    else:
        return redirect('login')

    return render(request,'dashboard.html',{'classes':classDetails})

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
                messages.success(request,'Thanks for Singing !!, Login to Continue')
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
                photo = studentForm.cleaned_data['photo']
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

