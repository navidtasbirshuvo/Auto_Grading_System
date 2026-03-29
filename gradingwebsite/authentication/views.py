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


        if not all([name, student_id, email, password, confirm_password, institution]):
            return render(request, 'student-register.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'student-register.html', {'error': 'Passwords do not match'})

        if len(password) < 6:
            return render(request, 'student-register.html', {'error': 'Password must be at least 6 characters long'})

        if User.objects.filter(username=student_id).exists():
            return render(request, 'student-register.html', {'error': 'Student ID already registered'})

        if User.objects.filter(email=email).exists():
            return render(request, 'student-register.html', {'error': 'Email already registered'})

        try:
            user = User.objects.create_user(username=student_id, email=email, password=password)

            student_profile = StudentProfile.objects.create(
                user=user,
                name=name,
                student_id=student_id,
                institution=institution
            )

            try:
                messages.success(request, 'Student account created successfully! Please login.')
            except:
                pass  # Handle case where messages framework is not available
            return redirect('login')
        except Exception as e:
            # Clean up any partially created user
            if User.objects.filter(username=student_id).exists():
                User.objects.filter(username=student_id).delete()
            return render(request, 'student-register.html', {'error': f'Registration failed: {str(e)}'})
    return render(request, 'student-register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')



        # Find all users with this email
        possible_users = User.objects.filter(email=email)
        
        if not possible_users.exists():
            messages.error(request, "No account found with that email.")
            return render(request, 'login.html')

        authenticated_user = None

        # Try to authenticate against each matching user
        for user_obj in possible_users:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                authenticated_user = user
                break
        
        if authenticated_user is not None:
            user = authenticated_user
            # Check if user has the appropriate profile for the selected role
            if role == "Teacher":
                try:
                    teacher_profile = TeacherProfile.objects.get(user=user)
                    login(request, user)
                    messages.success(request, "Logged in successfully as Teacher.")
                    return redirect('teacher-dashboard')
                except TeacherProfile.DoesNotExist:
                    # Continue expecting this might not be the right user if duplicates existed with diff roles? 
                    # But for now, let's assume if password matches, this IS the user.
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


        if not all([name, teacher_id, email, password, confirm_password, institution, department]):
            return render(request, 'teacher-register.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'teacher-register.html', {'error': 'Passwords do not match'})

        if len(password) < 6:
            return render(request, 'teacher-register.html', {'error': 'Password must be at least 6 characters long'})

        if User.objects.filter(username=teacher_id).exists():
            return render(request, 'teacher-register.html', {'error': 'Teacher ID already registered'})

        if User.objects.filter(email=email).exists():
            return render(request, 'teacher-register.html', {'error': 'Email already registered'})

        try:
            user = User.objects.create_user(username=teacher_id, email=email, password=password)
            teacher_profile = TeacherProfile.objects.create(
                user=user,
                name=name,
                teacher_id=teacher_id,
                institution=institution,
                department=department
            )

            # Subject creation removed as per new simple requirements


            try:
                messages.success(request, 'Teacher account created successfully! Please login.')
            except:
                pass  # Handle case where messages framework is not available
            return redirect('login')
        except Exception as e:
            # Clean up any partially created user
            if User.objects.filter(username=teacher_id).exists():
                User.objects.filter(username=teacher_id).delete()
            return render(request, 'teacher-register.html', {'error': f'Registration failed: {str(e)}'})
    return render(request, 'teacher-register.html')


