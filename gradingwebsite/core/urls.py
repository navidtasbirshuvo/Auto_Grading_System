from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('teacher/create-question/', views.create_question, name='create-question'),
    path('teacher/results/', views.teacher_results, name='teacher-results'),
    path('teacher/result/delete/<int:answer_id>/', views.delete_result, name='delete-result'),

    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('student/exams/', views.student_exams, name='student-exams'),
    path('student/results/', views.student_results, name='student-results'),
    path('student/attempt/<int:question_id>/', views.attempt_question, name='attempt-question'),
    
    # Result
    path('result/<int:answer_id>/', views.result_detail, name='result-detail'),
    
    # API / Compatibility (if needed, but mostly we use the views above)
]