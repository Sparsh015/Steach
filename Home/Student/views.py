from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden

# Create your views here.
def add_student(request):
    if request.method == "POST":
        try:
            # student fields
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
            student_image = request.FILES.get("student_image")

            # parent fields
            parent = Parent.objects.create(
                father_name=request.POST.get("father_name"),
                mother_name=request.POST.get("mother_name"),
                father_mobile=request.POST.get("father_mobile"),
                father_email=request.POST.get("father_email"),
                mother_mobile=request.POST.get("mother_mobile"),
                mother_email=request.POST.get("mother_email"),
                father_occupation=request.POST.get("father_occupation"),
                mother_occupation=request.POST.get("mother_occupation"),
                present_address=request.POST.get("present_address"),
                permanent_address=request.POST.get("permanent_address"),
            )

            Student.objects.create(
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
            messages.error(request, "Student ID must be unique.")

    return render(request, "students/add-student.html")

def student_list(request):
    students = Student.objects.select_related('parent').all()
    return render(request, "students/students.html", {
        'student_list': students
    })

def edit_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None

    if request.method == "POST":

        # update parent
        parent.father_name = request.POST.get("father_name")
        parent.mother_name = request.POST.get("mother_name")
        parent.father_mobile = request.POST.get("father_mobile")
        parent.father_email = request.POST.get("father_email")
        parent.mother_mobile = request.POST.get("mother_mobile")
        parent.mother_email = request.POST.get("mother_email")
        parent.father_occupation = request.POST.get("father_occupation")
        parent.mother_occupation = request.POST.get("mother_occupation")
        parent.present_address = request.POST.get("present_address")
        parent.permanent_address = request.POST.get("permanent_address")
        parent.save()

        # update student
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.gender = request.POST.get("gender")
        student.date_of_birth = request.POST.get("date_of_birth")
        student.student_class = request.POST.get("student_class")
        student.religion = request.POST.get("religion")
        student.joining_date = request.POST.get("joining_date")
        student.mobile_number = request.POST.get("mobile_number")
        student.admission_number = request.POST.get("admission_number")
        student.section = request.POST.get("section")

        if request.FILES.get("student_image"):
            student.student_image = request.FILES.get("student_image")

        student.save()

        messages.success(request, "Student updated successfully.")
        return redirect("student_list")

    return render(request, "students/edit-student.html", {
        'student': student,
        'parent': parent
    })

def view_student(request,slug):
    student = get_object_or_404(Student, student_id = slug)
    context = {
        'student' : student
    }
    return render(request, "students/student-details.html",context)



def delete_student(request, slug):
    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    return HttpResponseForbidden()
