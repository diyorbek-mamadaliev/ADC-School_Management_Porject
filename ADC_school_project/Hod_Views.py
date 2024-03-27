import ast

from django.db.models.functions import Now
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Course, customUser, Student, Staff, Payments, ExistingStudent, CorporateTax, Branch, Attendance, \
    Book, LibraryMembers
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
from django.db.models import Max, F




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
            branch=branch
        )
        course.save()
        messages.success(request, "New Group Added Successfully!")
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
        branch_name = request.POST.get('branch')
        branch_instance = Branch.objects.get(name=branch_name)
        course_id = request.POST.get('course_id')
        days = request.POST.get('days')
        hours = request.POST.get('hours')
        course_status = request.POST.get('status')
        teacher_id = request.POST.get('teacher_id')
        course = Course.objects.get(id=course_id)

        staff = Staff.objects.get(id=teacher_id)


        course.subject = subject
        course.level = level
        course.branch = branch_instance
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
        email = request.POST.get('email')
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
                          email=email,
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
                      branch=branch,
                      status=status,
                      birth_date=birth_date,
                      address=address,
                      mobile=mobile,
                      mobiletwo=mobiletwo)
        staff.save()
        messages.success(request, "New Staff Created Successfully!")
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
    branches = Branch.objects.all()

    context = {
        'staff': staff,
        'branches': branches
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
        email = request.POST.get('email')
        role = request.POST.get('role')
        fines = request.POST.get('fines')
        bonus = request.POST.get('bonus')
        tax = request.POST.get('tax')
        salary_type = request.POST.get('salary_type')
        salary_amount = request.POST.get('salary_amount')
        work_format = request.POST.get('work_format')
        branch_name = request.POST.get('branch_name')
        branch = Branch.objects.get(id=branch_name)
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
        user.email = email

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
        staff.branch_name = branch
        staff.address = address
        staff.mobile = mobile
        staff.mobiletwo = mobiletwo

        staff.save()
        messages.success(request, "Updated Successfully!")
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
    nows_month = datetime.now().strftime("%B")
    course = Course.objects.get(id=id)
    student = Student.objects.filter(course_id=id)
    payments = Payments.objects.filter(group_id__icontains=course.username, created_at__month=now_month)
    existing_students = ExistingStudent.objects.filter(course_id=id)
    attendance = Attendance.objects.filter(group_id=course.username, created_at__month=now_month)

    # Calculate attendance count for each student
    attendance_counts = {}
    for s in student:
        count = attendance.filter(students__contains=s.admin.username).count()
        attendance_counts[s.admin.username] = count

    attendance_existing_counts = {}
    for s in existing_students:
        count = attendance.filter(students__contains=s.student_id).count()
        attendance_existing_counts[s.student_id] = count

    context = {
        'course': course,
        'nows_month': nows_month,
        'student': student,
        'attendance_existing_counts': attendance_existing_counts,
        'attendance': attendance,
        'payments': payments,
        'attendance_counts': attendance_counts,
        'existing_students': existing_students
    }
    return render(request, 'Hod/view_students.html', context)

@login_required(login_url='/')
def ADD_FEE(request, id):
    student = Student.objects.filter(id=id)
    student_get = Student.objects.get(id=id)
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

        # Update the last_payment field of the associated Student instance
        student_get.last_payment = payment
        student_get.save()

        return redirect('payment_preview')

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
    staff = Staff.objects.all()

    context = {
        'payments': payments,
        'staff': staff
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

@login_required(login_url='/')
def STAFF_SALARY(request):
    # Retrieve Teachers
    teachers = Staff.objects.filter(department='Teacher')

    # Get current month
    current_month = datetime.now().month

    # Calculate Total Fees
    teacher_fees = []
    for teacher in teachers:
        # Query payments made to the teacher in the current month
        payments = Payments.objects.filter(teacher_id=teacher,
                                           created_at__month=current_month)

        # Calculate total cash payments
        total_cash = payments.filter(payment_type='Cash').aggregate(
            total_cash=Sum('fee_amount'))['total_cash'] or 0

        # Calculate total plastic payments
        total_plastic = payments.filter(payment_type='Plastic').aggregate(
            total_plastic=Sum('fee_amount'))['total_plastic'] or 0

        # Calculate total fees collected
        total_fees = total_cash + total_plastic

        teacher_fees.append({
            'teacher': teacher,
            'total_cash': total_cash,
            'total_plastic': total_plastic,
            'total_fees': total_fees
        })

    # Calculate Total Fees Across All Teachers
    total_fees_across_all_teachers = sum(
        teacher['total_fees'] for teacher in teacher_fees)

    context = {
        'teacher_fees': teacher_fees,
        'total_fees_across_all_teachers': total_fees_across_all_teachers
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
        teacher_id=request.user.get_full_name(),
        created_at__month=now_month,
        created_at__year=datetime.now().year
    )
    context = {'payments': payments}
    return render(request, 'Hod/payments_by_teacher.html', context)

def TEACHER_GROUP_PANEL(request):
    groups = Course.objects.exclude(status="Archived").exclude(username='Not_Selected_1').filter(teacher_id__admin__username=request.user.username)

    context = {
               'groups': groups}
    return render(request, 'Hod/teacher_group_panel.html', context)


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
    staff = Staff.objects.all()
    branch = Branch.objects.all()
    branch_count = Branch.objects.all().count()
    teacher_count = Staff.objects.filter(department='Teacher').count()
    managers_count = Staff.objects.exclude(department='Teacher').count()

    context = {
        'branch': branch,
        'branches_count': branch_count,
        'staff': staff,
        'teachers_count': teacher_count,
        'managing_staff': managers_count
    }
    return render(request, 'Hod/view_branches.html', context)


def VIEW_BRANCHES(request, id):
    branch = Branch.objects.get(id=id)
    group_count = Course.objects.filter(branch__name=branch.name).distinct().count()
    teacher_count = Staff.objects.filter(department='Teacher').count()
    staff_list = Staff.objects.filter(branch__name=branch.name).exclude(department='Teacher').distinct().count()
    days_to_check = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    tts = Course.objects.filter(days="Tuesday, Thursday, Saturday", branch__name=branch.name)
    mwf = Course.objects.filter(days="Monday, Wednesday, Friday", branch__name=branch.name)
    courses = Course.objects.exclude(subject="Not_Selected_1").all()
    student_count = Student.objects.filter(course_id__branch=branch).distinct().count()
    today_date = datetime.now().strftime("%A")
    staff = Staff.objects.filter(department="Teacher")

    context = {
        'group_count': group_count,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'staff_count': staff_list,
        'branch': branch,
        'today_date': today_date,
        'courses': courses,
        'staff': staff,
        'tts': tts,
        'mwf': mwf
    }
    return render(request, 'Hod/view_branch.html', context)


def ADD_BRANCH(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        rooms = request.POST.get('rooms')
        profile_pic = request.FILES.get('photo')  # Get the uploaded photo
        branch = Branch(
            name=name,
            address=address,
            phone_number=phone_number,
            rooms=rooms,
            profile_pic=profile_pic,  # Assign the photo to the branch instance
        )
        branch.save()
        return redirect('view_branch')
    else:
        return render(request, 'Hod/add_branch.html')


def ADD_ATTENDANCE(request, id):

    course = Course.objects.get(id=id)
    student_list = Student.objects.filter(course_id__username=course.username)
    existing_students = ExistingStudent.objects.filter(course_id=id)


    if request.method == 'POST':
        students = request.POST.getlist('students')
        group_id = request.POST.get('group_id')
        group_subject = request.POST.get('group_subject')
        group_level = request.POST.get('group_level')
        teacher_id = request.POST.get('teacher_id')
        teacher_first_name = request.POST.get('teacher_first_name')
        teacher_last_name = request.POST.get('teacher_last_name')
        lesson_topic = request.POST.get('lesson_topic')

        # Create an Attendance instance
        attendance = Attendance(
            students=students,
            group_id=group_id,
            group_subject=group_subject,
            group_level=group_level,
            teacher_id=teacher_id,
            teacher_first_name=teacher_first_name,
            teacher_last_name=teacher_last_name,
            lesson_topic=lesson_topic
        )
        attendance.save()

        return redirect('view_attendance', id=id)

    context = {'student_list': student_list, 'course': course, 'existing_students': existing_students}
    return render(request, 'Hod/add_attendance.html', context)


def VIEW_ATTENDANCE(request, id):
    course = Course.objects.get(id=id)
    attendance = Attendance.objects.filter(group_id=course.username)


    context = {
        'attendance': attendance,
        'course': course,
    }
    return render(request, 'Hod/view_attendance.html', context)


def VIEW_ATTENDANCE_DAY(request, id):
    attendance = Attendance.objects.get(id=id)
    students = Student.objects.all()
    if attendance.students:
        students_list = ast.literal_eval(attendance.students)
    else:
        students_list = []

    context = {
        'attendance': attendance,
        'student_list': students_list,
        'students': students
    }
    return render(request, 'Hod/view_attendance_day.html', context)


def VIEW_BOOKS(request):
    books = Book.objects.all().exclude(given_status="Given")

    context = {
        'books': books
    }
    return render(request, 'Hod/view_books.html', context)


def ADD_BOOK(request):
    if request.method == 'POST':
        # Retrieve data from the form
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        genre = request.POST.get('genre')

        # Create a new Book instance
        book = Book.objects.create(
            book_name=book_name,
            author=author,
            published_date=published_date,
            genre=genre
        )
        messages.success(request,'New Book Added Successfully!')

        # Redirect to a success page or wherever appropriate
        return redirect('view_books')  # Replace 'success_page' with the URL name of your success page

    return render(request, 'Hod/add_book.html')


def ADD_NEW_MEMBER(request):
    if request.method == 'POST':

        # Retrieve member data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        member_id = request.POST.get('member_id')
        passport_series = request.POST.get('passport_series')
        # Assuming you're also uploading an image for passport_scan
        passport_scan = request.FILES.get('passport_scan')

        # Create a new LibraryMember instance
        member = LibraryMembers.objects.create(
            first_name=first_name,
            last_name=last_name,
            member_id=member_id,
            passport_series=passport_series,
            passport_scan=passport_scan,
        )

        messages.success(request, 'New Library Member Added Successfully!')

        # Redirect to a success page or wherever appropriate
        return redirect('view_books')  # Replace 'view_books' with the URL name of your book view

    return render(request, 'Hod/add_new_member.html')


def VIEW_LIBRARY_MEMBERS(request):
    members = LibraryMembers.objects.all()

    context = {
        'members': members
    }
    return render(request, 'Hod/view_library_members.html', context)

def REGISTER_BOOK(request, id):
    books = Book.objects.filter(id=id)
    members = LibraryMembers.objects.all()
    context = {
        'books': books,
        'members': members,
    }
    return render(request, 'Hod/register_book.html', context)

# def REGISTER_BOOK(request):
#     if request.method == "POST":
#         book_name = request.POST.get('book_name')
#         author = request.POST.get('author')
#         published_date = request.POST.get('published_date')
#         genre = request.POST.get('genre')
#         given_status = request.POST.get('given_status')
#         given_member_id = request.POST.get('given_member_id')
#         given_book_name = request.POST.get('given_book_name')
#         existing_id = request.POST.get('id')
#
#         try:
#             existing_book = Book.objects.get(id=existing_id)
#             existing_book.book_name = book_name
#             existing_book.author = author
#             existing_book.published_date = published_date
#             existing_book.genre = genre
#             existing_book.given_status = given_status
#             existing_book.given_member_id = given_member_id
#             existing_book.given_book_name = given_book_name
#             existing_book.save()
#             messages.success(request, "Book Registered Successfully!")
#         except Book.DoesNotExist:
#             messages.error(request, "Book with given ID does not exist")

    #     return redirect('view_books')  # Redirect to a view where you display all books
    #
    # return render(request, 'Hod/register_book.html')
def UPDATE_BOOK(request):
    if request.method == "POST":
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        genre = request.POST.get('genre')
        given_status = request.POST.get('given_status')
        given_member_id = request.POST.get('given_member_id')
        due_date = request.POST.get('due_date')
        book_id = request.POST.get('book_id')  # Assuming there's an input field with name 'book_id' in your form

        book = Book.objects.get(id=book_id)
        book.book_name = book_name
        book.author = author
        book.published_date = published_date
        book.genre = genre
        book.due_date = due_date
        book.given_status = given_status
        book.given_member_id = given_member_id

        book.save()

        messages.success(request, "Book updated successfully")
        return redirect('view_books')  # Redirect to view_books or any appropriate URL after updating

    return render(request, 'Hod/register_book.html')


def VIEW_GIVEN_BOOKS(request):
    books = Book.objects.filter(given_status="Given")
    members = LibraryMembers.objects.all()

    context = {
        'books': books,
        'members': members
    }
    return render(request, 'Hod/view_given_books.html', context)