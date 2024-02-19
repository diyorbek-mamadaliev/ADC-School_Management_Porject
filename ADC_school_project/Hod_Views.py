from django.db.models.functions import Now
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Course, customUser, Student, Staff, Payments, ExistingStudent, CorporateTax, Branch
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Max, Count, Q
import datetime
from datetime import datetime
from decimal import Decimal
from django.db.models import Sum
import csv
from django.http import HttpResponse
from app.models import Payments




@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    waiting_count = Student.objects.all()
    existing_waiting = ExistingStudent.objects.all()
    student_counted = Student.objects.filter(status='Active').exclude(course_id__username='Not_Selected_1').count()
    group_count = Course.objects.exclude(username='Not_Selected_1').filter(status='Active').count()
    payment_count = Payments.objects.all().count()
    teacher_count = Staff.objects.filter(department='Teacher').count()
    staff_list = Staff.objects.filter(department='Teacher')

    course_with_student_counts = (
        Course.objects.filter(student__status='Active').exclude(username='Not_Selected_1')
        .values('subject')
        .annotate(student_count=Count('student'))
    )
    course_with_waiting_counts = (
        Student.objects.filter(status='Waiting')
        .values('preferred_course')
        .annotate(waiting_count=Count('id'))
    )
    course_with_existing_counts = (
        ExistingStudent.objects.filter(status='Waiting')
        .values('preferred_course')
        .annotate(existing_waiting=Count('id'))
    )

    context = {
        'student': student_count,
        'student_count': student_counted,
        'groups': group_count,
        'payments': payment_count,
        'teachers': teacher_count,
        'staff_list': staff_list,
        'course_with_student_counts': course_with_student_counts,
        'course_with_waiting_counts': course_with_waiting_counts,
        'course_with_existing_counts': course_with_existing_counts
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
        username = f"{first_name.lower()}_{next_username_number}"
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
        return redirect('view_waitlist')

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
    existing = ExistingStudent.objects.filter(status='Active')

    context = {
        'student': student,
        'existing': existing
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


def WAITING_FORM(request):
    course = Course.objects.all()
    last_username_number = customUser.objects.aggregate(Max('username'))['username__max']
    next_username_number = 1 if last_username_number is None or not last_username_number.split('_')[
        -1].isdigit() else int(last_username_number.split('_')[-1]) + 1

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = f"{first_name.lower()}_{next_username_number}"
        password = '111'  # Set password to '111'
        address = request.POST.get('address')
        birth_date = request.POST.get('date_of_birth')
        mobile = request.POST.get('mobile')
        mobiletwo = request.POST.get('mobile_two')
        course_id = request.POST.get('course_id')
        student_status = request.POST.get('status')
        preferred_course = request.POST.get('preferred_course')  # new field
        preferred_level = request.POST.get('preferred_level')  # new field
        preferred_time = request.POST.get('preferred_time')  # new field
        preferred_days = request.POST.get('preferred_days')  # new field

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
            preferred_course=preferred_course,  # new field
            preferred_level=preferred_level,  # new field
            preferred_time=preferred_time,  # new field
            preferred_days=preferred_days,  # new field
        )
        student.save()

        messages.success(request, user.first_name + ' ' + user.last_name + ' Saved Successfully')
        return redirect('view_waitlist')

    context = {
        'course': course,
    }
    return render(request, 'Hod/waiting_form.html', context)

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
        username = f"{course_name.lower()}_{next_username_number}"
        course_status = request.POST.get('status')
        days = request.POST.get('days')
        hours = request.POST.get('hours')
        branch_name = request.POST.get('branch_name')
        branch = Branch.objects.get(name=branch_name)
        teacher_id = request.POST.get('teacher_id')
        teacher = Staff.objects.get(id=teacher_id)

        course = Course(
            subject=course_name,
            username=username,
            status=course_status,
            level=course_level,
            teacher_id=teacher,
            days=days,
            hours=hours,
            branch_name=branch
        )
        course.save()
        messages.success(request, "Yangi Gruppa Qo'shildi")
        return redirect('add_course')
    staff = Staff.objects.all()
    branch = Branch.objects.all()
    context = {'staff': staff, 'branch' : branch}

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
    course = Course.objects.exclude(status="Archived").exclude(username='Not_Selected_1')
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
        days = request.POST.get('days')
        hours = request.POST.get('hours')
        course_status = request.POST.get('status')
        teacher_id = request.POST.get('teacher_id')
        course = Course.objects.get(id=course_id)

        staff = Staff.objects.get(id=teacher_id)


        course.subject = subject
        course.level = level
        course.branch = branch
        course.days = days
        course.hours = hours
        course.status = course_status
        course.teacher_id = staff
        course.save()

        messages.success(request, "Updated Successfully")
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
        username = f"{first_name.lower()}_{next_username_number}"
        department = request.POST.get('department')
        role = request.POST.get('role')
        branch_name = request.POST.get('branch_name')
        branch = Branch.objects.get(name=branch_name)
        salary_type = request.POST.get('salary_type')
        status = request.POST.get('status')
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
                          user_type=1)
        user.set_password(password)
        user.save()

        staff = Staff(admin=user,
                      department=department,
                      role=role,
                      salary_type=salary_type,
                      salary_amount=salary_amount,
                      work_format=work_format,
                      branch_name=branch,
                      status=status,
                      birth_date=birth_date,
                      address=address,
                      mobile=mobile,
                      mobiletwo=mobiletwo)
        staff.save()
        messages.success(request, "Hodim Kiritildi")
        return redirect('add_staff')
    branch = Branch.objects.all()
    context = {'branch': branch}

    return render(request, 'Hod/add_staff.html', context)

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.exclude(status='Archived')
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
        fines = request.POST.get('fines')
        bonus = request.POST.get('bonus')
        tax = request.POST.get('tax')
        salary_type = request.POST.get('salary_type')
        salary_amount = request.POST.get('salary_amount')
        work_format = request.POST.get('work_format')
        branch = request.POST.get('branch')
        status = request.POST.get('status')
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
        staff.fines = fines
        staff.status = status
        staff.bonus = bonus
        staff.tax = tax
        staff.branch = branch
        staff.address = address
        staff.mobile = mobile
        staff.mobiletwo = mobiletwo

        staff.save()
        messages.success(request, "Updated Successfully")
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def VIEW_WAITING(request):
    student = Student.objects.filter(status='Waiting')

    context = {
        'student': student,
    }
    return render(request, 'Hod/view_waitlist.html', context)


