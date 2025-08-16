from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Exam, Question, Subject, ExamAttempt, ExamEnrollment, QuestionOption
from authentication.models import StudentProfile, TeacherProfile

@login_required
def exam_list(request):
    """List all exams for the current user"""
    try:
        # Check if user is a teacher or student
        if hasattr(request.user, 'teacherprofile'):
            # Teacher view - show exams they created
            exams = Exam.objects.filter(teacher=request.user.teacherprofile)
            context = {'exams': exams, 'user_type': 'teacher'}
        elif hasattr(request.user, 'studentprofile'):
            # Student view - show enrolled exams
            enrollments = ExamEnrollment.objects.filter(
                student=request.user.studentprofile,
                is_active=True
            )
            exams = [enrollment.exam for enrollment in enrollments]
            context = {'exams': exams, 'user_type': 'student'}
        else:
            context = {'exams': [], 'user_type': 'unknown'}

        return render(request, 'core/exam_list.html', context)
    except Exception as e:
        return render(request, 'core/exam_list.html', {'error': str(e)})

@login_required
def exam_detail(request, exam_id):
    """Show exam details"""
    exam = get_object_or_404(Exam, id=exam_id)

    context = {
        'exam': exam,
        'questions': exam.questions.all().order_by('order'),
        'total_questions': exam.get_total_questions(),
    }

    # Add user-specific context
    if hasattr(request.user, 'studentprofile'):
        # Check if student is enrolled
        enrollment = ExamEnrollment.objects.filter(
            exam=exam,
            student=request.user.studentprofile
        ).first()
        context['is_enrolled'] = enrollment is not None

        # Check previous attempts
        attempts = ExamAttempt.objects.filter(
            exam=exam,
            student=request.user.studentprofile
        ).order_by('-started_at')
        context['attempts'] = attempts
        context['can_attempt'] = len(attempts) < exam.max_attempts

    return render(request, 'core/exam_detail.html', context)

@login_required
def start_exam(request, exam_id):
    """Start an exam attempt"""
    # Placeholder for exam starting logic
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'core/start_exam.html', {'exam': exam})

@login_required
def submit_exam(request, exam_id):
    """Submit an exam attempt"""
    # Placeholder for exam submission logic
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'core/submit_exam.html', {'exam': exam})

