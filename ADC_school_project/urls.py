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
    path('Hod/Finance/Pricelist', Hod_Views.PRICE_LIST, name="price_list"),
    path('Hod/Welcome', Hod_Views.WELCOME, name="welcome"),
    path('Hod/Branch/', Hod_Views.VIEW_BRANCH, name="view_branch"),
    path('Hod/Library/Books/New', Hod_Views.ADD_BOOK, name="add_book"),
    path('Hod/Library/Member/New', Hod_Views.ADD_NEW_MEMBER, name="add_new_member"),
    path('Hod/Library/Member/View', Hod_Views.VIEW_LIBRARY_MEMBERS, name="view_library_members"),
    path('Hod/Library/Books', Hod_Views.VIEW_BOOKS, name="view_books"),
    path('Hod/Library/Books/Register/<str:id>', Hod_Views.REGISTER_BOOK, name="register_book"),
    path('Hod/Library/Book/Update', Hod_Views.UPDATE_BOOK, name="update_book"),
    path('Hod/Library/Books/Given', Hod_Views.VIEW_GIVEN_BOOKS, name="view_given_books"),
    path('Hod/Branches/<str:id>', Hod_Views.VIEW_BRANCHES, name="view_branches"),
    path('Hod/Branch/Edit/<str:id>', Hod_Views.EDIT_BRANCH, name="edit_branch"),
    path('Hod/Branch/Update', Hod_Views.UPDATE_BRANCH, name="update_branch"),
    path('Hod/Attendance/Day/<str:id>', Hod_Views.VIEW_ATTENDANCE_DAY, name="view_attendance_day"),
    path('Hod/Attendance/Edit/<str:id>', Hod_Views.EDIT_ATTENDANCE, name="edit_attendance"),
    path('Hod/Attendance/Update', Hod_Views.UPDATE_ATTENDANCE, name="update_attendance"),
    path('Hod/Attendance/View/<str:id>', Hod_Views.VIEW_ATTENDANCE, name="view_attendance"),
    path('Hod/Attendance/New/<str:id>', Hod_Views.ADD_ATTENDANCE, name="add_attendance"),
    path('Hod/Branch/Add', Hod_Views.ADD_BRANCH, name="add_branch"),
    path('Hod/Student/Add', Hod_Views.ADD_STUDENT, name="add_student"),
    path('Hod/Student/View', Hod_Views.VIEW_STUDENT, name="view_student"),
    path('Hod/Student/Edit/<str:id>', Hod_Views.EDIT_STUDENT, name="edit_student"),
    path('Hod/Student/Update', Hod_Views.UPDATE_STUDENT, name="update_student"),
    path('Hod/Student/Waiting', Hod_Views.VIEW_WAITING, name="view_waiting"),
    path('Hod/Student/Archive', Hod_Views.ARCHIVE_STUDENT, name="archive_student"),
    path('Hod/Student/WaitingForm', Hod_Views.WAITING_FORM, name="waiting_form"),
    path('Hod/Student/WaitingView', Hod_Views.VIEW_WAITLIST, name="view_waitlist"),
    path('Hod/Student/ExistingWait/<str:id>', Hod_Views.EXISTING_WAIT, name="existing_wait"),
    path('Hod/Student/ViewExistingWaitlist', Hod_Views.VIEW_EXISTING, name="view_existing"),
    path('Hod/Student/EditExisting/<str:id>', Hod_Views.EDIT_EXISTING, name="edit_existing"),
    path('Hod/Student/UpdateExisting', Hod_Views.UPDATE_EXISTING, name="update_existing"),

    path('Hod/Course/Add', Hod_Views.ADD_COURSE, name="add_course"),
    path('Hod/Course/View', Hod_Views.VIEW_COURSE, name="view_course"),
    path('Hod/Course/Gallery', Hod_Views.VIEW_COURSES, name='view_courses'),
    path('Hod/Course/Edit/<str:id>', Hod_Views.EDIT_COURSE, name="edit_course"),
    path('Hod/Course/Update', Hod_Views.UPDATE_COURSE, name="update_course"),
    path('Hod/Course/Archive', Hod_Views.ARCHIVE_COURSE, name="archive_course"),
    path('Hod/Payments/Fee/<str:id>', Hod_Views.ADD_FEE, name="add_fee"),
    path('Hod/Payments/FeeExisting/<str:id>', Hod_Views.ADD_FEE_EXISTING, name="add_fee_existing"),
    path('Hod/Payments/History', Hod_Views.VIEW_PAYMENT_HISTORY, name="view_payment_history"),
    path('Hod/Payments/Preview', Hod_Views.PAYMENT_PREVIEW, name="payment_preview"),
    path('download-csv/', Hod_Views.DOWNLOAD_CSV, name='download_csv'),
    # path('Hod/Payments/Add', Hod_Views.ADD_NEW_PAYMENT, name="add_name_payment"),

    path('Hod/Staff/Add', Hod_Views.ADD_STAFF, name="add_staff"),
    path('Hod/Staff/View', Hod_Views.VIEW_STAFF, name="view_staff"),
    path('Hod/Staff/Teacher', Hod_Views.VIEW_TEACHER, name='view_teacher'),
    path('Hod/Staff/Student/<str:id>', Hod_Views.VIEW_STUDENTS, name='view_students'),
    path('Hod/Staff/Edit/<str:id>', Hod_Views.EDIT_STAFF, name="edit_staff"),
    path('Hod/Staff/Update', Hod_Views.UPDATE_STAFF, name="update_staff"),
    path('Hod/Staff/Salary/Fixed', Hod_Views.VIEW_FIXED_SALARY, name="view_fixed_salary"),
    path('Hod/Staff/Salary', Hod_Views.STAFF_SALARY, name="staff_salary"),
    path('Hod/Staff/Archived', Hod_Views.ARCHIVE_STAFF, name="archive_staff"),
    path('Hod/Staff/TeacherPanel', Hod_Views.TEACHER_PANEL, name="teacher_panel"),
    path('Hod/Staff/TeacherGroup', Hod_Views.TEACHER_GROUP_PANEL, name="teacher_group_panel"),
    path('Hod/Staff/viewexisttax', Hod_Views.VIEW_EXISTTAX, name="view_existtax"),
    # path('Hod/edit-corporatetax/<str:id>/', Hod_Views.EDIT_CORPORATETAX, name='edit_corporatetax'),
    # path('Hod/update-corporatetax/<str:id>/', Hod_Views.UPDATE_CORPORATETAX, name='update_corporatetax'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
