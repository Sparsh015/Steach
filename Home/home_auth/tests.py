from django.test import TestCase
from django.urls import reverse

from home_auth.models import CustomUser
from school.models import Teacher
from Student.models import Parent, Student


class RoleBasedAccessTests(TestCase):
    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username='student@example.com',
            email='student@example.com',
            first_name='Student',
            last_name='User',
            password='password123',
        )
        self.student_user.is_student = True
        self.student_user.save()

        self.teacher_user = CustomUser.objects.create_user(
            username='teacher@example.com',
            email='teacher@example.com',
            first_name='Teacher',
            last_name='User',
            password='password123',
        )
        self.teacher_user.is_teacher = True
        self.teacher_user.save()

        self.admin_user = CustomUser.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='password123',
        )
        self.admin_user.is_admin = True
        self.admin_user.save()

        self.teacher = Teacher.objects.create(
            first_name='Teacher',
            last_name='User',
            teacher_id='T001',
            email='teacher@example.com',
            mobile_number='1234567890',
            subject='Math',
            qualification='MSc',
            gender='Male',
            date_of_birth='1990-01-01',
            joining_date='2020-01-01',
            address='Main Street',
        )

    def test_student_login_redirects_to_profile_page(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'student@example.com', 'password': 'password123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_profile'))

    def test_teacher_login_redirects_to_students_page(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'teacher@example.com', 'password': 'password123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_students'))

    def test_student_login_redirects_to_profile_when_role_flag_is_missing(self):
        student_without_flag = CustomUser.objects.create_user(
            username='student2@example.com',
            email='student2@example.com',
            first_name='Student',
            last_name='Two',
            password='password123',
        )
        Student.objects.create(
            first_name='Student',
            last_name='Two',
            student_id='S002',
            gender='Female',
            date_of_birth='2005-01-01',
            student_class='10',
            religion='Islam',
            joining_date='2024-01-01',
            mobile_number='1234567890',
            admission_number='A002',
            section='A',
            parent=Parent.objects.create(
                father_name='Father',
                father_occupation='Engineer',
                father_mobile='1234567890',
                father_email='father@example.com',
                mother_name='Mother',
                mother_occupation='Teacher',
                mother_email='mother@example.com',
                mother_mobile='1234567890',
                present_address='Address',
                permanent_address='Address',
            ),
        )

        response = self.client.post(
            reverse('login'),
            {'email': 'student2@example.com', 'password': 'password123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_profile'))

    def test_admin_allocation_page_is_admin_only(self):
        self.client.force_login(self.student_user)
        response = self.client.get(reverse('admin_allocation'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_profile'))
