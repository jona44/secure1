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

