from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.exam_list, name='exam-list'),
    path('exams/create/', views.create_exam, name='create-exam'),
    path('exams/<int:exam_id>/', views.exam_detail, name='exam-detail'),
    path('exams/<int:exam_id>/start/', views.start_exam, name='start-exam'),
    path('exams/<int:exam_id>/submit/', views.submit_exam, name='submit-exam'),
    path('exams/<int:exam_id>/enroll/', views.enroll_students, name='enroll-students'),
    path('exams/<int:exam_id>/questions/', views.question_list, name='question-list'),
    path('questions/<int:question_id>/', views.question_detail, name='question-detail'),
    path('results/', views.results_list, name='results-list'),
    path('results/<int:attempt_id>/', views.result_detail, name='result-detail'),
    path('api/exams/', views.api_exam_list, name='api-exam-list'),
    path('api/subjects/', views.api_subject_list, name='api-subject-list'),
]