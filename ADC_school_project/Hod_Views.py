from django.db.models.functions import Now
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Course, customUser, Student, Staff, Payments
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Max, Count
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, date
from decimal import Decimal



@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    student_counted = Student.objects.all().count()
    group_count = Course.objects.all().count()
    payment_count = Payments.objects.all().count()
    teacher_count = Staff.objects.filter(department='Teacher').count()
    staff_list = Staff.objects.filter(department='Teacher')

    course_with_student_counts = (
        Course.objects.filter(student__status='Active')
        .values('subject')
        .annotate(student_count=Count('student'))
    )

    context = {
        'student': student_count,
        'student_count': student_counted,
        'groups': group_count,
        'payments': payment_count,
        'teachers': teacher_count,
        'staff_list': staff_list,
        'course_with_student_counts': course_with_student_counts
    }

    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    last_username_number = customUser.objects.aggregate(Max('username'))['username__max']
    next_username_number = 1 if last_username_number is None or not last_username_number.split('_')[
        -1].isdigit() else int(last_username_number.split('_')[-1]) + 1

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = f"{first_name.capitalize()}_{next_username_number}"
        password = '111'  # Set password to '111'
        address = request.POST.get('address')
        birth_date = request.POST.get('date_of_birth')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobile_two')
        course_id = request.POST.get('course_id')
        student_status = request.POST.get('status')

        user = customUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            profile_pic=profile_pic,
            user_type=3
        )
        user.set_password(password)
        user.save()

        course = Course.objects.get(id=course_id)

        student = Student(
            admin=user,
            mobile=mobile,
            mobiletwo=mobiletwo,
            address=address,
            birth_date=birth_date,
            course_id=course,
            status=student_status,
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
    student = Student.objects.filter(status='Active')

    context = {
        'student': student,
    }
    return render(request, 'Hod/view_student.html', context)


@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    context = {
        'student': student,
        'course': course,
    }
    return render(request, 'Hod/edit_student.html', context)

@login_required(login_url='/')
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
        student_status = request.POST.get('status')

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
        student.status = student_status

        course = Course.objects.get(id=course_id)
        student.course_id = course

        student.save()
        messages.success(request, "Ma'lumot Yangilandi")
        return redirect('view_student')
    return render(request, 'Hod/edit_student.html')


# def DELETE_STUDENT(request, admin):
#     student = customUser.objects.get(id=admin)
#     student.delete()
#     messages.success(request, "O'chrilidi")
#     return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    last_username_number = Course.objects.aggregate(Max('username'))['username__max']
    next_username_number = 1 if last_username_number is None or not last_username_number.split('_')[-1].isdigit() else int(last_username_number.split('_')[-1]) + 1
    if request.method == "POST":
        course_name = request.POST.get('subject')
        course_level = request.POST.get('level')
        username = f"{course_name.capitalize()}_{next_username_number}"
        course_status = request.POST.get('status')
        branch = request.POST.get('branch')
        teacher_id = request.POST.get('teacher_id')
        teacher = Staff.objects.get(id=teacher_id)

        course = Course(
            subject=course_name,
            username=username,
            status=course_status,
            level=course_level,
            teacher_id=teacher,
            branch=branch
        )
        course.save()
        messages.success(request, "Yangi Gruppa Qo'shildi")
        return redirect('add_course')
    staff = Staff.objects.all()
    context = {'staff': staff}

    return render(request, 'Hod/add_course.html', context)



# def ADD_COURSE(request):
#     if request.method == "POST":
#         course_name = request.POST.get('subject')
#         course_level = request.POST.get('level')
#         course_ind = request.POST.get('indexing')
#         course = Course(
#             subject=course_name,
#             level=course_level,
#             indexing=course_ind,
#         )
#         course.save()
#         messages.success(request, "Yangi Gruppa Qo'shildi")
#         return redirect('add_course')
#
#     return render(request, 'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.exclude(status="Archived")
    context = {
        'course': course,
    }
    return render(request, 'Hod/view_course.html', context)


@login_required(login_url='/')
def VIEW_COURSES(request):
    courses = Course.objects.exclude(status='Archived').values('subject').distinct()
    context = {
        'courses': courses,
    }

    return render(request, 'Hod/view_courses.html', context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id=id)
    staff = Staff.objects.all()
    context = {
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/edit_course.html', context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        branch = request.POST.get('branch')
        course_id = request.POST.get('course_id')
        course_status = request.POST.get('status')
        teacher_id = request.POST.get('teacher_id')
        course = Course.objects.get(id=course_id)

        staff = Staff.objects.get(id=teacher_id)


        course.subject = subject
        course.level = level
        course.branch = branch
        course.status = course_status
        course.teacher_id = staff
        course.save()

        messages.success(request, "Muvaffaqiyatli O'zgartirildi")
        return redirect('view_course')

    return render(request, 'Hod/edit_course.html')

@login_required(login_url='/')
def ADD_STAFF(request):
    last_username_number = customUser.objects.aggregate(Max('username'))['username__max']
    next_username_number = 1 if last_username_number is None or not last_username_number.split('_')[
        -1].isdigit() else int(last_username_number.split('_')[-1]) + 1
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = f"{first_name.capitalize()}_{next_username_number}"
        department = request.POST.get('department')
        role = request.POST.get('role')
        branch = request.POST.get('branch')
        salary_type = request.POST.get('salary_type')
        salary_amount = request.POST.get('salary_amount')
        work_format = request.POST.get('work_format')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobiletwo')
        password = request.POST.get('password')

        user = customUser(first_name=first_name,
                          last_name=last_name,
                          username=username,
                          user_type=2)
        user.set_password(password)
        user.save()

        staff = Staff(admin=user,
                      department=department,
                      role=role,
                      salary_type=salary_type,
                      salary_amount=salary_amount,
                      work_format=work_format,
                      branch=branch,
                      birth_date=birth_date,
                      address=address,
                      mobile=mobile,
                      mobiletwo=mobiletwo)
        staff.save()
        messages.success(request, "Hodim Kiritildi")
        return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.get(id=id)

    context = {
        'staff': staff,
    }
    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        department = request.POST.get('department')
        role = request.POST.get('role')
        salary_type = request.POST.get('salary_type')
        salary_amount = request.POST.get('salary_amount')
        work_format = request.POST.get('work_format')
        branch = request.POST.get('branch')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobiletwo')
        password = request.POST.get('password')

        user = customUser.objects.get(id = staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        if password != None and password != "":
            user.set_password(password)
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.department = department
        staff.role = role
        staff.salary_type = salary_type
        staff.salary_amount = salary_amount
        staff.work_format = work_format
        staff.birth_date = birth_date
        staff.branch = branch
        staff.address = address
        staff.mobile = mobile
        staff.mobiletwo = mobiletwo

        staff.save()
        messages.success(request, "Ma'lumot O'zgartirildi")
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def VIEW_WAITING(request):
    student = Student.objects.filter(status='Waiting')

    context = {
        'student': student,
    }
    return render(request, 'Hod/view_waiting.html', context)


@login_required(login_url='/')
def ARCHIVE_STUDENT(request):
    student = Student.objects.filter(status='Archived')

    context = {
        'student': student,
    }
    return render(request, 'Hod/archive_student.html', context)

@login_required(login_url='/')
def VIEW_TEACHER(request):
    staff = Staff.objects.filter(department='Teacher')
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_teacher.html', context)

@login_required(login_url='/')
def VIEW_STUDENTS(request, id):
    course = Course.objects.get(id=id)
    student = Student.objects.filter(course_id=id)
    context = {
        'course': course,
        'student': student,
    }
    return render(request, 'Hod/view_students.html', context)

@login_required(login_url='/')
def ADD_FEE(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group_id = request.POST.get('group_id')
        student_id = request.POST.get('student_id')
        payment_type = request.POST.get('payment_type')
        teacher_id = request.POST.get('teacher_id')
        comment = request.POST.get('comment')
        fee_amount = request.POST.get('fee_amount')
        author = request.user
        payment = Payments(
            first_name=first_name,
            last_name=last_name,
            group_id=group_id,
            teacher_id=teacher_id,
            comment=comment,
            student_id=student_id,
            payment_type=payment_type,
            fee_amount=fee_amount,
            author=author
        )
        payment.save()
        return redirect('view_payment_history')
    else:
        context = {
            'course': course,
            'student': student,
        }
    return render(request, 'Hod/add_fee.html', context)

    # if request.method == 'POST':
    #     # get the user object for the current user
    #     author = request.user
    #     # create a new fee object with the form data and author set to the current user
    #     fee = ADD_FEE(student=student, author=author, **request.POST)
    #     fee.save()
    #     return redirect('fee_detail', fee.id)

@login_required(login_url='/')
def VIEW_PAYMENT_HISTORY(request):
    payments = Payments.objects.all()

    context = {
        'payments': payments,
    }
    return render(request, 'Hod/payment_history.html', context)

# def ADD_NEW_PAYMENT(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         group_id = request.POST.get('group_id')
#         student_id = request.POST.get('student_id')
#         teacher_id = request.POST.get('teacher_id')
#         comment = request.POST.get('comment')
#         fee_amount = request.POST.get('fee_amount')
#         author = request.user  # current logged in user
#         payment = Payments(first_name=first_name, last_name=last_name, group_id=group_id,
#                            student_id=student_id, teacher_id=teacher_id, comment=comment,
#                            fee_amount=fee_amount, author=author)
#         payment.save()
#         return redirect('view_payment_history')
#     else:
#         return render(request, 'Hod/add_fee.html')

# def ADD_NEW_PAYMENT(request):
#     if request.method == 'POST':
#         # Process form data and save new payment record
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         group_id = request.POST.get('group_id')
#         student_id = request.POST.get('student_id')
#         teacher_id = request.POST.get('teacher_id')
#         fee_amount = request.POST.get('fee_amount')
#         comments = request.POST.get('comments')
#         author = request.user
#         payment = Payments.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             group_id=group_id,
#             student_id=student_id,
#             teacher_id=teacher_id,
#             fee_amount=fee_amount,
#             comments=comments,
#             author=author
#         )
#         return redirect('Hod/payment_history')
#
from decimal import Decimal

def STAFF_SALARY(request):
    teachers = Staff.objects.filter(department='Teacher')

    # Calculate total fees for each teacher by summing up all fees created by them
    current_month = datetime.now().month
    fees = Payments.objects.filter(
        teacher_id__in=[teacher.admin.username for teacher in teachers],
        created_at__month=current_month
    ).values('teacher_id').annotate(total_fees=Sum('fee_amount'))

    # Calculate total fees across all teachers
    total_fees = sum([fee['total_fees'] for fee in fees])

    # Calculate 39% of the total fees for each teacher and add it to the teacher_fees list
    teacher_fees = []
    for fee in fees:
        teacher = Staff.objects.get(admin__username=fee['teacher_id'])
        teacher_total_fees = fee['total_fees']
        teacher_commission = Decimal('0.39') * teacher_total_fees
        administrator_bonus = Decimal('0.01') * teacher_total_fees
        teacher_fees.append({
            'first_name': teacher.admin.first_name,
            'last_name': teacher.admin.last_name,
            'department': teacher.department,
            'total_fees': teacher_total_fees,
            'commission': teacher_commission,
            'bonus': administrator_bonus,
        })

    context = {
        'teacher_fees': teacher_fees,
        'total_fees': total_fees,
    }

    return render(request, 'Hod/view_salary.html', context)


