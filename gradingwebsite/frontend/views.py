from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Exam, Subject, ExamEnrollment
from authentication.models import StudentProfile, TeacherProfile

def index(request):
    return render(request, 'index.html')

def student_dashboard(request):
    return render(request, 'student-dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher-dashboard.html')

def student_results(request):
    return render(request, 'student-results.html')

def teacher_results(request):
    return render(request, 'teacher-results.html')

@login_required
def set_question(request):
    context = {}

    if hasattr(request.user, 'teacherprofile'):
        subjects = Subject.objects.filter(teacher=request.user.teacherprofile)
        context['subjects'] = subjects
        context['user_type'] = 'teacher'
    else:
        context['subjects'] = []
        context['user_type'] = 'unknown'

    return render(request, 'set-question.html', context)

def student_login(request):
    return render(request, 'student-login.html')

def student_register(request):
    return render(request, 'student-register.html')

def student_profile(request):
    return render(request, 'student-profile.html')

def teacher_login(request):
    return render(request, 'teacher-login.html')

def teacher_register(request):
    return render(request, 'teacher-register.html')

def teacher_profile(request):
    return render(request, 'teacher-profile.html')

def exam_detail(request):
    return render(request, 'exam-detail.html')

@login_required
def past_exams(request):
    if hasattr(request.user, 'studentprofile'):
        enrollments = ExamEnrollment.objects.filter(
            student=request.user.studentprofile,
            is_active=True
        )
        past_exams = [enrollment.exam for enrollment in enrollments if enrollment.exam.is_past]
        context = {
            'exams': past_exams,
            'user_type': 'student'
        }
    else:
        context = {'exams': [], 'user_type': 'unknown'}

    return render(request, 'past-exams.html', context)

@login_required
def current_exams(request):
    if hasattr(request.user, 'studentprofile'):
        enrollments = ExamEnrollment.objects.filter(
            student=request.user.studentprofile,
            is_active=True,
            exam__status='active'
        )
        current_exams = [enrollment.exam for enrollment in enrollments if enrollment.exam.is_active]
        context = {
            'exams': current_exams,
            'user_type': 'student'
        }
    else:
        context = {'exams': [], 'user_type': 'unknown'}

    return render(request, 'current-exams.html', context)

@login_required
def upcoming_exams(request):
    if hasattr(request.user, 'studentprofile'):
        enrollments = ExamEnrollment.objects.filter(
            student=request.user.studentprofile,
            is_active=True,
            exam__status__in=['scheduled', 'active']
        )
        upcoming_exams = [enrollment.exam for enrollment in enrollments if enrollment.exam.is_upcoming]
        context = {
            'exams': upcoming_exams,
            'user_type': 'student'
        }
    else:
        context = {'exams': [], 'user_type': 'unknown'}

    return render(request, 'upcoming-exams.html', context)

@login_required
def manage_exams(request):
    if hasattr(request.user, 'teacherprofile'):
        exams = Exam.objects.filter(teacher=request.user.teacherprofile).order_by('-created_at')
        context = {
            'exams': exams,
            'user_type': 'teacher'
        }
    else:
        context = {'exams': [], 'user_type': 'unknown'}

    return render(request, 'manage-exams.html', context)

def teacher_students(request):
    return render(request, 'teacher-students.html')

def teacher_settings(request):
    return render(request, 'teacher-settings.html')