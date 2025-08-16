from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from authentication.models import TeacherProfile, StudentProfile
from core.models import Subject, Exam, Question, QuestionOption, ExamEnrollment

class Command(BaseCommand):
    help = 'Create sample exam data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample exam data...')
        
        # Get existing teacher and student profiles
        try:
            teacher = TeacherProfile.objects.first()
            if not teacher:
                self.stdout.write(self.style.ERROR('No teacher profiles found. Please create a teacher first.'))
                return
                
            students = StudentProfile.objects.all()[:5]  # Get first 5 students
            if not students:
                self.stdout.write(self.style.ERROR('No student profiles found. Please create students first.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting profiles: {e}'))
            return

        # Create subjects
        subjects_data = [
            {'name': 'Computer Science Fundamentals', 'code': 'CS101', 'description': 'Introduction to Computer Science'},
            {'name': 'Data Structures', 'code': 'CS201', 'description': 'Data Structures and Algorithms'},
            {'name': 'Database Systems', 'code': 'CS301', 'description': 'Database Design and Management'},
        ]
        
        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults={
                    'name': subject_data['name'],
                    'description': subject_data['description'],
                    'teacher': teacher
                }
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'Created subject: {subject.code} - {subject.name}')

        # Create exams
        now = timezone.now()
        exams_data = [
            {
                'title': 'Midterm Exam - CS Fundamentals',
                'description': 'Midterm examination covering basic CS concepts',
                'subject': subjects[0],
                'start_time': now + timedelta(days=1),
                'end_time': now + timedelta(days=1, hours=2),
                'duration_minutes': 120,
                'total_marks': 100,
                'passing_marks': 60,
                'status': 'scheduled'
            },
            {
                'title': 'Quiz - Data Structures',
                'description': 'Quick quiz on arrays and linked lists',
                'subject': subjects[1],
                'start_time': now + timedelta(days=3),
                'end_time': now + timedelta(days=3, hours=1),
                'duration_minutes': 60,
                'total_marks': 50,
                'passing_marks': 30,
                'status': 'scheduled'
            }
        ]
        
        for exam_data in exams_data:
            exam, created = Exam.objects.get_or_create(
                title=exam_data['title'],
                defaults={
                    **exam_data,
                    'teacher': teacher
                }
            )
            if created:
                self.stdout.write(f'Created exam: {exam.title}')
                
                # Create sample questions for each exam
                self.create_sample_questions(exam)
                
                # Enroll students in the exam
                for student in students:
                    enrollment, created = ExamEnrollment.objects.get_or_create(
                        exam=exam,
                        student=student
                    )
                    if created:
                        self.stdout.write(f'Enrolled {student.name} in {exam.title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_sample_questions(self, exam):
        """Create sample questions for an exam"""
        if 'CS Fundamentals' in exam.title:
            questions_data = [
                {
                    'question_text': 'What does CPU stand for?',
                    'question_type': 'mcq',
                    'marks': 10,
                    'order': 1,
                    'options': [
                        {'text': 'Central Processing Unit', 'is_correct': True},
                        {'text': 'Computer Processing Unit', 'is_correct': False},
                        {'text': 'Central Program Unit', 'is_correct': False},
                        {'text': 'Computer Program Unit', 'is_correct': False},
                    ]
                },
                {
                    'question_text': 'Python is a compiled language.',
                    'question_type': 'true_false',
                    'marks': 5,
                    'order': 2,
                    'expected_answer': 'False'
                },
                {
                    'question_text': 'Explain the difference between RAM and ROM.',
                    'question_type': 'short_answer',
                    'marks': 15,
                    'order': 3,
                    'expected_answer': 'RAM is volatile memory used for temporary storage, ROM is non-volatile memory for permanent storage.'
                }
            ]
        else:
            questions_data = [
                {
                    'question_text': 'Which data structure follows LIFO principle?',
                    'question_type': 'mcq',
                    'marks': 10,
                    'order': 1,
                    'options': [
                        {'text': 'Queue', 'is_correct': False},
                        {'text': 'Stack', 'is_correct': True},
                        {'text': 'Array', 'is_correct': False},
                        {'text': 'Linked List', 'is_correct': False},
                    ]
                }
            ]
        
        for q_data in questions_data:
            question = Question.objects.create(
                exam=exam,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                marks=q_data['marks'],
                order=q_data['order'],
                expected_answer=q_data.get('expected_answer', '')
            )
            
            # Create options for MCQ questions
            if q_data['question_type'] == 'mcq' and 'options' in q_data:
                for i, option_data in enumerate(q_data['options']):
                    QuestionOption.objects.create(
                        question=question,
                        option_text=option_data['text'],
                        is_correct=option_data['is_correct'],
                        order=i + 1
                    )
        
        # Update exam total marks
        exam.calculate_total_marks()
