from pydoc import classname
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Teacher
from .forms import *
from .models import *

def getCode(self):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))


# Create your views here.
@login_required
def createClass(request):
    if request.user.is_teacher:
        if request.method == 'POST':
            form = classCreationForm(request.POST)
            if form.is_valid():
                form.save()
                classroom = Classroom.objects.get(className = form.cleaned_data['className'])
                # teacher = request.user.id
                teacher = Teacher.objects.get(user = request.user)
                classTeacher = classTeachers(classroom.id,teacher)
                print(classTeacher)
                classTeacher.save()
                return redirect('dash')
        else:
            form = classCreationForm()
        return render(request,'create-class.html',{'form':form})
    else:
        return redirect('dash')

@login_required
def joinclass(request):
    if request.method == 'POST':
        print(request.POST)
        code = request.POST.get('code')
        clsStudent = classStudents()
        try:  
            classroom = Classroom.objects.get(classCode = code)
            classroom.studentCount += 1
            # classroom.save()
            clsStudent.classroom = classroom
            clsStudent.student = Student.objects.get(user = request.user)
            clsStudent.save()

        except:
            messages.warning(request,'Code Did Not Match. Verify and Try Again')

    return redirect('dash')


# @login_required
# def streamview(request,name):
    # print(request.student.id)
    # print(request.student.name)
    # print(request.student.email)
    # return render(request,'classroom.html')
    # if request.user.is_student:
    #     print(request.user)
    # elif request.user.is_teacher:

def inClass(request,name):
    class_room = Classroom.objects.all().filter(className = name).first()
    if request.user.is_student:
        stu = Student.objects.all().filter(user = request.user).first()
        classes = classStudents.objects.all().filter(student = stu,classroom = class_room)
        return classes != None
    elif request.user.is_teacher:
        teacher = Teacher.objects.all().filter(user = request.user).first()
        return classTeachers.objects.filter(classroom = class_room,teacher = teacher) != None
    else:
        return True


@login_required
def streamview(request,name):
    
    class_room = Classroom.objects.all().filter(className = name).first()
    if inClass(request,name):
        stream = classStream.objects.filter(classroom = class_room.id)
        comments = []
        for i in stream:
            comments += streamComment.objects.filter(stream = i)
        print(type(class_room))
        return render(request,'classroom.html',{'class':class_room,'stream':stream,'comments':comments,'classname':name})
    else:
        return redirect('home')

@login_required
def peopleview(request,name):
    
    if inClass(request,name):
        class_room = Classroom.objects.all().get(className = name)
        teachers = classTeachers.objects.filter(classroom = class_room)
        students = classStudents.objects.filter(classroom = class_room)
        return render(request,'people.html',{'teachers':teachers,'students':students,'classname':name})
    else:
        return redirect('home')

def createAssignment(request,name):
    if request.method == 'POST':
        form = AssignmentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment-list',name)
    else:
        form  = AssignmentCreationForm()
    return render(request,'createAssignment.html',{'form':form,'classname':name})


@login_required
def assignments(request,name):
    if inClass(request,name):    
        class_room = Classroom.objects.all().get(className = name)
        assignments = Assignment.objects.all().filter(classroom = class_room).values('title','deadline','marks')
        return render(request,'assignment-list.html',{'assignments':assignments,'classname':name})
    else:
        return redirect('home')

def assignmentDetails(request,name):
    assignmentTitle = request.GET.get('title')
    class_room = Classroom.objects.all().get(className = name)
    assignmentDetail = Assignment.objects.all().filter(classroom = class_room,title=assignmentTitle).first()
    if assignmentDetail == None:
        return redirect('assignment-list',name)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST,request.FILES)
        print(request.POST)
        if form.is_valid():
            stuWork = StudentWork()
            stuWork.student = Student.objects.get(user = request.user)
            stuWork.assignment = assignmentDetail
            stuWork.work = form.cleaned_data['work']
            stuWork.save()
            return render(request,'assignment-list.html',{'assignmentDetail':assignmentDetail,'form':form})
    else:
        form = AssignmentSubmissionForm()

    if request.user.is_student:
        return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'form':form,'classname':name})
    else:
        stuwork = StudentWork.objects.filter(assignment = assignmentDetail)
        return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'classWork':stuwork,'classname':name})

@login_required
def createStream(request,name):
    if request.method == 'POST':
        stream = classStream()
        stream.classroom = Classroom.objects.get(className = name)
        stream.message = request.POST.get('post')
        stream.user = request.user
        stream.save()
        return redirect('class',name)
    else:
        return redirect('class',name)

@login_required
def createComment(request,name):
    if request.method == 'POST':
        comment = streamComment()
        comment.stream = classStream.objects.get(id = request.GET.get('id'))
        comment.reply = request.POST.get('comment')
        comment.user = request.user
        comment.save()
        return redirect('class',name)
    else:
        return redirect('class',name)