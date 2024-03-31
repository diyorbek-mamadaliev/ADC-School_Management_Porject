from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import DateFieldListFilter


# Register your models here.

class DateRangeFilter(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.links += ((('Any date'), {}),)
class UserModel(UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['first_name', 'last_name', 'username', 'email']
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['subject', 'level', 'branch', 'status', 'teacher_id']
    list_filter = ['subject', 'level', 'branch', 'status', 'teacher_id']
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
    list_filter = ['department', 'role', 'branch', 'status']
    def admin_first_name(self, obj):
        return obj.admin.first_name

    def admin_last_name(self, obj):
        return obj.admin.last_name
@admin.register(Payments)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'group_id', 'payment_type', 'student_id', 'teacher_id', 'fee_amount', 'author', 'created_at']
    list_filter = [('created_at', DateRangeFilter), 'first_name', 'last_name', 'student_id', 'author']
@admin.register(Branch)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number', 'rooms']

@admin.register(PriceList)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'course_level', 'price']
@admin.register(Book)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'author', 'published_date']
    list_filter = ['book_name', 'author']

class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_archived') # fields to display in the list

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_archived=True)