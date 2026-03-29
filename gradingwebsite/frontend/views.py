from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Question, StudentAnswer


# =========================
# PUBLIC / HOME
# =========================
def index(request):
    return render(request, "index.html")


# =========================
# DASHBOARDS
# =========================
@login_required
def student_dashboard(request):
    answers = StudentAnswer.objects.filter(student=request.user)
    return render(request, "student-dashboard.html", {
        "answers": answers
    })


@login_required
def teacher_dashboard(request):
    questions = Question.objects.filter(teacher=request.user)
    return render(request, "teacher-dashboard.html", {
        "questions": questions
    })


# =========================
# TEACHER: SET QUESTION
# =========================
@login_required
def set_question(request):
    if request.method == "POST":
        question_text = request.POST.get("question")
        correct_answer = request.POST.get("correct_answer")

        if not question_text or not correct_answer:
            messages.error(request, "All fields are required")
        else:
            Question.objects.create(
                teacher=request.user,
                question_text=question_text,
                correct_answer=correct_answer
            )
            messages.success(request, "Question created successfully")
            return redirect("set_question")

    return render(request, "set-question.html")


# =========================
# STUDENT: EXAM (QUESTION LIST)
# =========================
@login_required
def exam(request):
    questions = Question.objects.filter(is_active=True)
    return render(request, "exam.html", {
        "questions": questions
    })


# =========================
# STUDENT: ANSWER QUESTION
# =========================
@login_required
def exam_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # prevent duplicate submission
    if StudentAnswer.objects.filter(student=request.user, question=question).exists():
        messages.warning(request, "You already answered this question")
        return redirect("exam")

    if request.method == "POST":
        answer_text = request.POST.get("answer")

        if not answer_text:
            messages.error(request, "Answer cannot be empty")
        else:
            StudentAnswer.objects.create(
                student=request.user,
                question=question,
                answer_text=answer_text
            )
            messages.success(request, "Answer submitted successfully")
            return redirect("exam")

    return render(request, "exam-detail.html", {
        "question": question
    })


# =========================
# STUDENT: RESULTS
# =========================
@login_required
def student_results(request):
    answers = StudentAnswer.objects.filter(student=request.user)
    return render(request, "student-results.html", {
        "answers": answers
    })


# =========================
# TEACHER: VIEW STUDENT ANSWERS
# =========================
@login_required
def teacher_results(request):
    answers = StudentAnswer.objects.select_related("student", "question")
    return render(request, "teacher-results.html", {
        "answers": answers
    })


# =========================
# AUTH PAGES (STATIC)
# =========================
def student_login(request):
    return render(request, "student-login.html")


def student_register(request):
    return render(request, "student-register.html")


def teacher_login(request):
    return render(request, "teacher-login.html")


def teacher_register(request):
    return render(request, "teacher-register.html")


# =========================
# PROFILES (OPTIONAL)
# =========================
@login_required
def student_profile(request):
    return render(request, "student-profile.html")


@login_required
def teacher_profile(request):
    return render(request, "teacher-profile.html")


# =========================
# SETTINGS / EXTRA
# =========================
@login_required
def teacher_students(request):
    return render(request, "teacher-students.html")


@login_required
def teacher_settings(request):
    return render(request, "teacher-settings.html")
