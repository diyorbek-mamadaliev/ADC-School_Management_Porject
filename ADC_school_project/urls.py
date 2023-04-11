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
    path('Hod/Student/Waiting', Hod_Views.VIEW_WAITING, name="view_waiting"),
    path('Hod/Student/Archive', Hod_Views.ARCHIVE_STUDENT, name="archive_student"),

    path('Hod/Course/Add', Hod_Views.ADD_COURSE, name="add_course"),
    path('Hod/Course/View', Hod_Views.VIEW_COURSE, name="view_course"),
    path('Hod/Course/Gallery', Hod_Views.VIEW_COURSES, name='view_courses'),
    path('Hod/Course/Edit/<str:id>', Hod_Views.EDIT_COURSE, name="edit_course"),
    path('Hod/Course/Update', Hod_Views.UPDATE_COURSE, name="update_course"),

    path('Hod/Staff/Add', Hod_Views.ADD_STAFF, name="add_staff"),
    path('Hod/Staff/View', Hod_Views.VIEW_STAFF, name="view_staff"),
    path('Hod/Staff/Edit/<str:id>', Hod_Views.EDIT_STAFF, name="edit_staff"),
    path('Hod/Staff/Update', Hod_Views.UPDATE_STAFF, name="update_staff"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
