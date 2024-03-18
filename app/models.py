from datetime import timezone

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User




# User registratiom type hirerarchy (for all users by default registered in HOD)

class customUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (3, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic',blank=True, null=True)


# Stores Staff by this model
class Staff(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    fines = models.CharField(max_length=30, blank=True, null=True)
    bonus = models.CharField(max_length=30, blank=True, null=True)
    tax = models.CharField(max_length=30, blank=True, null=True)
    salary_type = models.CharField(max_length=30)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, blank=True, null=True)
    work_format = models.CharField(max_length=30)
    salary_amount = models.CharField(max_length=30)
    birth_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    mobiletwo = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: {self.admin.first_name} {self.admin.last_name} | Role: {self.role} | Branch: {self.branch}"


# Stores Course by this view
class Course(models.Model):
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=150)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    teacher_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    days = models.CharField(max_length=25, blank=True, null=True)
    hours = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated

    # This will display the subject info in the list within admin panel
    def __str__(self):
        return '{}'.format(self.subject + " | " + self.level)


# Stores Students by this model using also custom User model
class Student(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)
    mobiletwo = models.CharField(max_length=14)
    preferred_course = models.CharField(max_length=30, blank=True, null=True)
    preferred_level = models.CharField(max_length=30, blank=True, null=True)
    preferred_days = models.CharField(max_length=30, blank=True, null=True)
    preferred_time = models.CharField(max_length=30, blank=True, null=True)
    last_payment = models.ForeignKey(
        'Payments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='last_payment_for_student',
        help_text='Last payment made by the student',
    )
    address = models.CharField(max_length=150, blank=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)
    birth_date = models.DateTimeField()
    status = models.CharField(max_length=20, blank=True, null=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.admin.first_name + " " + self.admin.last_name)


# Stores payments by this model, used separately, also connected to a view for adding payment for existing students
class Payments(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    group_id = models.CharField(max_length=70)
    payment_type = models.CharField(max_length=15, blank=True, null=True)
    student_id = models.CharField(max_length=50)
    teacher_id = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.group_id} | {self.payment_type} | {self.student_id} | {self.teacher_id} | {self.author}"


# Stores a waiting list the exiting student fetching from Student model
class ExistingStudent(models.Model):
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    student_id = models.CharField(max_length=30, blank=True, null=True)
    preferred_course = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    preferred_level = models.CharField(max_length=30)
    preferred_days = models.CharField(max_length=30)
    preferred_time = models.CharField(max_length=30)
    last_payment = models.ForeignKey(
        'Payments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='last_payment_for_existing_student',
        help_text='Last payment made by the student',
    )
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student_id}"

class CorporateTax(models.Model):
    bills = models.CharField(max_length=50, blank=True, null=True)
    plastic = models.CharField(max_length=50, blank=True, null=True)
    avans = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.bills} | {self.plastic} | {self.avans}"

class Branch(models.Model):
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    rooms = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.address} | {self.phone_number}"


class Attendance(models.Model):
    students = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group_id = models.CharField(max_length=50)
    group_subject = models.CharField(max_length=100)
    group_level = models.CharField(max_length=150)
    teacher_id = models.CharField(max_length=50)
    teacher_first_name = models.CharField(max_length=40)
    teacher_last_name = models.CharField(max_length=40)
    lesson_topic = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.group_subject} {self.teacher_first_name} {self.created_at}"