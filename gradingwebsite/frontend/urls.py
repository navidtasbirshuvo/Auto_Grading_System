from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('set-question/', views.set_question, name='set_question'),
    path('teacher-results/', views.teacher_results, name='teacher_results'),
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher-students/', views.teacher_students, name='teacher_students'),
    path('teacher-settings/', views.teacher_settings, name='teacher_settings'),

    path('exam/', views.exam, name='exam'),
    path('exam/<int:question_id>/', views.exam_detail, name='exam_detail'),
    path('student-results/', views.student_results, name='student_results'),
    path('student-profile/', views.student_profile, name='student_profile'),

    path('student-login/', views.student_login, name='student_login'),
    path('student-register/', views.student_register, name='student_register'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('teacher-register/', views.teacher_register, name='teacher_register'),
]
