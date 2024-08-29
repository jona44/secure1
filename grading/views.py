from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.views import View
from grading.forms import *
from grading.models import *
from teacher.models import TeacherProfile
from student.models import ClassRoom
from django.db.models import Avg
from django.urls import reverse
from district.models import Subjects

def capture(request, subject_id):
    subject = get_object_or_404(SchoolSubject, pk=subject_id)
    academic_year = get_object_or_404(AcademicCalendar, is_current=True)
    teacher_profile = get_object_or_404(TeacherProfile, teacher=request.user)
    select_classes = teacher_profile.get_all_classes_taught()

    existing_captures = Capture.objects.filter(
        subject=subject,
        academic_year=academic_year
    ).order_by('test_type', 'topic')

    # Annotate each capture with a flag indicating if it's done
    captures_with_status = []
    for capture_instance in existing_captures:
        is_done = capture_instance.all_classes_captured()  # Assuming this is a method in your model
        captures_with_status.append({
            'capture': capture_instance,
            'is_done': is_done
        })

    if request.method == 'POST':
        if 'capture_id' in request.POST:
            capture_id = request.POST['capture_id']
            capture_instance = get_object_or_404(Capture, pk=capture_id)
            return redirect('captured_classroom', capture_id=capture_instance.id)
        else:
            form = CaptureForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                test_type = cleaned_data['test_type']
                topic = cleaned_data['topic']
                total_mark = cleaned_data['total_mark']

                capture_instance = Capture.objects.filter(
                    subject=subject,
                    test_type=test_type,
                    topic=topic,
                    total_mark=total_mark,
                    academic_year=academic_year
                ).first()

                if not capture_instance:
                    capture_instance = Capture.objects.create(
                        subject=subject,
                        test_type=test_type,
                        topic=topic,
                        total_mark=total_mark,
                        academic_year=academic_year,
                    )
                    capture_instance.select_classes.set(select_classes)

                return redirect('captured_classroom', capture_id=capture_instance.id)
    else:
        form = CaptureForm()

    context = {
        'form': form,
        'subject': subject,
        'captures_with_status': captures_with_status,
    }
    return render(request, 'grading/capture.html', context)

#------------------------------------------------captured_classroom--------------------------------


def captured_classroom(request, capture_id):
    capture = get_object_or_404(Capture, pk=capture_id)
    available_classrooms = capture.select_classes.all()

    if request.method == 'POST':
        form = CapturedClassroomForm(request.POST)
        if form.is_valid():
            captured_classroom_instance = CapturedClassroom.objects.filter(
                classroom=form.cleaned_data['classroom'],
                capture=capture
            ).first()

            if captured_classroom_instance:
                return redirect('getmark', captured_classroom_id=captured_classroom_instance.id)
            else:
                captured_classroom = form.save(commit=False)
                captured_classroom.capture = capture
                captured_classroom.save()
                return redirect('getmark', captured_classroom_id=captured_classroom.id)
    else:
        form = CapturedClassroomForm()
        # Exclude classrooms that have already captured all students
        fully_captured_classrooms = CapturedClassroom.objects.filter(capture=capture, is_captured=True).values_list('classroom', flat=True)
        form.fields['classroom'].queryset = available_classrooms.exclude(id__in=fully_captured_classrooms)

    context = {'form': form, 'capture': capture}
    return render(request, 'grading/captured_classroom.html', context)


#--------------------------------------getmark----------------------------------------

def getmark(request, captured_classroom_id):
    captured_classroom = get_object_or_404(CapturedClassroom, pk=captured_classroom_id)
    all_students = captured_classroom.classroom.students.all()
    all_students_count = all_students.count()

    # Get students who haven't been graded yet
    students = all_students.exclude(
        marks__captured_classroom=captured_classroom, marks__mark__isnull=False
    )

    if not students.exists():
        # Set the is_captured attribute to True if all students are graded
        captured_classroom.is_captured = True
        captured_classroom.save()
        return redirect('success_page', captured_classroom_id=captured_classroom.id)

    current_student = students.first()
    graded_students = all_students_count - students.count()
    progress = round((graded_students / all_students_count) * 100)

    student_before = all_students.filter(id__lt=current_student.id).last()
    student_after = all_students.filter(id__gt=current_student.id).first()

    if request.method == 'POST':
        form = GetMarkForm(request.POST)
        if form.is_valid():
            get_mark_instance = form.save(commit=False)
            get_mark_instance.captured_classroom = captured_classroom  # Manually set the captured_classroom
            get_mark_instance.save()
            get_mark_instance.student.add(current_student)  # Correctly add the student to the many-to-many field
            return redirect('getmark', captured_classroom_id=captured_classroom_id)
    else:
        form = GetMarkForm()

    context = {
        'form': form,
        'captured_classroom': captured_classroom,
        'current_student': current_student,
        'all_students': all_students,
        'all_students_count': all_students_count,
        'student_before': student_before,
        'student_after': student_after,
        'progress': progress,
    }
    return render(request, 'grading/getmark.html', context)


#--------------------------------------success_page---------------------------------------


