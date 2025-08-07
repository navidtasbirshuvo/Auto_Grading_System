from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    institution = forms.CharField(max_length=100)
    student_id = forms.CharField(max_length=20)

    class Meta:
        model = StudentProfile
        fields = ['institution', 'student_id']

