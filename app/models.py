from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.

class customUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic',blank=True, null=True)

# Courses Model
class Course(models.Model):
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    #this will display the subject info in the list within admin panel
    def __str__(self):
        return '{}'.format(self.subject + " | " + self.level)

class Student(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)
    mobiletwo = models.CharField(max_length=14)
    address = models.CharField(max_length=150)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.admin.first_name + " " + self.admin.last_name)



