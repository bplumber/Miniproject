from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class StudentForm(UserCreationForm):
    studentform = forms.BooleanField(widget=forms.HiddenInput,initial=True)
    name = forms.CharField(max_length=50)
    email = models.EmailField()
    # phone = models.CharField(max_length=10)
    photo = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['name','email','password1','password2','photo']

class TeacherForm(UserCreationForm):
    teacherform = forms.BooleanField(widget=forms.HiddenInput,initial=True)
    name = forms.CharField(max_length=50)
    email = models.EmailField()
    # phone = models.CharField(max_length=10)
    # photo = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['name','email','password1','password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    passwd = forms.CharField(max_length=20,widget=forms.PasswordInput)

    fields = '__all__'