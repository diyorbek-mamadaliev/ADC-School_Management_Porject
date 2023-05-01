from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User




# Create your models here.

class customUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic',blank=True, null=True)


class Staff(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    salary_type = models.CharField(max_length=30)
    work_format = models.CharField(max_length=30)
    salary_amount = models.CharField(max_length=30)
    birth_date = models.DateTimeField(blank=True, null=True)
    address = models.TextField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    mobiletwo = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin.username


class Course(models.Model):
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=150)
    username = models.CharField(max_length=50, blank=True, null=True)
    teacher_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated

    # This will display the subject info in the list within admin panel
    def __str__(self):
        return '{}'.format(self.subject + " | " + self.level)


class Student(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)
    mobiletwo = models.CharField(max_length=14)
    preferred_course = models.CharField(max_length=30, blank=True, null=True)
    preferred_level = models.CharField(max_length=30, blank=True, null=True)
    preferred_days = models.CharField(max_length=30, blank=True, null=True)
    preferred_time = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)
    birth_date = models.DateTimeField()
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.admin.first_name + " " + self.admin.last_name)

class Payments(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    group_id = models.CharField(max_length=70)
    student_id = models.CharField(max_length=50)
    teacher_id = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"