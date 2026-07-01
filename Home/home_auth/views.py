from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser as User, PasswordResetRequest
from Student.models import Student
from school.models import Teacher

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'student')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_student = role == 'student'
        user.is_teacher = role == 'teacher'
        user.is_admin = role == 'admin'
        user.is_authorised = True
        user.save()

        login(request, user)
        messages.success(request, 'Account created successfully.')

        if user.is_teacher:
            return redirect('teacher_dashboard')
        if user.is_student:
            return redirect('dashboard')
        return redirect('index')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

        is_super_admin = user.email.lower() == 'sparsh@gmail.com' or user.is_admin
        user.is_admin = is_super_admin or user.is_admin
        user.save(update_fields=['is_admin'])

        login(request, user)
        if user.is_admin:
            messages.success(request, 'Logged in successfully.')
            return redirect('admin_allocation')

        if user.is_teacher or Teacher.objects.filter(first_name=user.first_name, last_name=user.last_name).exists():
            messages.success(request, f'Logged in successfully as {user.first_name} {user.last_name}.')
            return redirect('teacher_students')

        if user.is_student or Student.objects.filter(first_name=user.first_name, last_name=user.last_name).exists():
            messages.success(request, f'Logged in successfully as {user.first_name} {user.last_name}.')
            return redirect('/Student/profile/')

        messages.success(request, 'Logged in successfully.')
        return redirect('index')

    return render(request, 'authentication/login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email)
            reset_request.send_reset_email()
            messages.success(request, 'Password reset email sent.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')
    return render(request, 'authentication/forgot_password.html')


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(
        token=token,
    ).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired link.')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not new_password or not confirm_password:
            messages.error(request, 'Please provide and confirm your new password.')
            return redirect('reset-password', token=token)
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset-password', token=token)

        reset_request.user.set_password(new_password)
        reset_request.user.save()

        reset_request.is_used = True
        reset_request.save()

        messages.success(request, 'Password reset successfully.')
        return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')