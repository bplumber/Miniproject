from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Teacher
from .forms import *
from .models import *
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
                teacher = Teacher.objects.get(user = request.user)
                ct = classTeachers()
                ct.classroom = classroom
                ct.teacher = teacher
                ct.save()
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
            classroom.save()
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
    assignments = Assignment.objects.all().filter(classroom = class_room)[:3]
    if inClass(request,name):
        stream = []
        message = classStream.objects.filter(classroom = class_room.id)
        for i in message:
            d = {}
            c = []
            d['message'] = i
            c = streamComment.objects.filter(stream = i)
            d['comments'] = c
            d['len'] = len(c)
            stream.append(d)
        assignments = Assignment.objects.all().filter(classroom = class_room)[:3]
        return render(request,'classroom.html',{'class':class_room,'stream':stream,'assignments':assignments,'classname':name})
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
            a = Assignment()
            a.classroom = Classroom.objects.get(className = name)
            a.title = request.POST.get('title')
            a.description = request.POST.get('description')
            if request.POST.get('marks'):
                a.marks = request.POST.get('marks')
            else:
                a.marks = None
            if request.POST.get('deadline'):
                a.deadline = request.POST.get('deadline')
            else:
                a.deadline = None
            a.save()
            return redirect('assignment-list',name)
    else:
        form  = AssignmentCreationForm()
    return render(request,'createAssignment.html',{'form':form,'classname':name})


@login_required
def assignments(request,name):
    if inClass(request,name):    
        class_room = Classroom.objects.all().get(className = name)
        assignments = Assignment.objects.all().filter(classroom = class_room)
        if request.user.is_student:
            submittedAssignments = StudentWork.objects.filter(student = Student.objects.get(user = request.user))
            pending = []
            submitted = []
            print(submittedAssignments)
            for i in assignments:
                s = False
                for j in submittedAssignments:
                    if i == j.assignment:
                        submitted.append(i)
                        s = True
                        break
                if not s:
                    pending.append(i)
            return render(request,'assignment-list.html',{'submitted':submitted,'pending':pending,'classname':name})
        else:
            return render(request,'assignment-list.html',{'assignments':assignments,'classname':name})
    else:
        return redirect('home')

@login_required
def assignmentDetails(request,name):
    assignmentTitle = request.GET.get('title')
    class_room = Classroom.objects.all().get(className = name)
    assignmentDetail = Assignment.objects.all().filter(classroom = class_room,title=assignmentTitle).first()
    
    if assignmentDetail == None:
        return redirect('assignment-list',name)
    if request.method == 'POST':
        if request.user.is_student:
            print(request.FILES)
            stuWork = StudentWork()
            stuWork.student = Student.objects.get(user = request.user)
            stuWork.assignment = assignmentDetail
            stuWork.work = request.FILES.get('work')
            qry= stuWork.work.read()
            # print(x)
            # qry = file_name.read()
            # file_name = str(str(file_name).split('mode')[0])[25:-2]
            user_notes = [qry]
            user_files = ['file_name']
            x_searches = []
            try:
                for x in search(query=qry, num=10, stop=10, pause=10.0):
                    x_searches.append(x)
                for x in range(0, len(x_searches) - 1):
                    url = x_searches[x]
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    all_p = soup.find_all('p')
                    all = ""
                    for i in all_p:
                        all += str(i.text)
                    user_notes.append(all)
                user_files.append(url)
                def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
                def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])
                vectors = vectorize(user_notes)
                s_vectors = list(zip(user_files, vectors))
                plagiarism_results = set()
                student_a = s_vectors[0][0]
                text_vector_a = s_vectors[0][1]
                new_vectors = s_vectors.copy()
                current_index = new_vectors.index((student_a, text_vector_a))
                del new_vectors[current_index]
                for student_b, text_vector_b in new_vectors:
                    sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                    student_pair = sorted((student_a, student_b))
                    score = (student_pair[0], student_pair[1], sim_score)
                    plagiarism_results.add(score)
                mx = 0
                for i in plagiarism_results:
                    if i[2]>mx:
                        mx = i[2]
                print('Accuracy is ' + str((mx)))
                if mx > 0.5:
                    messages.add_message(request,messages.ERROR,"Plagiarism Detected {}".format(mx))
                    return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'classname':name})
                else:
                    stuWork.plagCheck = True
                    stuWork.save()
                    messages.add_message(request,messages.SUCCESS,"Assignment Submitted Successfully")
                    myWork = StudentWork.objects.filter(student = Student.objects.get(user = request.user),assignment = assignmentDetail)
                    return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'myWork':myWork,'classname':name})
            except:
                stuWork.save()
                messages.add_message(request,messages.SUCCESS,"Assignment Saved Successfully")
                messages.add_message(request,messages.ERROR,"Too many requests for plagiarism.")
                return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'classname':name})
    
        else:
            stuwork = StudentWork.objects.filter(assignment = assignmentDetail)
            main_results = []
            if len(stuwork) > 1:
                user_files = []
                user_notes = []
                for i in stuwork:
                    filename = i.work.path
                    file = open(filename, encoding="utf-8").read()
                    user_files.append(filename.split('\\')[-1])
                    user_notes.append(file)
                def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
                def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])
                vectors = vectorize(user_notes)
                s_vectors = list(zip(user_files, vectors))
                plagiarism_results = set()
                for student_a, text_vector_a in s_vectors:
                    new_vectors = s_vectors.copy()
                    current_index = new_vectors.index((student_a, text_vector_a))
                    del new_vectors[current_index]
                    for student_b, text_vector_b in new_vectors:
                        sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                        student_pair = sorted((student_a, student_b))
                        score = (student_pair[0], student_pair[1], sim_score)
                        plagiarism_results.add(score)
                        main_results.append(plagiarism_results)
                # print(main_results)
                main_results = main_results[0]
            return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'classWork':stuwork,'classname':name,'main_results' : main_results})
    else:
        if request.user.is_student:
            myWork = StudentWork.objects.filter(student = Student.objects.get(user = request.user),assignment = assignmentDetail)
            return render(request,'assignment.html',{'assignmentDetail':assignmentDetail,'myWork':myWork,'classname':name})
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

@login_required
def leaveClass(request,name):
    classDetail = Classroom.objects.filter(className = name).first()
    if classDetail:
        classDetail.delete()
    return redirect('dash')