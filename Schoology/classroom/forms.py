from django import forms
from django.forms import ModelForm
from .models import Assignment, Classroom, StudentWork


class classCreationForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ['className','classSection','classDescription']

class AssignmentCreationForm(ModelForm):
    deadline = forms.DateTimeField(required=False,widget=forms.DateTimeInput())
    class Meta:
        model = Assignment
        fields = ['title','marks','deadline','description']

class AssignmentSubmissionForm(ModelForm):
    class Meta:
        model = StudentWork
        fields = ['work']

class JoinClassForm():
    code = forms.CharField(max_length=6)