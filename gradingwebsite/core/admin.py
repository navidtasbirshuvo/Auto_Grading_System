from django.contrib import admin
from .models import Question, StudentAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher", "created_at", "is_active")
    search_fields = ("question_text",)
    list_filter = ("is_active", "created_at")


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "question", "llm_score", "submitted_at")
    search_fields = ("answer_text",)
    list_filter = ("submitted_at",)
