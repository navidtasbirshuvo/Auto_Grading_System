from django.urls import path
from .views import student_register, teacher_register, login_view

urlpatterns = [
    path('student-register/', student_register, name='student-register'),
    path('teacher-register/', teacher_register, name='teacher-register'),
    path('login/', login_view, name='auth-login'),
]
