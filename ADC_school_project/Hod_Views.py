from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, customUser, Student
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Max

@login_required(login_url='/')
def HOME(request):
    return render(request, 'Hod/home.html')

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    last_username_number = customUser.objects.aggregate(Max('username'))['username__max']
    next_username_number = 1 if last_username_number is None or not last_username_number.split('_')[
        -1].isdigit() else int(last_username_number.split('_')[-1]) + 1

    # next_username_number = 2 if last_username_number is None else int(last_username_number.split('_')[-1]) + 1

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = f"{first_name.lower()}_{next_username_number}"
        password = request.POST.get('password')
        address = request.POST.get('address')
        birth_date = request.POST.get('date_of_birth')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobile_two')
        course_id = request.POST.get('course_id')

        user = customUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            profile_pic=profile_pic,
            user_type=3
        )
        user.set_password(password)
        user.save()

        course = Course.objects.get(id = course_id)

        student = Student(
            admin=user,
            mobile=mobile,
            mobiletwo=mobiletwo,
            address=address,
            birth_date=birth_date,
            course_id=course,
        )
        student.save()

        messages.success(request,  user.first_name + ' ' + user.last_name + ' Saved Successfully')
        return redirect('add_student')

    context = {
        'course': course,
    }
    return render(request, 'Hod/add_student.html', context)

# def ADD_STUDENT(request):
#     course = Course.objects.all()
#
#     if request.method == "POST":
#         profile_pic = request.FILES.get('profile_pic')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         address = request.POST.get('address')
#         birth_date = request.POST.get('date_of_birth')
#         mobile = request.POST.get('mobile')
#         mobiletwo = request.POST.get('mobile_two')
#         course_id = request.POST.get('course_id')
#
#         if customUser.objects.filter(username=username).exists():
#             messages.warning(request, 'Username exists in a database')
#         else:
#             user = customUser(
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 profile_pic=profile_pic,
#                 user_type=3
#             )
#             user.set_password(password)
#             user.save()
#
#             course = Course.objects.get(id = course_id)
#
#             student = Student(
#                 admin=user,
#                 mobile=mobile,
#                 mobiletwo=mobiletwo,
#                 address=address,
#                 birth_date=birth_date,
#                 course_id=course,
#             )
#             student.save()
#             messages.success(request,  user.first_name + ' ' + user.last_name + ' Saved Successfully')
#             return redirect('add_student')
#     context = {
#         'course': course,
#     }
#     return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.exclude(course_id__level='Students')

    context = {
        'student': student,
    }
    return render(request, 'Hod/view_student.html', context)


def EDIT_STUDENT(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    context = {
        'student': student,
        'course': course,
    }
    return render(request, 'Hod/edit_student.html', context)


def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        birth_date = request.POST.get('date_of_birth')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobile_two')
        course_id = request.POST.get('course_id')

        user = customUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        if username != None and password != "":
            user.username = username
        if password != None and password != "":
            user.set_password(password)
        user.save()

        student = Student.objects.get(admin=student_id)
        student.address = address
        student.birth_date = birth_date
        student.mobile = mobile
        student.mobiletwo = mobiletwo
        course = Course.objects.get(id=course_id)
        student.course_id=course
        student.save()
        messages.success(request, "Ma'lumot Yangilandi")
        return redirect('view_student')
    return render(request, 'Hod/edit_student.html')


# def DELETE_STUDENT(request, admin):
#     student = customUser.objects.get(id=admin)
#     student.delete()
#     messages.success(request, "O'chrilidi")
#     return redirect('view_student')




