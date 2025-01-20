from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from customadmin.models import CustomUser
from customsettings.models import AcademicCalendar
from district.models import SchoolAdminProfile
from teacher.models import TeacherProfile
from .forms import *
from .models import   *
from django.db import transaction
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import get_user_school
from .utils import mark_default_attendance


def get_assigned_school(user):
    profile = get_object_or_404(SchoolAdminProfile, school_admin=user)
    _school = profile.school
    school = get_object_or_404(SchoolProfile, school=_school)
    
    return school

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, prefix='student')
        if form.is_valid():
            # Save student details
            student = form.save(commit=False)
            student.save()
            return redirect('create_student_profile', user_id=student.pk)
    else:
        form = StudentRegistrationForm(prefix='student')
    return render(request, 'student/student_registration.html', {'form': form})


#----------------------------------create_student_profile--------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def create_student_profile(request, user_id):
    student = get_object_or_404(CustomUser, pk=user_id)
    
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)
    try:
        student_profile = StudentProfile.objects.get(student=student)
        form = StudentProfileForm(instance=student_profile)
    except StudentProfile.DoesNotExist:
        student_profile = None
        form = StudentProfileForm()

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            try:
                with transaction.atomic():
                    student_profile = form.save(commit=False)
                    student_profile.student = student
                    student_profile.school = school

                    grade_level_id = form.cleaned_data['grade_level'].id

                    current_academic_calendar = AcademicCalendar.objects.get(is_current=True)
                    student_profile.academic_year = current_academic_calendar
                    
                    student_profile.save()

                    # Assign all subjects from the school to the student
                    subjects = SchoolSubject.objects.filter(school=school)
                    student_profile.subjects.set(subjects)  
                    student_profile.save()

                    return redirect('select_classroom', pk=student_profile.pk, grade_level_id=grade_level_id)
            except Exception as e:
                form.add_error(None, str(e))
        else:
            print(form.errors)  # Add this line to print form errors to the console

    return render(request, 'student/create_student_profile.html', {'form': form, 'student': student})

#-------------------------------select_classroom------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def select_classroom(request, pk, grade_level_id):  # Add grade_level_id parameter
    student = get_object_or_404(StudentProfile, pk=pk)
    
    school = get_assigned_school(request.user)
    try:
        grade_level = get_object_or_404(GradeLevel, pk=grade_level_id)
    except GradeLevel.DoesNotExist:
        print(f"Grade level not found for ID: {grade_level_id}")
        return render(request, 'student/select_classroom.html', {
            'error': f"Grade level not found for ID: {grade_level_id}",
            'student': student
        })

    classrooms = ClassRoom.objects.filter(name__schoolprofile=school.id,grd_level=grade_level)

    class_data = []
    for classroom in classrooms:
        class_students = classroom.students.all()
        total_students = class_students.count()
        male_count = class_students.filter(gender='male').count()
        female_count = class_students.filter(gender='female').count()

        total_count = male_count + female_count
        if total_count > 0:
            female_percentage = (female_count / total_count) * 100
            male_percentage = (male_count / total_count) * 100
        else:
            female_percentage = 0
            male_percentage = 0

        class_data.append({
            'classroom': classroom,
            'total_students': total_students,
            'male_count': male_count,
            'female_count': female_count,
            'female_percentage': female_percentage,
            'male_percentage': male_percentage,
        })

    return render(request, 'student/select_classroom.html', {
        'classrooms': classrooms,
        'class_data': class_data,
        'student': student,
    })
    
    
#---------------------------------assign_classroom--------------------------------    


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def assign_classroom(request, pk):
    student_profile = get_object_or_404(StudentProfile, pk=pk)

    # Check if a classroom ID is provided in the URL query parameter
    classroom_id = request.GET.get('classroom_id')
    if classroom_id:
        # Retrieve the classroom object based on the provided ID
        classroom = get_object_or_404(ClassRoom, pk=classroom_id)
        
        # Assign the chosen classroom to the student
        student_profile.assigned_class = classroom
        student_profile.save()

        # Also add the student to the selected classroom
        classroom.students.add(student_profile)

        # Redirect to student details page or wherever needed
        return redirect('student_details', pk=student_profile.pk)
    else:
        # If no classroom ID is provided, redirect to the select_classroom page
        return HttpResponseRedirect(reverse('select_classroom', args=[pk]))
    
#--------------------------------student_details-------------------------------------------    
    
from django.db.models import F


