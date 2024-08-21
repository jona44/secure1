from django.db import models
from django.forms import ValidationError
from customsettings.models import AcademicCalendar, SchoolSubject
from customsettings.models import Subjects
from student.models import ClassRoom, StudentProfile
from django.core.exceptions import ValidationError

class Capture(models.Model):
    CHOICES = [
        ('weekly', 'Weekly Exercise'),
        ('assignment','Assigment'),
        ('year', 'End-of-Year Exam')
    ]
   
    subject      = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE,)
    test_type    = models.CharField(max_length=50, choices=CHOICES, blank=False, null=False)
    topic        = models.CharField(max_length=50, blank=False, null=False)
    total_mark   = models.IntegerField(default=50, blank=False, null=False)
    select_classes  = models.ManyToManyField(ClassRoom) 
    date            = models.DateField(auto_now_add=True)
    academic_year   = models.ForeignKey(AcademicCalendar,on_delete=models.CASCADE, blank=False, null=False)
    is_captured     = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject}-{self.test_type}- {self.topic}"
    
    def all_classes_captured(self):
            # Check if all selected classes are captured
        selected_classes = self.select_classes.all()
        captured_classes = CapturedClassroom.objects.filter(capture=self, is_captured=True).values_list('classroom', flat=True)
        return all(cls.id in captured_classes for cls in selected_classes)
    
    
class CapturedClassroom(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=False, null=False)
    capture   = models.ForeignKey(Capture, on_delete=models.CASCADE, blank=False, null=False)
    is_captured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.classroom} -- {self.capture}"


class GetMark(models.Model):
    captured_classroom = models.ForeignKey(CapturedClassroom, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ManyToManyField(StudentProfile, related_name='marks')
    mark    = models.PositiveBigIntegerField(null=True, blank=True)
    grade   = models.PositiveBigIntegerField(null=True, blank=True)
    pass_code = models.CharField(default='F', max_length=1, null=True, blank=True)
    date      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.captured_classroom} -- {self.student} -- {self.grade}"

    def calculate_grade(self):
        if self.mark is not None and self.captured_classroom.capture.total_mark:
            total_mark = self.captured_classroom.capture.total_mark
            if total_mark != 0:
                percentage = (self.mark / total_mark) * 100
                return round(percentage)
            else:
                return "Invalid total mark"  # Handle case where total_mark is 0
        return None

    def categorize_grade(self, grade):
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

    def save(self, *args, **kwargs):
        self.grade = self.calculate_grade()
        if self.grade is not None and isinstance(self.grade, int):  # Check if grade is an integer
            self.pass_code = self.categorize_grade(self.grade)
        super().save(*args, **kwargs)