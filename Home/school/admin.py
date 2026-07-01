from django.contrib import admin
from .models import Teacher

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'first_name', 'last_name', 'subject', 'email', 'mobile_number')
    search_fields = ('teacher_id', 'first_name', 'last_name', 'subject', 'email')
    list_filter = ('subject', 'gender', 'joining_date')

