from audioop import avg
from datetime import date, timezone
import datetime
from itertools import count
from django.db import models
from django.urls import reverse
from customadmin.models import  CustomUser
from django.db.models import Count
from customsettings.models import *
class StudentProfile(models.Model):
    school_name     = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, blank=True, null=True)
    student         = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender          = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    subjects        = models.ManyToManyField(SchoolSubject)  # Correctly relates to Subject
    grade_level     = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=8)
    date_of_birth   = models.DateField()
    assigned_class  = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True)
    address         = models.TextField(null=True, blank=True)
    guardian_name   = models.CharField(max_length=255, null=True, blank=True)
    guardian_number = models.CharField(max_length=15, null=True, blank=True)
    guardian_email  = models.EmailField(null=True, blank=True)
    date            = models.DateField(auto_now_add=True)
    academic_year   = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)
    extra_activity  = models.ForeignKey('ExtraCurricularActivity', on_delete=models.CASCADE, null=True, blank=True)
    student_photo   = models.ImageField(upload_to="students_photos", blank=True, null=True)
    is_suspended    = models.BooleanField(default=False)
    matriculated    = models.BooleanField(default=False)

    # Define default image paths
    DEFAULT_MALE_PHOTO = 'students_photos/default_male.png'
    DEFAULT_FEMALE_PHOTO = 'students_photos/default_female.png'

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'

    def get_assigned_class(self):
        return self.assigned_class

    def get_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # Set default photo based on gender if no photo is uploaded
        if not self.student_photo:
            if self.gender == 'male':
                self.student_photo = self.DEFAULT_MALE_PHOTO
            elif self.gender == 'female':
                self.student_photo = self.DEFAULT_FEMALE_PHOTO
        super().save(*args, **kwargs)


class ClassRoom(models.Model):
    name      = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    grd_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, null=True, blank=True)
    students  = models.ManyToManyField(StudentProfile, blank=True) 
    class_teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_class')
    max_capacity  = models.PositiveIntegerField(default=45)
    date          = models.DateField(auto_now_add=True)
    year          = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"  
    
    class Meta:
        ordering = ['name']
    
    def total_students(self):
            return self.students.count()

    def gender_distribution(self):
        return self.students.values('gender').annotate(total_students=Count('gender'))
    
    def get_absolute_url(self):
            return reverse('classroom-detail', kwargs={'pk': self.pk})


class Attendance(models.Model):
    classroom    = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date    = models.DateField(default=datetime.datetime.now)
    status  = models.CharField(max_length=10,default='',choices=[('Present', 'Present'), ('Absent', 'Absent')])    
    academic_year   = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)

    def has_attendance(self, day):
        return self.attendance_set.filter(date=day).exists()
    
    def is_present(self):
        return self.status == 'Present'

    def is_absent(self):
        return self.status == 'Absent'


class ExtraCurricularActivity(models.Model):
    CATEGORY_CHOICES = [
        ('SP', 'Sports'),
        ('AR', 'Arts'),
        ('AC', 'Academic'),
        ('OT', 'Other'),
    ]
    activity_name  = models.CharField(max_length=50)    
    description    = models.TextField()
    instructor     = models.CharField(max_length=100)
    requirements   = models.TextField(blank=True)
    category       = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.activity_name