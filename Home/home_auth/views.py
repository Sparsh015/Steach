from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser as User, PasswordResetRequest
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

    #create the user
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=role,
    )
    
    if role == 'student':
        user.is_student = True
    elif role == 'teacher':
        user.is_teacher = True
    elif role == 'admin':
        user.is_admin = True
    
    user.save()
    login(request,user)
    messages.success(request, 'Account created successfully.')
    return redirect('index')

    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username = email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('index')
        
        if user.is_admin:
            return redirect('admin_dashboard')
        elif user.is_teacher:
            return redirect('teacher_dashboard')
        elif user.is_student:
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid user role')
            return redirect('index')
        
    else:
        messages.error(request, 'Invalid email or password')
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