@login_required
def student_details(request, pk):
    # Retrieve the student profile
    student_profile = get_object_or_404(StudentProfile, pk=pk)
    student_school=student_profile.school
    current_school =student_profile.school
    _class  =student_profile.assigned_class
   
    
    # Check if the logged-in user is the school admin for the student's school
    user_is_student_school_admin = False
    
    if student_school:
        the_school = get_user_school(request.user) 
        the_school = the_school
    else:
          
        student_school = the_school

    # Retrieve the next and previous students
    next_student = StudentProfile.objects.filter(pk__gt=pk,school=current_school,assigned_class=_class).first()
    previous_student = StudentProfile.objects.filter(pk__lt=pk,school=current_school,assigned_class=_class).order_by('-pk').first()

    return render(request, 'student/student_details.html', {
        'student_profile': student_profile,
        'next_student': next_student,
        'previous_student': previous_student,
        'user_is_student_school_admin': user_is_student_school_admin,
        'student_school':student_school
    })
#--------------------------------student_details-------------------------------------------    
    
from django.db.models import F


@login_required
def student_profile(request, pk):
    # Retrieve the student profile
    student_profile = get_object_or_404(StudentProfile, pk=pk)
    student_school=student_profile.school
    current_school =student_profile.school
    _class  =student_profile.assigned_class
   
    
    # Check if the logged-in user is the school admin for the student's school
    user_is_student_school_admin = False
    
    if student_school:
        the_school = get_user_school(request.user) 
        the_school = the_school
    else:
          
        student_school = the_school

    # Retrieve the next and previous students
    next_student = StudentProfile.objects.filter(pk__gt=pk,school=current_school,assigned_class=_class).first()
    previous_student = StudentProfile.objects.filter(pk__lt=pk,school=current_school,assigned_class=_class).order_by('-pk').first()

    return render(request, 'student/student_profile.html', {
        'student_profile': student_profile,
        'next_student': next_student,
        'previous_student': previous_student,
        'user_is_student_school_admin': user_is_student_school_admin,
        'student_school':student_school
    })


#------------------------------------classrooms--------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def classrooms(request):
    classrooms = ClassRoom.objects.all()
    class_data = []
    for classroom in classrooms:
        class_students = classroom.students.all()
        total_students = class_students.count()
        boys_count = class_students.filter(gender='male').count()
        girls_count = class_students.filter(gender='female').count()
        class_data.append({
            'classroom': classroom,
            'total_students': total_students,
            'boys_count': boys_count,
            'girls_count': girls_count,
        })
    return render(request,'student/classrooms.html}',{'classrooms':classrooms,'class_data': class_data})




#-----------------------------------create_classroom---------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def create_classroom(request):
    year = AcademicCalendar.objects.get(is_current=True)
    
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)
    
    if request.method == 'POST':
        form = CreateClassRoomForm(request.POST, school=school ,year=year)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.school=school
            classroom.year = year
            classroom.save()  # Corrected: Call save() method to save the classroom object
            return redirect(reverse('classroom_details', args=[classroom.pk]))
    else:
        form = CreateClassRoomForm(school=school, year=year)
        print(school)  
    return render(request, 'student/create_classroom.html', {'form': form})


#------------------------------classroom_details----------------------------------

from django.http import HttpResponseNotFound

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type in ['school_admin', 'teacher'])
def classroom_details(request, pk):
    # Fetch the classroom object by primary key (pk)
    classroom = get_object_or_404(ClassRoom, pk=pk)
    
    # Determine the logged-in user's profile and school
    profile = None
    if request.user.user_type == 'school_admin':
        profile = SchoolAdminProfile.objects.filter(school_admin=request.user).first()
    elif request.user.user_type == 'teacher':
        profile = TeacherProfile.objects.filter(teacher=request.user).first()
    
    if not profile:
        return HttpResponseNotFound("Profile not found for the logged-in user.")
    
    school = profile.school

    # Filter students by classroom and the user's school
    students = classroom.students.filter(school=school)

    # Gender-based statistics
    male_count = students.filter(gender='male').count()
    female_count = students.filter(gender='female').count()
    total_count = students.count()
    male_percentage = (male_count / total_count) * 100 if total_count > 0 else 0
    female_percentage = (female_count / total_count) * 100 if total_count > 0 else 0

    # Handle selected student (optional)
    selected_student = None
    selected_student_pk = request.GET.get('student_id')
    if selected_student_pk:
        selected_student = get_object_or_404(StudentProfile, pk=selected_student_pk)

    # Prepare context for template
    context = {
        'classroom': classroom,
        'students': students,
        'male_count': male_count,
        'female_count': female_count,
        'total_count': total_count,
        'male_percentage': male_percentage,
        'female_percentage': female_percentage,
        'selected_student': selected_student,
        'selected_student_pk': selected_student_pk,
    }
    return render(request, 'student/classroom_details.html', context)


