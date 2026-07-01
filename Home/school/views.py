from datetime import date
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, TeacherAttendance
from Student.models import Student
from django.db import IntegrityError
# Create your views here.


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_teacher or request.user.is_admin):
            messages.error(request, 'Only teachers can access this page.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped

def index(request):
    return render(request, "authentication/login.html")

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if user.is_teacher:
        return redirect('teacher_students')
    if user.is_student:
        return redirect('student_profile')
    if user.is_admin:
        return redirect('admin_allocation')
    messages.error(request, 'You do not have access to this page.')
    return redirect('index')

# Teacher Views
@login_required(login_url='login')
@teacher_required
def add_teacher(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            teacher_id = request.POST.get("teacher_id")
            email = request.POST.get("email")
            mobile_number = request.POST.get("mobile_number")
            subject = request.POST.get("subject")
            qualification = request.POST.get("qualification")
            gender = request.POST.get("gender")
            date_of_birth = request.POST.get("date_of_birth")
            joining_date = request.POST.get("joining_date")
            address = request.POST.get("address")
            teacher_image = request.FILES.get("teacher_image")

            Teacher.objects.create(
                first_name=first_name,
                last_name=last_name,
                teacher_id=teacher_id,
                email=email,
                mobile_number=mobile_number,
                subject=subject,
                qualification=qualification,
                gender=gender,
                date_of_birth=date_of_birth,
                joining_date=joining_date,
                address=address,
                teacher_image=teacher_image
            )

            messages.success(request, "Teacher added successfully.")
            return redirect('teacher_list')

        except IntegrityError:
            messages.error(request, "Teacher ID must be unique.")

    return render(request, "teachers/add-teacher.html")

@login_required(login_url='login')
@teacher_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, "teachers/teachers.html", {
        'teacher_list': teachers
    })

@login_required(login_url='login')
@teacher_required
def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    return render(request, "teachers/teacher-details.html", {
        'teacher': teacher
    })

@login_required(login_url='login')
@teacher_required
def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)

    if request.method == "POST":
        teacher.first_name = request.POST.get("first_name")
        teacher.last_name = request.POST.get("last_name")
        teacher.email = request.POST.get("email")
        teacher.mobile_number = request.POST.get("mobile_number")
        teacher.subject = request.POST.get("subject")
        teacher.qualification = request.POST.get("qualification")
        teacher.gender = request.POST.get("gender")
        teacher.date_of_birth = request.POST.get("date_of_birth")
        teacher.joining_date = request.POST.get("joining_date")
        teacher.address = request.POST.get("address")

        if request.FILES.get("teacher_image"):
            teacher.teacher_image = request.FILES.get("teacher_image")

        teacher.save()
        messages.success(request, "Teacher updated successfully.")
        return redirect('teacher_list')

    return render(request, "teachers/edit-teacher.html", {
        'teacher': teacher
    })

@login_required(login_url='login')
@teacher_required
def delete_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect('teacher_list')

    return render(request, "teachers/delete-teacher.html", {
        'teacher': teacher
    })

@login_required(login_url='login')
@teacher_required
def teacher_dashboard(request):
    return redirect('teacher_students')


@login_required(login_url='login')
@teacher_required
def teacher_students(request):
    try:
        teacher = Teacher.objects.get(
            first_name=request.user.first_name,
            last_name=request.user.last_name
        )
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('index')

    if request.method == "POST":
        status = request.POST.get('status', 'Present')
        TeacherAttendance.objects.update_or_create(
            teacher=teacher,
            date=date.today(),
            defaults={'status': status}
        )
        messages.success(request, f"Today's attendance marked as {status}.")
        return redirect('teacher_students')

    students = teacher.students.all()
    today_status = TeacherAttendance.objects.filter(teacher=teacher, date=date.today()).first()
    return render(request, "teachers/teacher-students.html", {
        'teacher': teacher,
        'students': students,
        'user_name': f"{teacher.first_name} {teacher.last_name}",
        'user_email': teacher.email,
        'student_count': students.count(),
        'today_status': today_status.status if today_status else 'Not marked',
    })


@login_required(login_url='login')
def admin_allocation(request):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can access this page.')
        if request.user.is_student:
            return redirect('student_profile')
        if request.user.is_teacher:
            return redirect('teacher_students')
        return redirect('index')

    teachers = Teacher.objects.prefetch_related('students').all()
    students = Student.objects.all()
    selected_teacher = None

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        selected_ids = request.POST.getlist('student_ids')
        selected_teacher = get_object_or_404(Teacher, id=teacher_id)
        selected_students = Student.objects.filter(id__in=selected_ids)
        selected_teacher.students.set(selected_students)
        messages.success(request, 'Student allocation updated successfully.')
        return redirect('admin_allocation')

    return render(request, 'admin/allocation.html', {
        'teachers': teachers,
        'students': students,
        'selected_teacher': selected_teacher,
    })