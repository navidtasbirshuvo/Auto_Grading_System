from django.urls import path
from .views import student_register, login_view, student_dashboard

urlpatterns = [
    path('student-register/', student_register, name='student_register'),
    path('login/', login_view, name='login'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
]