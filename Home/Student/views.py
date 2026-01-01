from django.shortcuts import render
from .models import *
from django.contrib import messages

# Create your views here.

def add_student(request):
    if request.method -- "POST":
        first_name = request.Post.get("first_name")
        last_name = request.Post.get("last_name")
        student_id = request.Post.get("student_id")
        gender = request.Post.get("gender")
        date_of_birth = request.Post.get("date_of_birth")
        student_class = request.Post.get("student_class")
        religion = request.Post.get("religion")
        address = request.Post.get("address")
        joining_date = request.Post.get("joining_date")
        mobile_number = request.Post.get("mobile_number")
        admission_number = request.Post.get("admission_number")
        section = request.Post.get("section")
        student_image = request.Post.get("student_image")  
        
        #parent details from form
        parent = Parent.objects.create(
            father_name=request.Post.get("father_name"),
            mother_name=request.Post.get("mother_name"),
            father_mobile=request.Post.get("father_mobile"),
            father_email=request.Post.get("father_email"),
            mother_email=request.Post.get("mother_email"),
            mother_mobile=request.Post.get("mother_mobile"),
            father_occupation=request.Post.get("father_occupation"),
            mother_occupation=request.Post.get("mother_occupation"),
            address=request.Post.get("parent_address"),
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
            address=address,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )
        messages.success(request, "Student added successfully.")
        return render(request, "students/student_list.html")

    return render(request, "students/add-student.html")

def student_list(request):
    return render(request, "students/students.html")

def edit_student(request):
    return render(request, "students/edit-student.html")

def view_student(request):
    return render(request, "students/student-details.html")