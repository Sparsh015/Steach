from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    
]
