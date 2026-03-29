from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, StudentAnswer
from authentication.models import StudentProfile, TeacherProfile
from .services import grade_answer

# ==============================
# TEACHER VIEWS
# ==============================

@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'teacherprofile'):
        messages.error(request, "Access denied. Teacher only.")
        return redirect('login')

    questions = Question.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'core/teacher_dashboard.html', {'questions': questions})

@login_required
def create_question(request):
    if not hasattr(request.user, 'teacherprofile'):
        return redirect('student-dashboard')

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        correct_answer = request.POST.get('correct_answer')

        if not question_text or not correct_answer:
            messages.error(request, "Both question and correct answer are required.")
        else:
            Question.objects.create(
                teacher=request.user,
                question_text=question_text,
                correct_answer=correct_answer
            )
            messages.success(request, "Question created successfully.")
            return redirect('teacher-dashboard')

    return render(request, 'core/create_question.html')

@login_required
def teacher_results(request):
    """View all student answers for teacher's questions"""
    if not hasattr(request.user, 'teacherprofile'):
        return redirect('student-dashboard')
        
    # Get all answers for questions created by this teacher
    answers = StudentAnswer.objects.filter(question__teacher=request.user).select_related('student', 'question').order_by('-submitted_at')
    
    return render(request, 'core/teacher_results.html', {'answers': answers})

@login_required
def delete_result(request, answer_id):
    if not hasattr(request.user, 'teacherprofile'):
        messages.error(request, "Access denied.")
        return redirect('student-dashboard')
        
    if request.method == 'POST':
        answer = get_object_or_404(StudentAnswer, id=answer_id)
        if answer.question.teacher != request.user:
            messages.error(request, "You can only delete results for your own questions.")
            return redirect('teacher-results')
            
        answer.delete()
        messages.success(request, "Result deleted successfully.")
        
    return redirect('teacher-results')

# ==============================
# STUDENT VIEWS
# ==============================

@login_required
def student_results(request):
    """View all answers submitted by this student"""
    if not hasattr(request.user, 'studentprofile'):
        return redirect('teacher-dashboard')
        
    answers = StudentAnswer.objects.filter(student=request.user).select_related('question').order_by('-submitted_at')
    return render(request, 'core/student_results.html', {'answers': answers})

@login_required
def student_exams(request):
    """View available exams for student"""
    if not hasattr(request.user, 'studentprofile'):
        return redirect('teacher-dashboard')

    # Get all active questions
    all_questions = Question.objects.filter(is_active=True).order_by('-created_at')
    
    # Get answers by this student mapping question_id -> answer_id
    student_answers = StudentAnswer.objects.filter(student=request.user)
    answer_map = {ans.question_id: ans.id for ans in student_answers}
    
    questions_data = []
    for q in all_questions:
        ans_id = answer_map.get(q.id)
        questions_data.append({
            'id': q.id,
            'text': q.question_text,
            'is_answered': ans_id is not None,
            'answer_id': ans_id
        })

    return render(request, 'core/student_exams.html', {'questions': questions_data})

@login_required
def profile_view(request):
    user = request.user
    profile = None
    
    if hasattr(user, 'teacherprofile'):
        profile = user.teacherprofile
    elif hasattr(user, 'studentprofile'):
        profile = user.studentprofile
        
    return render(request, 'core/profile.html', {
        'profile': profile,
        'user': user
    })

def student_dashboard(request):
    if not hasattr(request.user, 'studentprofile'):
        messages.error(request, "Access denied. Student only.")
        return redirect('login')

    # Calculate Stats
    total_exams = Question.objects.filter(is_active=True).count()
    student_answers = StudentAnswer.objects.filter(student=request.user)
    completed_exams = student_answers.count()
    
    # Calculate Average Score
    graded_answers = [a for a in student_answers if a.llm_score is not None]
    if graded_answers:
        avg_score = sum(a.llm_score for a in graded_answers) / len(graded_answers)
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0

    context = {
        'stats': {
            'total_exams': total_exams,
            'completed_exams': completed_exams,
            'avg_score': avg_score
        }
    }

    return render(request, 'core/student_dashboard.html', context)

@login_required
def attempt_question(request, question_id):
    if not hasattr(request.user, 'studentprofile'):
        return redirect('teacher-dashboard')

    question = get_object_or_404(Question, id=question_id)
    
    # Check if already answered
    if StudentAnswer.objects.filter(student=request.user, question=question).exists():
        messages.info(request, "You have already answered this question.")
        return redirect('student-dashboard')

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        
        if not user_answer:
            messages.error(request, "Please provide an answer.")
        else:
            # Create the answer record first
            student_answer = StudentAnswer(
                student=request.user,
                question=question,
                answer_text=user_answer
            )
            
            # Call Grading Service
            try:
                score = grade_answer(question.question_text, question.correct_answer, user_answer)
                student_answer.llm_score = score
            except Exception as e:
                # Log error, keep score as None or 0
                print(f"Grading failed: {e}")
                student_answer.llm_score = 0
            
            student_answer.save()
            messages.success(request, "Answer submitted and graded!")
            return redirect('result-detail', answer_id=student_answer.id)

    return render(request, 'core/attempt_question.html', {'question': question})

@login_required
def result_detail(request, answer_id):
    """
    Shows the result to the student.
    Strictly NO correct answer shown.
    """
    answer = get_object_or_404(StudentAnswer, id=answer_id)
    
    # Security check: only the student who submitted or the teacher who created the question can view
    is_owner = answer.student == request.user
    is_teacher = answer.question.teacher == request.user
    
    if not (is_owner or is_teacher):
        messages.error(request, "Access denied.")
        return redirect('home')

    return render(request, 'core/result_detail.html', {'answer': answer})
