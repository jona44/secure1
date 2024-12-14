from .models import  ClassRoom

def assign_class(student_profile):
    grade_classes = ClassRoom.objects.all()

    # Filter available classes based on gender balance
    available_classes = []
    for grade_class in grade_classes:
        # Filter students by gender
        male_count = grade_class.students.filter(student__studentprofile__gender='male').count()
        female_count = grade_class.students.filter(student__studentprofile__gender='female').count()

        # Check if the class has reached max capacity
        if grade_class.students.count() < grade_class.max_capacity:
            available_classes.append((grade_class, abs(male_count - female_count)))

    # Sort available classes by gender balance
    available_classes.sort(key=lambda c: c[1])

    if available_classes:
        return available_classes[0][0]  # Return the class with the best gender balance
    else:
        return None  # No available classes
    

from datetime import datetime
from .models import Attendance, StudentProfile, AcademicCalendar, ClassRoom

def mark_default_attendance(classroom, date=None):
    """
    Marks all students in the given classroom as 'Present' for the specified date.
    Students marked 'Absent' manually are excluded from this process.
    """
    if date is None:
        date = datetime.now().date()
    
    academic_year = AcademicCalendar.objects.get(is_current=True)
    students = classroom.students.all()

    for student in students:
        # Check if attendance already exists for the student
        attendance_exists = Attendance.objects.filter(student=student, classroom=classroom, date=date).exists()
        if not attendance_exists:
            # Create a "Present" record for students with no prior attendance record for the day
            Attendance.objects.create(
                student=student,
                classroom=classroom,
                date=date,
                status='Present',
                academic_year=academic_year,
            )
    