#---------------------------------------------------------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def edit_classroom(request, pk):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    if request.method == 'POST':
        form = EditClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('classroom_details',  pk=pk)
    else:
        form =  EditClassRoomForm(instance=classroom)
    return render(request, 'student/edit_classroom.html', {'form': form, 'classroom': classroom})

#-----------------------------edit student_profile---------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def edit_student_profile(request, pk):
    student_profile = get_object_or_404(StudentProfile, pk=pk)

    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    grade_level_id = form.cleaned_data['grade_level'].id
                    # Redirect to a success page or another view
                    return redirect('select_classroom', pk=student_profile.pk,grade_level_id=grade_level_id)
            except Exception as e:
                # Handle any exceptions gracefully
                form.add_error(None, str(e))  # Add error to non-field errors
    else:
        form = EditStudentProfileForm(instance=student_profile)
    return render(request, 'student/edit_student_profile.html', {'form': form, 'student_profile': student_profile})


#--------------------------------------------attendance----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'teacher')
def attendance(request, classroom_id):
    # Get today's date
    today = datetime.now().date()

    # Get the classroom
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)

    # Mark default attendance for the day
    mark_default_attendance(classroom, today)

    # Fetch today's attendance records for the classroom
    attendance_records = Attendance.objects.filter(classroom=classroom, date=today)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Update attendance record with the form data
            attendance = Attendance.objects.get(
                student=form.cleaned_data['student'], 
                date=today, 
                classroom=classroom
            )
            attendance.status = 'Absent'
            attendance.save()
            return redirect('attendance', classroom_id=classroom_id)
    else:
        form = AttendanceForm(initial={'date': today})

    return render(request, 'student/attendance.html', {
        'form': form,
        'classroom': classroom,
        'today': today,
        'attendance_records': attendance_records,
    })    
#-------------------------------------------------attendance_record--------------------------------------------------------------    

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'teacher')
def attendance_record(request, classroom_id):
    # Get the current academic year
    academic_year = AcademicCalendar.objects.get(is_current = True)

    # Filter attendances by classroom and academic year
    attendances = Attendance.objects.filter(classroom_id=classroom_id, academic_year=academic_year)
    
    # Extract unique dates from attendance records
    unique_dates = sorted(set(attendance.date for attendance in attendances))

    # Prepare data in the format {student_name: [attendance_record_1, attendance_record_2, ...]}
    attendance_records = {}
    for attendance in attendances:
        student_name = attendance.student
        if student_name not in attendance_records:
            attendance_records[student_name] = [None] * len(unique_dates)
        index = unique_dates.index(attendance.date)
        attendance_records[student_name][index] = attendance

    return render(request, 'student/attendance_record.html',
                {'unique_dates': unique_dates, 'attendance_records': attendance_records})
    
    
#----------------------------- student_attendance-----------------------------------------------
  

def student_attendance(request, student_id):
    student = StudentProfile.objects.get(id=student_id)
    attendance_records = Attendance.objects.filter(student=student).order_by('date')
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
    }
    return render(request, 'student/student_attendance.html', context)


#----------------------------all students-------------------------------------------


from django.db.models import Q

def students_list(request):
    # school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # the_school = school_admin_profile.school
    # school = SchoolProfile.objects.get(school=the_school)
    school = get_assigned_school(request.user)

    # Retrieve filter options from GET request
    assigned_class = request.GET.get('assigned_class')
    gender = request.GET.get('gender')
    grade_level = request.GET.get('grade_level')
    is_suspended = request.GET.get('is_suspended')

    # Base queryset
    students = StudentProfile.objects.filter(school=school)

    # Apply filters if present
    if assigned_class:
        students = students.filter(assigned_class_id=assigned_class)
    if gender:
        students = students.filter(gender=gender)
    if grade_level:
        students = students.filter(grade_level_id=grade_level)
    if is_suspended is not None:
        students = students.filter(is_suspended=(is_suspended == 'true'))

    # Retrieve data for filter options
    classes = ClassRoom.objects.filter(school=school)
    grade_levels = GradeLevel.objects.all()

    return render(
        request, 
        'student/students_list.html', 
        {
            'students': students,
            'school': school,
            'classes': classes,
            'grade_levels': grade_levels,
        }
    )


#----------------------------------create_activity---------------------------------------

def create_activity(request):
    if request.method == 'POST':
        form = ExtraCurricularActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activity_list')  # Redirect to a list view or any other view
    else:
        form = ExtraCurricularActivityForm()
    
    return render(request, 'student/create_activity.html', {'form': form})


