from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
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
        role = request.POST.get('role')

    #create the user
        user = User.objects.create_user(
            username= email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
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
        if user is None:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
        
        if user is not None:
            login(request, user)
            
        
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('dashboard')
            messages.success(request, 'Logged in successfully.')
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

def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token, is_used=False).first()

    if not reset_request or reset_request.is_valid():
        messages.error(request, 'Invalid or expired link.')
        return redirect('index')
    
    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successfully.')
        return redirect('login')
    
    return render(request, 'reset_password.html', {'token': token})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')