from django.shortcuts import render

# Create your views here.

def add_student(request):
    return render(request, "students/add-student.html")

def student_list(request):
    return render(request, "students/students.html")

def edit_student(request):
    return render(request, "students/edit-student.html")

def view_student(request):
    return render(request, "students/student-details.html")