@login_required(login_url='/')
def ARCHIVE_STUDENT(request):
    student = Student.objects.filter(status='Archived')
    existing = ExistingStudent.objects.filter(status='Archived')

    context = {
        'student': student,
        'existing': existing,
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
    now_month = datetime.now().month
    course = Course.objects.get(id=id)
    student = Student.objects.filter(course_id=id)
    payments = Payments.objects.filter(group_id=id,
                                       created_at__month=now_month,
                                       created_at__year=datetime.now().year
                                       )
    existing_students = ExistingStudent.objects.filter(course_id=id)
    context = {
        'course': course,
        'student': student,
        'payments': payments,
        'existing_students': existing_students
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
        return redirect('payment_preview')
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


def STAFF_SALARY(request):
    teachers = Staff.objects.filter(department='Teacher')

    # Calculate total fees for each teacher by summing up all fees created by them
    current_month = datetime.now().month
    fees = Payments.objects.filter(
        teacher_id__in=[teacher.admin.username for teacher in teachers],
        created_at__month=current_month
    ).values('teacher_id').annotate(
        total_fees=Sum('fee_amount'),
        total_cash=Sum('fee_amount', filter=Q(payment_type='Cash')),
        total_plastic=Sum('fee_amount', filter=Q(payment_type='Plastic'))
    )

    # Calculate total fees across all teachers
    total_fees = sum([fee['total_fees'] for fee in fees])

    # Calculate commission, bonus, fines, teacher_bonus, and tax for each teacher based on their total fees
    teacher_fees = []
    for fee in fees:
        teacher = Staff.objects.get(admin__username=fee['teacher_id'])
        teacher_total_fees = fee['total_fees']
        teacher_total_cash = fee['total_cash']
        teacher_total_plastic = fee['total_plastic']
        teacher_commission = Decimal('0.39') * teacher_total_fees
        administrator_bonus = Decimal('0.01') * teacher_commission  # Calculate bonus based on teacher_commission
        teacher_fine = teacher.fines  # Get the fines for the teacher from the 'Staff' model's 'fines' column
        teacher_bonus = teacher.bonus  # Get the teacher_bonus for the teacher from the 'Staff' model's 'bonus' column
        teacher_tax = teacher.tax  # Get the tax for the teacher from the 'Staff' model's 'tax' column
        teacher_fees.append({
            'first_name': teacher.admin.first_name,
            'last_name': teacher.admin.last_name,
            'department': teacher.department,
            'total_fees': teacher_total_fees,
            'total_cash': teacher_total_cash,
            'total_plastic': teacher_total_plastic,
            'commission': teacher_commission,
            'bonus': administrator_bonus,
            'fines': teacher_fine,  # Include the fines in the dictionary
            'teacher_bonus': teacher_bonus,  # Include the teacher_bonus in the dictionary
            'tax': teacher_tax,  # Include the tax in the dictionary
        })

    context = {
        'teacher_fees': teacher_fees,
        'total_fees': total_fees,
    }

    return render(request, 'Hod/view_salary.html', context)





def VIEW_WAITLIST(request):
    student = Student.objects.filter(status='Waiting')

    context = {
        'student': student,
    }
    return render(request, 'Hod/view_waitlist.html', context)


def EXISTING_WAIT(request, id):
    student = Student.objects.filter(id=id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        preferred_course = request.POST.get('preferred_course')
        preferred_level = request.POST.get('preferred_level')
        preferred_time = request.POST.get('preferred_time')
        preferred_days = request.POST.get('preferred_days')
        mobile = request.POST.get('mobile')
        status = request.POST.get('status')
        student_id = request.POST.get('student_id')
        existing = ExistingStudent(
            student_id=student_id,
            preferred_course=preferred_course,
            preferred_level=preferred_level,
            preferred_days=preferred_days,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            status=status,
            preferred_time=preferred_time
        )
        existing.save()
        return redirect('view_waitlist')
    else:
        context = {
            'student': student,
        }
    return render(request, 'Hod/waiting_form_existing.html', context)


def VIEW_EXISTING(request):
    existstudent = ExistingStudent.objects.filter(status='Waiting')
    context = {
        'existstudent': existstudent
    }
    return render(request, 'Hod/view_existwaitlist.html', context)


def EDIT_EXISTING(request, id):
    existing = ExistingStudent.objects.get(id=id)
    course = Course.objects.all()

    context = {
        'existing': existing,
        'course': course
    }
    return render(request, 'Hod/edit_waiting_form_existing.html', context)


def UPDATE_EXISTING(request):
    if request.method == "POST":
        first_name = request.POST.get('full_name')
        last_name = request.POST.get('last_name')
        preferred_course = request.POST.get('preferred_course')
        preferred_level = request.POST.get('preferred_level')
        preferred_time = request.POST.get('preferred_time')
        student_id = request.POST.get('student_id')
        existing_id = request.POST.get('id')
        preferred_days = request.POST.get('preferred_days')
        course_id = request.POST.get('course_id')
        status = request.POST.get('status')

        existing = ExistingStudent.objects.get(id=existing_id)
        course = Course.objects.get(id=course_id)
        existing.course_id = course
        existing.frst_name = first_name
        existing.last_name = last_name
        existing.preferred_course = preferred_course
        existing.preferred_level = preferred_level
        existing.preferred_days = preferred_days
        existing.student_id = student_id
        existing.preferred_time = preferred_time
        existing.status = status

        existing.save()

        messages.success(request, "Updated Successfully")
        return redirect('view_student')

    return render(request, 'Hod/edit_waiting_form_existing.html')


def ARCHIVE_STAFF(request):
    staff = Staff.objects.filter(status='Archived')

    context = {
        'staff': staff,
    }
    return render(request, 'Hod/archive_staff.html', context)


def ARCHIVE_COURSE(request):
    course = Course.objects.filter(status='Archived')

    context = {
        'course': course,
    }
    return render(request, 'Hod/archive_course.html', context)


def TEACHER_PANEL(request):
    now_month = datetime.now().month
    payments = Payments.objects.filter(
        teacher_id=request.user.username,
        created_at__month=now_month,
        created_at__year=datetime.now().year
    )
    context = {'payments': payments}
    return render(request, 'Hod/payments_by_teacher.html', context)


def WELCOME(request):
    return render(request, 'Hod/welcome_page.html')


def PAYMENT_PREVIEW(request):
    # get the current logged-in user's username
    current_user = request.user.username

    # filter payments by the current user's username
    payment = Payments.objects.filter(author__username=current_user).order_by('-created_at').first()

    # pass payment object to template
    context = {
        'payment': payment
    }
    return render(request, 'Hod/payment_preview.html', context)


def ADD_FEE_EXISTING(request, id):
    existing = ExistingStudent.objects.filter(id=id)
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
        return redirect('payment_preview')
    else:
        context = {
            'course': course,
            'existing': existing,
        }
    return render(request, 'Hod/add_fee_existing.html', context)


def DOWNLOAD_CSV(request):
    model_data = Payments.objects.all().values()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="model_data.csv"'

    writer = csv.DictWriter(response, fieldnames=model_data[0].keys())
    writer.writeheader()
    writer.writerows(model_data)

    return response

# def EDIT_CORPORATETAX(request, id):
#     corporatetax = get_object_or_404(CorporateTax, id=id)
#     context = {
#         'corporatetax': corporatetax,
#     }
#     return render(request, 'Hod/edit_corporate_tax.html', context)
#
# @login_required(login_url='/')
# def UPDATE_CORPORATETAX(request, id):
#     corporatetax = get_object_or_404(CorporateTax, id=id)
#     if request.method == "POST":
#         corporatetax.bills = request.POST.get('bills')
#         corporatetax.plastic = request.POST.get('plastic')
#         corporatetax.avans = request.POST.get('avans')
#         corporatetax.save()
#         messages.success(request, "Corporate Tax information updated successfully.")
#         return redirect('view_corporatetax')
#     context = {
#         'corporatetax': corporatetax,
#     }
#     return render(request, 'Hod/edit_corporate_tax.html', context)


def VIEW_EXISTTAX(request):
    corporatetax = CorporateTax.objects.all()
    context = {
        'corporatetax': corporatetax
    }
    return render(request, 'Hod/view_exist_tax.html', context)


def VIEW_BRANCH(request):
    branch = Branch.objects.all()
    branch_count = Branch.objects.all().count()
    teacher_count = Staff.objects.filter(department='Teacher').count()
    managers_count = Staff.objects.exclude(department='Teacher').count()

    context = {
        'branch': branch,
        'branches_count': branch_count,
        'teachers_count': teacher_count,
        'managing_staff': managers_count
    }
    return render(request, 'Hod/view_branches.html', context)


def VIEW_BRANCHES(request, id):
    branch = Branch.objects.filter(id=id)

    context = {
        'branch': branch,
    }
    return render(request, 'Hod/view_branch.html', context)