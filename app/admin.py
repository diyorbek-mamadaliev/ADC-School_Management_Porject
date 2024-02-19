from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UserModel(UserAdmin):
    list_display = ['username', 'user_type']
admin.site.register(customUser, UserModel)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Payments)
admin.site.register(ExistingStudent)
admin.site.register(CorporateTax)
admin.site.register(Branch)

class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_archived') # fields to display in the list

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_archived=True)