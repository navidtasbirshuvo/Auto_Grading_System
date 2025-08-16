from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import StudentProfile, TeacherProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def student_register(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        institution = request.POST.get('institution')

        if password != confirm_password:
            return render(request, 'student-register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=student_id).exists():
            return render(request, 'student-register.html', {'error': 'Student already registered'})
        try:
            user = User.objects.create_user(username=student_id, email=email, password=password)
            print("User Created: ", user.username)
            StudentProfile.objects.create(
                user=user,
                name=name,
                student_id=student_id,
                institution=institution
            )

            print("Student profile created for:", student_id)

            return redirect('login')  # Use named URL, not 'login.html'
        except Exception as e:
            print("Error creating user or profile:", e)
            return render(request, 'student-register.html', {'error': str(e)})
    return render(request, 'student-register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')



        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user has the appropriate profile for the selected role
            if role == "Teacher":
                try:
                    teacher_profile = TeacherProfile.objects.get(user=user)
                    login(request, user)
                    messages.success(request, "Logged in successfully as Teacher.")
                    return redirect('teacher-dashboard')
                except TeacherProfile.DoesNotExist:
                    messages.error(request, "You don't have teacher access. Please contact administrator.")
                    return render(request, 'login.html')
            else:  # Student role
                try:
                    student_profile = StudentProfile.objects.get(user=user)
                    login(request, user)
                    messages.success(request, "Logged in successfully as Student.")
                    return redirect('student-dashboard')
                except StudentProfile.DoesNotExist:
                    messages.error(request, "You don't have student access. Please contact administrator.")
                    return render(request, 'login.html')
        else:
            messages.error(request, "Invalid password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def teacher_register(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        teacher_id = request.POST.get('teacher_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        institution = request.POST.get('institution')
        department = request.POST.get('department')

        if password != confirm_password:
            return render(request, 'teacher-register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=teacher_id).exists():
            return render(request, 'teacher-register.html', {'error': 'Teacher already registered'})
        try:
            user = User.objects.create_user(username=teacher_id, email=email, password=password)
            print("User Created: ", user.username)
            TeacherProfile.objects.create(
                user=user,
                name=name,
                teacher_id=teacher_id,
                institution=institution,
                department=department
            )

            print("Teacher profile created for:", teacher_id)

            return redirect('login')  # Use named URL, not 'login.html'
        except Exception as e:
            print("Error creating user or profile:", e)
            return render(request, 'teacher-register.html', {'error': str(e)})
    return render(request, 'teacher-register.html')

# Dashboard views moved to frontend app