#--------------------------------------------activity_list---------------------------------------------------------------


def activity_list(request):
    activities = ExtraCurricularActivity.objects.all()  # Fetch all activities from the database
    return render(request, 'student/activity_list.html', {'activities': activities})

#------------------------------------------------

from django.contrib import messages

from .forms import JoinActivityForm

def join_activity(request, student_profile_id):
    student_profile = get_object_or_404(StudentProfile, id=student_profile_id)

    if request.method == 'POST':
        form = JoinActivityForm(request.POST)
        if form.is_valid():
            # Get the student and activity from the form
            activity = form.cleaned_data['activity_id']
            
            # Add the student to the activity participants
            activity.participants.add(student_profile)
            
            # Update the student's profile with the activity
            student_profile.extra_activity = activity
            student_profile.save()

            # Send success message and redirect
            messages.success(request, f'{student_profile.student} has been successfully added to {activity}.')
            return redirect('activity_members_list', activity_id=activity.id)  # Redirect to activity list or another page
    else:
        form = JoinActivityForm(initial={'student_profile_id': student_profile})

    return render(request, 'student/join_activity.html', {'form': form})


def activity_members_list(request, activity_id):
    activity = get_object_or_404(ExtraCurricularActivity, id=activity_id)
    participants = activity.participants.all()

    return render(request, 'student/activity_members_list.html', {
        'activity': activity,
        'participants': participants
    })
    
#-----------------------------transfer-student----------------------------------

from django.utils.timezone import now

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def transfer_student(request, pk):
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)
    student_profile = get_object_or_404(StudentProfile, id=pk)

    # Record the current school in the history if it exists
    if student_profile.school:
        StudentSchoolHistory.objects.create(
            student=student_profile,
            school=student_profile.school
        )

    # Set the student's school to null (suspended)
    student_profile.school = None
    student_profile.save()

    messages.success(request, f'{student_profile.student} has been placed in suspense for transfer.')
    return redirect('student_details', pk)

#-------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def undo_transfer(request, pk):
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)
    
    student_profile = get_object_or_404(StudentProfile, id=pk)

    # Check if the student has any school history
    latest_history = StudentSchoolHistory.objects.filter(student=student_profile).order_by('-transfer_date').first()

    if latest_history:
        # Restore the most recent school
        student_profile.school = latest_history.school
        student_profile.save()

        # Optionally, delete the latest history entry if no longer needed
        latest_history.delete()

        messages.success(
            request,
            f"{student_profile.student.get_full_name} has been restored to {student_profile.school.school.school}."
        )
    else:
        messages.error(request, f"No school history found for {student_profile.student.get_full_name}. Undo failed.")

    return redirect('student_details', pk)


#------------------------------suspense_pool----------------------------------------------


from django.db.models import OuterRef, Subquery

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def suspense_pool(request):
    # Get the school admin's school
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)

    # Subqueries to fetch the most recent school and district
    recent_school_subquery = StudentSchoolHistory.objects.filter(
        student=OuterRef('pk')
    ).order_by('-transfer_date').values('school__school__school')[:1]

    recent_district_subquery = StudentSchoolHistory.objects.filter(
        student=OuterRef('pk')
    ).order_by('-transfer_date').values('school__school__district__district')[:1]

    # Annotate students in suspense with recent school and district
    students_in_suspense = StudentProfile.objects.filter(school__isnull=True).annotate(
        recent_school=Subquery(recent_school_subquery),
        recent_district=Subquery(recent_district_subquery)
    )

    # Render the suspense pool template
    return render(request, 'student/suspense_pool.html', {
        'students': students_in_suspense,
        'school': school,
    })
#------------------------------accept_student----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def accept_student(request, student_profile_id):
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=the_school)
    student_profile = get_object_or_404(StudentProfile, id=student_profile_id)
    
    # Fetch academic records related to the student and their previous school
    academic_records = AcademicRecord.objects.filter(student=student_profile, school__isnull=False).order_by('-year', '-term')

    if request.method == 'POST':
        # Assign the student to the current admin's school (this depends on your admin system)
        school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
        the_school = school_admin_profile.school
        school = District_School_Registration.objects.get(school=the_school) # Assuming the logged-in user is associated with a school
        
        # Transfer the student to the new school
        student_profile.school = school
        student_profile.save()

        messages.success(request, f'{student_profile.student} has been successfully transferred to {school}.')
        return redirect('suspense_pool')

    return render(request, 'student/accept_student.html', {
        'student_profile': student_profile,
        'academic_records': academic_records
    })
