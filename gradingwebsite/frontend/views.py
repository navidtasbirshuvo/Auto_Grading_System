from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

# login_view moved to authentication app

def student_dashboard(request):
    return render(request, 'student-dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher-dashboard.html')

def student_results(request):
    return render(request, 'student-results.html')

def teacher_results(request):
    return render(request, 'teacher-results.html')

def set_question(request):
    return render(request, 'set-question.html')

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

def past_exams(request):
    return render(request, 'past-exams.html')

def current_exams(request):
    return render(request, 'current-exams.html')

def upcoming_exams(request):
    return render(request, 'upcoming-exams.html')

def manage_exams(request):
    return render(request, 'manage-exams.html')

def teacher_students(request):
    return render(request, 'teacher-students.html')

def teacher_settings(request):
    return render(request, 'teacher-settings.html')