from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.

def add_student(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            student_id = request.POST.get("student_id")
            gender = request.POST.get("gender")
            date_of_birth = request.POST.get("date_of_birth")
            student_class = request.POST.get("student_class")
            religion = request.POST.get("religion")
            joining_date = request.POST.get("joining_date")
            mobile_number = request.POST.get("mobile_number")
            admission_number = request.POST.get("admission_number")
            section = request.POST.get("section")
            student_image = request.POST.get("student_image")  
            
            #parent details from form
            parent = Parent.objects.create(
                father_name=request.POST.get("father_name"),
                mother_name=request.POST.get("mother_name"),
                father_mobile=request.POST.get("father_mobile"),
                father_email=request.POST.get("father_email"),
                mother_email=request.POST.get("mother_email"),
                mother_mobile=request.POST.get("mother_mobile"),
                father_occupation=request.POST.get("father_occupation"),
                mother_occupation=request.POST.get("mother_occupation"),
                present_address=request.POST.get("present_address"),
                permanent_address=request.POST.get("permanent_address")
            )

            #save student information
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=date_of_birth,    
                student_class=student_class,
                religion=religion,
                joining_date=joining_date,
                mobile_number=mobile_number,
                admission_number=admission_number,
                section=section,
                student_image=student_image,
                parent=parent
            )
            messages.success(request, "Student added successfully.")
        except IntegrityError:
            messages.error(request, "Student ID must be unique. A student with this ID already exists.")
        #return render(request, "students/student_list.html")

    return render(request, "students/add-student.html")

def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    context = {
        'student_list' : student_list
    }
    return render(request, "students/students.html", context)

def edit_student(request):
    return render(request, "students/edit-student.html")

def view_student(request):
    student = get_object_or_404(Student, student_id = slug)
    context = {
        'student' : student
    }
    return render(request, "students/student-details.html")