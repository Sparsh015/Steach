from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-students/', views.teacher_students, name='teacher_students'),
    path('allocation/', views.admin_allocation, name='admin_allocation'),
    # Teacher URLs
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<str:slug>/', views.view_teacher, name='view_teacher'),
    path('teachers/<str:slug>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<str:slug>/delete/', views.delete_teacher, name='delete_teacher'),
]
