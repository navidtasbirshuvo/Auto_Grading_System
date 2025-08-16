from django.contrib import admin
from .models import (
    Subject, Exam, Question, QuestionOption,
    ExamAttempt, Answer, ExamEnrollment, ExamResult
)

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4
    fields = ['option_text', 'is_correct', 'order']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'marks', 'order']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'code', 'teacher__name']
    ordering = ['code']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'status', 'start_time', 'end_time', 'total_marks']
    list_filter = ['status', 'subject', 'teacher', 'created_at']
    search_fields = ['title', 'subject__name', 'teacher__name']
    ordering = ['-created_at']
    inlines = [QuestionInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject', 'teacher')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'duration_minutes')
        }),
        ('Settings', {
            'fields': ('total_marks', 'passing_marks', 'max_attempts', 'shuffle_questions', 'show_results_immediately')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'question_text_short', 'question_type', 'marks', 'order']
    list_filter = ['question_type', 'exam__subject', 'exam']
    search_fields = ['question_text', 'exam__title']
    ordering = ['exam', 'order']
    inlines = [QuestionOptionInline]

    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text_short', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__exam']
    search_fields = ['option_text', 'question__question_text']
    ordering = ['question', 'order']

    def option_text_short(self, obj):
        return obj.option_text[:30] + "..." if len(obj.option_text) > 30 else obj.option_text
    option_text_short.short_description = 'Option Text'

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'attempt_number', 'status', 'total_score', 'percentage', 'started_at']
    list_filter = ['status', 'is_passed', 'exam', 'started_at']
    search_fields = ['student__name', 'exam__title']
    ordering = ['-started_at']
    readonly_fields = ['started_at', 'total_score', 'percentage', 'is_passed']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'marks_awarded', 'answered_at']
    list_filter = ['is_correct', 'question__question_type', 'attempt__exam']
    search_fields = ['attempt__student__name', 'question__question_text']
    ordering = ['-answered_at']

@admin.register(ExamEnrollment)
class ExamEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'enrolled_at', 'is_active']
    list_filter = ['is_active', 'exam', 'enrolled_at']
    search_fields = ['student__name', 'exam__title']
    ordering = ['-enrolled_at']

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'total_questions', 'correct_answers', 'accuracy_percentage', 'rank']
    list_filter = ['attempt__exam', 'created_at']
    search_fields = ['attempt__student__name', 'attempt__exam__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
