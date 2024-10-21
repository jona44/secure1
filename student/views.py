from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from customadmin.models import CustomUser
from customsettings.models import AcademicCalendar
from district.models import SchoolAdminProfile
from .forms import *
from .models import   *
from django.db import transaction
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import get_user_school


def get_assigned_school(user):
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=user)
    the_school = school_admin_profile.school
    school = get_object_or_404(SchoolProfile, school=the_school)
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


import logging
logger = logging.getLogger(__name__)

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
    
def student_details(request, pk):
    # Retrieve the student profile
    student_profile = get_object_or_404(StudentProfile, pk=pk)
    if pk is not None:
        edit_student_profile_url = reverse('edit_student_profile', args=[student_profile.pk])
    
    return render(request, 'student/student_details.html', {'student_profile': student_profile})

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


def classroom_details(request, pk):
    # Get the classroom object by primary key (pk)
    classroom = get_object_or_404(ClassRoom, pk=pk)

    # Safely query all SchoolProfile objects; if empty, it will pass an empty QuerySet
    subjects = SchoolProfile.objects.all()  # Make sure there are no missing or required fields that could raise a 404
    
    students = classroom.students.all()  # Assuming classroom has a related name to Student model

    male_count = students.filter(gender='male').count()
    female_count = students.filter(gender='female').count()
    total_count = students.count()

    female_percentage = (female_count / total_count) * 100 if total_count > 0 else 0
    male_percentage = (male_count / total_count) * 100 if total_count > 0 else 0

    # Initialize selected_student to None
    selected_student = None
    selected_student_pk = None

    # Capture the student_id from the request URL (if present)
    if request.GET.get('student_id'):
        selected_student_pk = request.GET['student_id']
        selected_student = StudentProfile.objects.get(pk=selected_student_pk)

    context = {
        'classroom': classroom,
        'subjects': subjects,
        'students': students,
        'male_count': male_count,
        'female_count': female_count,
        'total_count': total_count,
        'male_percentage': male_percentage,
        'female_percentage': female_percentage,
        'selected_student': selected_student,  # Pass selected student profile to context
        'selected_student_pk': selected_student_pk,  # Pass selected student profile to context
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

    # Get the classroom and its students
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    students = classroom.students.all()
    attendance_records = Attendance.objects.filter(date=today, classroom=classroom)

    # Get the current academic year
    academic_year = AcademicCalendar.objects.get(is_current = True)
   
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Assign the classroom and academic year to the form before saving
            form.instance.classroom = classroom
            form.instance.academic_year = academic_year
            form.save()
            # Redirect to the same page to fetch the next student
            return redirect('attendance', classroom_id=classroom_id)
    else:
        # Check if there are students remaining to mark attendance
        remaining_students = students.exclude(id__in=Attendance.objects.filter(date=today, classroom=classroom).values_list('student', flat=True))

        if remaining_students.exists():
            # Fetch the first student from the remaining list
            student = remaining_students.first()
            form = AttendanceForm(initial={'student': student, 'date': today})
        else:
            # If all students have been marked, redirect to the success page
            return redirect('attendance_record', classroom_id=classroom_id)
            
    return render(request, 'student/attendance.html', {
        'form': form,
        'classroom': classroom,
        'today': today,
        'attendance_records': attendance_records
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
    

#----------------------------all students-------------------------------------------


def students_list(request):  
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    the_school = school_admin_profile.school
    school =SchoolProfile.objects.get(school=the_school)
    students = StudentProfile.objects.filter(school=school)
    return render(request, 'student/students_list.html',{'students':students,'school':school})

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

def transfer_student(request, pk):
    student_profile = get_object_or_404(StudentProfile, id=pk)
    
    # Set the student's school to null (suspended)
    student_profile.school = None
    student_profile.save()

    messages.success(request, f'{student_profile.student} has been placed in suspense for transfer.')
    return redirect('student_details', pk)

#------------------------------suspense_pool----------------------------------------------

def suspense_pool(request):
    students_in_suspense = StudentProfile.objects.filter(school__isnull=True)
    return render(request, 'student/suspense_pool.html', {'students': students_in_suspense})

#------------------------------accept_student----------------------------------------

def accept_student(request, student_profile_id):
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
