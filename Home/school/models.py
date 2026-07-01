from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from Student.models import Student

# Create your models here.

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female','Female'), ('Other','Other')])
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    students = models.ManyToManyField(Student, related_name='teachers', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
            slug = base_slug
            count = 1

            while Teacher.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name + " (" + self.subject + ")"


class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Absent")

    class Meta:
        unique_together = ('teacher', 'date')

    def __str__(self) -> str:
        return f"{self.teacher} - {self.date} - {self.status}"