@login_required
def question_list(request, exam_id):
    """List questions for an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().order_by('order')
    return render(request, 'core/question_list.html', {'exam': exam, 'questions': questions})

@login_required
def question_detail(request, question_id):
    """Show question details"""
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'core/question_detail.html', {'question': question})

@login_required
def results_list(request):
    """List exam results"""
    # Placeholder for results listing
    return render(request, 'core/results_list.html', {})

@login_required
def result_detail(request, attempt_id):
    """Show detailed result for an attempt"""
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)
    return render(request, 'core/result_detail.html', {'attempt': attempt})

# API Views for AJAX calls
@login_required
def api_exam_list(request):
    """API endpoint to get exams as JSON"""
    try:
        if hasattr(request.user, 'teacherprofile'):
            exams = Exam.objects.filter(teacher=request.user.teacherprofile)
        elif hasattr(request.user, 'studentprofile'):
            enrollments = ExamEnrollment.objects.filter(
                student=request.user.studentprofile,
                is_active=True
            )
            exams = [enrollment.exam for enrollment in enrollments]
        else:
            exams = []

        exam_data = []
        for exam in exams:
            exam_data.append({
                'id': exam.id,
                'title': exam.title,
                'subject': exam.subject.name,
                'start_time': exam.start_time.isoformat(),
                'end_time': exam.end_time.isoformat(),
                'status': exam.status,
                'total_marks': exam.total_marks,
                'is_active': exam.is_active,
                'is_upcoming': exam.is_upcoming,
                'is_past': exam.is_past,
            })

        return JsonResponse({'exams': exam_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_subject_list(request):
    """API endpoint to get subjects as JSON"""
    try:
        if hasattr(request.user, 'teacherprofile'):
            subjects = Subject.objects.filter(teacher=request.user.teacherprofile)
        else:
            subjects = Subject.objects.all()

        subject_data = []
        for subject in subjects:
            subject_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'description': subject.description,
            })

        return JsonResponse({'subjects': subject_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def create_exam(request):
    """Create a new exam"""
    if not hasattr(request.user, 'teacherprofile'):
        messages.error(request, "Only teachers can create exams.")
        return redirect('teacher-dashboard')

    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            subject_id = request.POST.get('subject')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            duration_minutes = request.POST.get('duration_minutes')
            total_marks = request.POST.get('total_marks', 0)
            passing_marks = request.POST.get('passing_marks', 0)
            max_attempts = request.POST.get('max_attempts', 1)
            shuffle_questions = request.POST.get('shuffle_questions') == 'on'
            show_results_immediately = request.POST.get('show_results_immediately') == 'on'
            auto_enroll_all = request.POST.get('auto_enroll_all') == 'on'  # New field

            # Validate required fields
            if not all([title, subject_id, start_time, end_time, duration_minutes]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('create-exam')

            # Get subject
            subject = get_object_or_404(Subject, id=subject_id, teacher=request.user.teacherprofile)

            # Parse datetime strings
            start_datetime = datetime.fromisoformat(start_time.replace('T', ' '))
            end_datetime = datetime.fromisoformat(end_time.replace('T', ' '))

            # Create exam
            exam = Exam.objects.create(
                title=title,
                description=description,
                subject=subject,
                teacher=request.user.teacherprofile,
                start_time=start_datetime,
                end_time=end_datetime,
                duration_minutes=int(duration_minutes),
                total_marks=int(total_marks),
                passing_marks=int(passing_marks),
                max_attempts=int(max_attempts),
                shuffle_questions=shuffle_questions,
                show_results_immediately=show_results_immediately,
                status='scheduled'
            )

            # Auto-enroll all students if requested
            if auto_enroll_all:
                students = StudentProfile.objects.all()
                for student in students:
                    ExamEnrollment.objects.get_or_create(
                        exam=exam,
                        student=student,
                        defaults={'is_active': True}
                    )
                messages.success(request, f"Exam created successfully! {students.count()} students enrolled automatically.")
            else:
                messages.success(request, "Exam created successfully!")

            return redirect('manage-exams')

        except Exception as e:
            messages.error(request, f"Error creating exam: {str(e)}")
            return redirect('create-exam')

    # GET request - show form
    subjects = Subject.objects.filter(teacher=request.user.teacherprofile)
    return render(request, 'core/create_exam.html', {'subjects': subjects})

@login_required
def enroll_students(request, exam_id):
    """Enroll students in an exam"""
    exam = get_object_or_404(Exam, id=exam_id)

    # Check if user is the teacher who created this exam
    if not hasattr(request.user, 'teacherprofile') or exam.teacher != request.user.teacherprofile:
        messages.error(request, "You don't have permission to manage this exam.")
        return redirect('manage-exams')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'enroll_all':
            # Enroll all students
            students = StudentProfile.objects.all()
            enrolled_count = 0
            for student in students:
                enrollment, created = ExamEnrollment.objects.get_or_create(
                    exam=exam,
                    student=student,
                    defaults={'is_active': True}
                )
                if created:
                    enrolled_count += 1
            messages.success(request, f"Enrolled {enrolled_count} new students in the exam.")

        elif action == 'enroll_selected':
            # Enroll selected students
            student_ids = request.POST.getlist('students')
            enrolled_count = 0
            for student_id in student_ids:
                try:
                    student = StudentProfile.objects.get(id=student_id)
                    enrollment, created = ExamEnrollment.objects.get_or_create(
                        exam=exam,
                        student=student,
                        defaults={'is_active': True}
                    )
                    if created:
                        enrolled_count += 1
                except StudentProfile.DoesNotExist:
                    continue
            messages.success(request, f"Enrolled {enrolled_count} students in the exam.")

        return redirect('enroll-students', exam_id=exam_id)

    # GET request - show enrollment form
    enrolled_students = ExamEnrollment.objects.filter(exam=exam, is_active=True).values_list('student_id', flat=True)
    all_students = StudentProfile.objects.all()
    available_students = all_students.exclude(id__in=enrolled_students)

    context = {
        'exam': exam,
        'enrolled_students': ExamEnrollment.objects.filter(exam=exam, is_active=True),
        'available_students': available_students,
        'total_students': all_students.count(),
        'enrolled_count': len(enrolled_students)
    }

    return render(request, 'core/enroll_students.html', context)
