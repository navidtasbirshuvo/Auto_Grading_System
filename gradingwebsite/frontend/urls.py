from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('student-results/', views.student_results, name='student-results'),
    path('teacher-results/', views.teacher_results, name='teacher-results'),
    path('set-question/', views.set_question, name='set-question'),
    path('student-login/', views.student_login, name='student-login'),
    path('student-register/', views.student_register, name='student-register'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('teacher-login/', views.teacher_login, name='teacher-login'),
    path('teacher-register/', views.teacher_register, name='teacher-register'),
    path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    path('exam-detail/', views.exam_detail, name='exam-detail'),
    path('past-exams/', views.past_exams, name='past-exams'),
    path('current-exams/', views.current_exams, name='current-exams'),
    path('upcoming-exams/', views.upcoming_exams, name='upcoming-exams'),
]