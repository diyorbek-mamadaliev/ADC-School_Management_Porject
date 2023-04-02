from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    # Login Page
    path('', views.LOGIN, name='login'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    # Profile page url
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),

    #This is HOD home panel Url
    path('Hod/Home', Hod_Views.HOME, name='hod_home'),
    path('Hod/Student/Add', Hod_Views.ADD_STUDENT, name="add_student"),
    path('Hod/Student/View', Hod_Views.VIEW_STUDENT, name="view_student"),
    path('Hod/Student/Edit<str:id>', Hod_Views.EDIT_STUDENT, name="edit_student"),
    path('Hod/Student/Update', Hod_Views.UPDATE_STUDENT, name="update_student"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
