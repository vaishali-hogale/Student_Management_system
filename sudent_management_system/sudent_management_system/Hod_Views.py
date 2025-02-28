from django.contrib.sessions.models import Session
from  django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, CustomUser, Student, Staff, Subject, Staff_Notification, Staff_leave
from django.contrib import messages



def HOME(request):
    student_count=Student.objects.all().count()
    staff_count=Staff.objects.all().count()
    course_count=Course.objects.all().count()
    subject_count=Subject.objects.all().count()
    student_gender_male=Student.objects.filter(gender='Male').count()
    student_gender_female=Student.objects.filter(gender='Female').count()


    context={
        'subject_count':subject_count,
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female
    }
    return render(request,'Hod/home.html',context)

@login_required(login_url='/')

def ADD_STUDENT(request):
    course = Course.objects.all()
    if request.method == "POST":
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        gender=request.POST.get('gender')
        course_id=request.POST.get('course_id')
       # print(first_name,last_name,profile_pic,username,email,password)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Emil is already exit')
            return redirect('add_student')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username is already Exit')
            return redirect('add_student')

        else:
            user=CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type = 3
            )
            user.set_password=password
            user.save()

            course=Course.objects.get(id=course_id)

            student=Student(
                admin = user,
                address=address,
                course_id=course,
                gender=gender

            )
            student.save()
            messages.success(request,user.first_name+" "+ user.last_name+ "Are Successfully Added ")
            return redirect('add_student')



    context={
        'course':course,
    }


    return render(request,'Hod/add_student.html',context)

@login_required(login_url='/')

def VIEW_STUDENT(request):
    student=Student.objects.all()
    context={
        'student':student,

    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')

def EDIT_STUDENT(request,id):
    student=Student.objects.filter(id=id)
    course=Course.objects.all()
    context={
        'student':student,
        'course':course,
    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')

def UPDATE_STUDENT(request):
    if request.method=="POST":
        student_id=request.POST.get('student_id')
        print(student_id)
        profile_pic=request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')


        user=CustomUser.objects.get(id=student_id)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email

        user.username=username

        if password!=None and password != "":
           user.set_password(password)
        if profile_pic != None and profile_pic !="":
            user.profile_pic=profile_pic
        user.save()


        student=Student.objects.get(admin=student_id)
        student.address=address
        student.gender=gender

        course=Course.objects.get(id= course_id)
        student.course_id=course

        student.save()

        messages.success(request,"Record are successfully updated")
        return redirect('view_student')
    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student=CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Record Are Successfully Deleted')

    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method=="POST":
        course_name=request.POST.get('course_name')
        course=Course(
            name=course_name,

        )
        course.save()
        messages.success(request,"Course Are Successfully Created")
        return redirect('add_course')

    return render(request,'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course=Course.objects.all()
    context={
        'course':course
    }

    return render(request,'Hod/view_course.html',context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course=Course.objects.get(id=id)
    context={
        'course':course,
    }
    return render(request,'Hod/edit_course.html',context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method=="POST":
        name=request.POST.get('name')
        course_id=request.POST.get('course_id')


        course=Course.objects.get(id=course_id)
        course.name=name
        course.save()
        messages.success(request,"Course Are Successfully Update! ")
        return redirect('view_course')

    return render(request,'Hod/edit_course.html')



@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Record Are Successfully Deleted')

    return redirect('view_student')

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method=="POST":
        profile_pic=request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Emil is already exit')
            return redirect('add_staff')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username is already Exit')
            return redirect('add_student')
        else:
            user=CustomUser(first_name=first_name,last_name=last_name,email=email,profile_pic=profile_pic,user_type=2,username=username)
            user.set_password(password)
            user.save()

            staff=Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request,'Staff Are Successfully Added')
            return redirect('add_staff')



    return render(request,'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff=Staff.objects.all()
    context={
        'staff':staff,
    }
    return render(request,'Hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff=Staff.objects.get(id=id)
    context={
        'staff':staff,
    }

    return render(request, 'Hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method=="POST":
        staff_id=request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user=CustomUser.objects.get(id=staff_id)
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        if password!=None and password != "":
           user.set_password(password)
        if profile_pic != None and profile_pic !="":
            user.profile_pic=profile_pic
        user.save()

        staff=Staff.objects.get(admin=staff_id)
        staff.gender=gender
        staff.address=address
        staff.save()
        messages.success(request,'Staff Are Successfully Updated')
        return redirect('view_staff')



    return render(request,'Hod/edit_staff')

@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff=CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request,'Record Are Successfully Deleted!')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_SUBJECT(request):
    course=Course.objects.all()
    staff=Staff.objects.all()
    if request.method=="POST":
        subject_name=request.POST.get('subject_name')
        course_id=request.POST.get('course_id')
        staff_id=request.POST.get('staff_id')
        course=Course.objects.get(id=course_id)
        staff=Staff.objects.get(id=staff_id)
        subject=Subject(
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request,'Subjects Are Successfully Added')
        return redirect('add_subject')

    context={
        'course':course,
        'staff':staff
    }
    return render(request,'Hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject=Subject.objects.all()
    context={
        'subject':subject,
    }
    return render(request,'Hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject=Subject.objects.get(id=id)
    course=Course.objects.all()
    staff=Staff.objects.all()
    context={
        'subject':subject,
        'course':course,
        'staff':staff
    }
    return render(request,'Hod/edit_subject.html',context)


def UPDATE_SUBJECT(request,):
    if request.method=="POST":
        subject_name=request.POST.get('subject_name')
        subject_id=request.POST.get('subject_id')
        course_id=request.POST.get('course_id')
        staff_id=request.POST.get('staff_id')
        course=Course.objects.get(id=course_id)
        staff=Staff.objects.get(id=staff_id)
        subject=Subject(
            id=subject_id,
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request,"Subject Are Successfully Updated")
        return redirect('view_subject')


def DELETE_SUBJECT(request,id):
    subject=Subject.objects.filter(id=id)
    subject.delete()
    messages.success(request,'Subject Are Successfully Deleted')
    return redirect('view_subject')


def STAFF_SEND_NOTIFICATION(request):
    staff=Staff.objects.all().order_by('id')[0:5]
    see_notification=Staff_Notification.objects.all()
    context={
        'staff':staff,
        'see_notification':see_notification,

    }
    return render(request,'Hod/staff_notification.html',context)


def SAVE_NOTIFICATION(request):
    if request.method=="POST":
        staff_id=request.POST.get('staff_id')
        message=request.POST.get('message')
        staff=Staff.objects.get(admin=staff_id)
        notification=Staff_Notification(
            staff_id=staff,
            message=message,

        )
        notification.save()
        messages.success(request,"Notification Are Send Successfully")
        return redirect('staff_send_notification')



def STAFF_LEAVE_VIEW(request):
    staff_leave=Staff_leave.objects.all()
    context={
        'staff_leave':staff_leave
    }
    return render(request,'Hod/staff_leave.html',context)


def STAFF_APPROVE_LEAVE(request,id):
    leave=Staff_leave.objects.get(id=id)
    leave.status=1
    leave.save()

    return redirect('staff_leave_view')


def STAFF_DISAPPROVE_LEAVE(request,id):
    leave=Staff_leave.objects.get(id=id)
    leave.status=2
    leave.save()
    return  redirect('staff_leave_view')
