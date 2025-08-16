from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from authentication.models import TeacherProfile, StudentProfile

class Subject(models.Model):
    """Subject/Course model"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']

class Exam(models.Model):
    """Main Exam model"""
    EXAM_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='created_exams')

    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")

    # Settings
    total_marks = models.PositiveIntegerField(default=0)
    passing_marks = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=1)
    shuffle_questions = models.BooleanField(default=False)
    show_results_immediately = models.BooleanField(default=True)

    # Status
    status = models.CharField(max_length=20, choices=EXAM_STATUS_CHOICES, default='draft')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.subject.code}"

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.status == 'active'

    @property
    def is_upcoming(self):
        return timezone.now() < self.start_time and self.status in ['scheduled', 'active']

    @property
    def is_past(self):
        return timezone.now() > self.end_time or self.status == 'completed'

    def get_total_questions(self):
        return self.questions.count()

    def calculate_total_marks(self):
        """Calculate and update total marks based on questions"""
        total = sum(question.marks for question in self.questions.all())
        self.total_marks = total
        self.save()
        return total

    def get_enrolled_students_count(self):
        return self.enrollments.filter(is_active=True).count()

    def get_attempts_count(self):
        return self.attempts.count()

    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    """Question model for exams"""
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    # For essay and short answer questions
    expected_answer = models.TextField(blank=True, help_text="Expected answer for reference")

    # Settings
    is_required = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

    class Meta:
        ordering = ['exam', 'order']
        unique_together = ['exam', 'order']

class QuestionOption(models.Model):
    """Options for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_text} ({'Correct' if self.is_correct else 'Incorrect'})"

    class Meta:
        ordering = ['question', 'order']
        unique_together = ['question', 'order']

class ExamAttempt(models.Model):
    """Student's attempt at an exam"""
    ATTEMPT_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('auto_submitted', 'Auto Submitted'),
        ('cancelled', 'Cancelled'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_attempts')
    attempt_number = models.PositiveIntegerField(default=1)

    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken_minutes = models.PositiveIntegerField(null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES, default='in_progress')

    # Scoring (calculated after submission)
    total_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_passed = models.BooleanField(null=True, blank=True)

    # Grading
    is_graded = models.BooleanField(default=False)
    graded_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_attempts')
    graded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.exam.title} (Attempt {self.attempt_number})"

    @property
    def is_active(self):
        return self.status == 'in_progress'

    def calculate_score(self):
        """Calculate the total score for this attempt"""
        total = 0
        for answer in self.answers.all():
            if answer.is_correct:
                total += answer.question.marks
        self.total_score = total
        self.percentage = (total / self.exam.total_marks) * 100 if self.exam.total_marks > 0 else 0
        self.is_passed = self.total_score >= self.exam.passing_marks
        self.save()
        return total

    class Meta:
        ordering = ['-started_at']
        unique_together = ['exam', 'student', 'attempt_number']

class Answer(models.Model):
    """Student's answer to a question"""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    # Different answer types
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, null=True, blank=True)  # For MCQ
    text_answer = models.TextField(blank=True)  # For short answer, essay, fill in blank
    boolean_answer = models.BooleanField(null=True, blank=True)  # For true/false

    # Grading
    is_correct = models.BooleanField(null=True, blank=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    teacher_feedback = models.TextField(blank=True)

    # Timestamps
    answered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.attempt.student.name} - Q{self.question.order}"

    def auto_grade(self):
        """Auto-grade the answer based on question type"""
        if self.question.question_type == 'mcq' and self.selected_option:
            self.is_correct = self.selected_option.is_correct
            self.marks_awarded = self.question.marks if self.is_correct else 0
        elif self.question.question_type == 'true_false' and self.boolean_answer is not None:
            # This would need logic to determine correct answer for true/false
            # For now, assume it's stored in expected_answer as 'True' or 'False'
            expected = self.question.expected_answer.lower() == 'true'
            self.is_correct = self.boolean_answer == expected
            self.marks_awarded = self.question.marks if self.is_correct else 0
        # For essay and short answer, manual grading is required
        self.save()

    class Meta:
        ordering = ['attempt', 'question__order']
        unique_together = ['attempt', 'question']

class ExamEnrollment(models.Model):
    """Students enrolled in an exam"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} enrolled in {self.exam.title}"

    class Meta:
        unique_together = ['exam', 'student']
        ordering = ['enrolled_at']

class ExamResult(models.Model):
    """Final results and analytics for exam attempts"""
    attempt = models.OneToOneField(ExamAttempt, on_delete=models.CASCADE, related_name='result')

    # Detailed scoring
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    unanswered = models.PositiveIntegerField(default=0)

    # Performance metrics
    accuracy_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    time_efficiency = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage of time used

    # Ranking (optional)
    rank = models.PositiveIntegerField(null=True, blank=True)

    # Generated report
    detailed_report = models.JSONField(default=dict, blank=True)  # Store detailed analytics

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result: {self.attempt.student.name} - {self.attempt.exam.title}"

    def generate_report(self):
        """Generate detailed performance report"""
        report = {
            'subject_wise_performance': {},
            'question_type_performance': {},
            'time_analysis': {},
            'recommendations': []
        }
        # Implementation would go here
        self.detailed_report = report
        self.save()

    class Meta:
        ordering = ['-created_at']
