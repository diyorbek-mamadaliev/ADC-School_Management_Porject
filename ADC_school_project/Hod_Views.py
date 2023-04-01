from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, customUser, Student, ArchivedUser
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

@login_required(login_url='/')
def HOME(request):
    return render(request, 'Hod/home.html')

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()

    if request.method == "POST":
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

        if customUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username exists in a database')
        else:
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

@login_required(login_url='/')
def VIEW_STUDENT(request):
    # student = Student.objects.all()
    student = customUser.objects.filter(is_staff=False, is_superuser=False, is_archived=False)

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

def archive_student(request, admin):
    student = customUser.objects.get(id=admin)
    student.is_archived = True
    student.save()
    return redirect('view_student')


def unarchive_user(request, pk):
    archived_user = get_object_or_404(ArchivedUser, pk=pk)
    user = archived_user.user
    user.is_active = True
    user.save()
    archived_user.delete()
    return redirect('archived_users')


