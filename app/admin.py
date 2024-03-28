from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UserModel(UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['subject', 'level', 'branch', 'status', 'teacher_id']
admin.site.register(customUser, UserModel)
@admin.register(Student)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['admin_first_name', 'admin_last_name', 'preferred_course', 'preferred_level', 'mobile', 'course_id', 'status']

    def admin_first_name(self, obj):
        return obj.admin.first_name

    def admin_last_name(self, obj):
        return obj.admin.last_name
@admin.register(Staff)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['admin_first_name', 'admin_last_name', 'department', 'role', 'branch', 'address', 'mobile', 'status']
    def admin_first_name(self, obj):
        return obj.admin.first_name

    def admin_last_name(self, obj):
        return obj.admin.last_name
@admin.register(Payments)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'group_id', 'payment_type', 'student_id', 'teacher_id', 'fee_amount', 'author', 'created_at']
@admin.register(Branch)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number', 'rooms']
@admin.register(Book)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'author', 'published_date']

class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_archived') # fields to display in the list

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_archived=True)