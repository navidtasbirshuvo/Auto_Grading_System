from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='unknown')
    student_id = models.CharField(max_length=20, unique=True)
    institution = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username  # Or self.name if you want

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='unknown')
    teacher_id = models.CharField(max_length=20, unique=True)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username  # Or self.name if you want
