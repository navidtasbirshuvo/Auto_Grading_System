from django.db import models
from django.contrib.auth.models import User


# =========================
# QUESTION MODEL (TEACHER)
# =========================
class Question(models.Model):
    """
    Teacher creates questions and provides the correct answer.
    The correct answer will be used by the LLM for grading.
    """

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_questions"
    )
    question_text = models.TextField()
    correct_answer = models.TextField(
        help_text="Correct answer used by LLM for grading"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.id}: {self.question_text[:50]}"


# =========================
# STUDENT ANSWER MODEL
# =========================
class StudentAnswer(models.Model):
    """
    Student submits answer for a question.
    LLM evaluates and assigns score.
    """

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_answers"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    # LLM Grading (ONLY SCORE)
    llm_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Score given by LLM (0–10)"
    )

    def __str__(self):
        return f"{self.student.username} → Q{self.question.id}"

    class Meta:
        unique_together = ['student', 'question']
        ordering = ['-submitted_at']