def success_page(request, captured_classroom_id):
    # Retrieve the capture object or return a 404 error if not found
    captured_classroom = get_object_or_404(CapturedClassroom, pk=captured_classroom_id)
     
    capture = captured_classroom.capture
    classroom = captured_classroom.classroom

    # Filter GetMark instances by the specified capture
    marks_for_capture = GetMark.objects.filter(captured_classroom=captured_classroom)

    # Get the subject_id from the capture object
    subject_id = capture.subject.id

    # Calculate the average pass rate for female students
    female_students = StudentProfile.objects.filter(gender='female')
    female_average = GetMark.objects.filter(student__in=female_students, captured_classroom=captured_classroom).aggregate(Avg('grade'))['grade__avg']

    # Round the average to a single decimal place
    female_average = round(female_average, 1) if female_average else None

    # Calculate the average pass rate for male students
    male_students = StudentProfile.objects.filter(gender='male')
    male_average = GetMark.objects.filter(student__in=male_students, captured_classroom=captured_classroom).aggregate(Avg('grade'))['grade__avg']

    # Round the average to a single decimal place
    male_average = round(male_average, 1) if male_average else None

    context = {'marks_for_capture': marks_for_capture,
              'capture': capture,
              'subject_id': subject_id,
              'female_average': female_average,
              'male_average': male_average,
              'classroom':classroom
              }
    return render(request, 'grading/success_page.html', context)


#----------------------------------------editmark--------------------------------------


def editmark(request, getmark_id, student_id):
    getmark = get_object_or_404(GetMark, pk=getmark_id)
    student = get_object_or_404(StudentProfile, pk=student_id)

    if request.method == 'POST':
        form = EditMarkForm(request.POST, instance=getmark)
        if form.is_valid():
            form.save()
            return redirect('success_page',captured_classroom_id=getmark.captured_classroom.id)
    else:
        form = EditMarkForm(instance=getmark)

    context = { 'form': form,
                'getmark': getmark, 
                'student': student
                }
    return render(request, 'grading/editmark.html', context)


#----------------------------------edit_capture----------------------------------------


def edit_capture(request, capture_id):
    # Retrieve the Capture object or return a 404 error if not found
    capture = get_object_or_404(Capture, pk=capture_id)
    subject = capture.subject

    if request.method == 'POST':
        form = CaptureForm(request.POST, instance=capture)
        if form.is_valid():
            form.save()
            return redirect('captured_classroom', capture_id=capture.id)
    else:
        form = CaptureForm(instance=capture)

    context = {'form': form, 'capture': capture ,'subject':subject}
    return render(request, 'grading/edit_capture.html', context)


#----------------------------------student grades--------------------------------------


def student_grades(request, student_id, subject_id):
    # Retrieve the student and subject instances
    student = get_object_or_404(StudentProfile, pk=student_id)
    subject = get_object_or_404(SchoolSubject, pk=subject_id)  # Ensure this is a Subjects instance

    # Filter CapturedClassroom instances based on the subject instance
    captured_classrooms = CapturedClassroom.objects.filter(capture__subject=subject)

    if not captured_classrooms.exists():
        return render(request, 'grading/no_captured_classroom.html', {'subject': subject})

    # Retrieve all GetMark instances for the student and captured classrooms
    student_grades = GetMark.objects.filter(student=student, captured_classroom__in=captured_classrooms)

    # Extract grades to render separately
    grades_list = list(student_grades.values_list('grade', flat=True))

    # Calculate average grade using model's aggregate function
    grade_average = student_grades.aggregate(Avg('grade'))['grade__avg'] or 0

    context = {
        'student_grades': student_grades,
        'student': student,
        'subject': subject,
        'grades_list': grades_list,  # Pass the list of grades to the context
        'grade_average': grade_average,
    }
    return render(request, 'grading/student_grades.html', context)


#-----------------------------------------student_report------------------------------------------------


def student_report(request, student_id):
    student = get_object_or_404(StudentProfile, pk=student_id)

    # Get all subjects for the student
    subjects = SchoolSubject.objects.filter(
        capture__capturedclassroom__getmark__student=student
    ).distinct()

    # Create a dictionary to store the average grade and category for each subject
    subject_data = {}

    # Calculate average grades and categorize them for each subject
    for subject in subjects:
        # Filter GetMark instances by the specified student and subject
        student_grades = GetMark.objects.filter(
            student=student, 
            captured_classroom__capture__subject=subject
        )

        # Calculate the average grade for the subject
        average_grade = student_grades.aggregate(Avg('grade'))['grade__avg']
        if average_grade is not None:
            # Categorize the grade
            grade_category = categorize_grade(round(average_grade))
            subject_data[subject] = {
                'average_grade': round(average_grade),
                'category': grade_category
            }
        else:
            # Handle the case where average_grade is None
            subject_data[subject] = {
                'average_grade': None,
                'category': None 
            }

    # Context data to be passed to the template
    context = {'student': student, 'subject_data': subject_data}

    # Render the student report template with the context data
    return render(request, 'grading/student_report.html', context)


#-------------------------------------categorize_grades-----------------------------------

def categorize_grade(grade):
    """Categorizes a grade based on the given scale."""
    if grade >= 90:
        return 'A'
    elif grade >= 75:
        return 'B'
    elif grade >= 60:
        return 'C'
    elif grade >= 50:
        return 'D'
    elif grade >= 40:
        return 'E'
    else:
        return 'F'

                         
