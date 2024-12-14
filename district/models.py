import datetime
from django.db import models
from customadmin.models import CustomUser


class District(models.Model):
    district = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return f'{self.district}' 


class District_School_Registration(models.Model):
   
    district      = models.ForeignKey(District,on_delete=models.CASCADE,blank=True, null=True)
    school        = models.CharField(max_length=255,blank=True, null=True)
    address       = models.TextField(blank=True, null=True)
    phone_number  = models.CharField(max_length=20,blank=True, null=True)
    email         = models.EmailField(blank=True, null=True)
   
    def __str__(self):
        return f'{self.school}' 


class SchoolAdminProfile(models.Model):
    school_admin      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    contact_number    = models.CharField(max_length=255,blank=True, null=True)
    email             = models.EmailField(blank=True, null=True)
    school            = models.ForeignKey(District_School_Registration, on_delete=models.CASCADE,blank=True, null=True)
    admin             = models.CharField(max_length=10,choices=[('admin1','admin1'),('admin2','admin2'),('admin3','admin3')],null=True,blank=True)
    
    def __str__(self):
        return f'{self.school_admin}' 


class DistrictAdminProfile(models.Model):
    district_admin   = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='district_admin_profile')
    district_name    = models.CharField(max_length=255,blank=True, null=True)
    contact_number   = models.CharField(max_length=255,blank=True, null=True)
    email            = models.EmailField(blank=True, null=True)
    district_schools = models.ManyToManyField(District_School_Registration)
    admin   = models.CharField(max_length=10,choices=[('admin1','admin1'),('admin2','admin2'),('admin3','admin3')],null=True,blank=True)
    

    def __str__(self):
        return f'{self.district_admin}' 
    
    
    
class SchoolHeadProfile(models.Model):
    school_head      = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='SchoolHead_profile')
    phone_number     =  models.CharField(max_length=255,blank=True, null=True)
    email            = models.EmailField(blank=True, null=True)
    school           = models.ForeignKey(District_School_Registration, on_delete=models.CASCADE,blank=True, null=True)
    
    def __str__(self):
        return f'{self.school_head}' 
        
        
class Subjects(models.Model):
    subjects = models.CharField(max_length=50,blank=True,null=True)   

    def __str__(self):
        return f'{self.subjects}'  

    class Meta:
        verbose_name_plural = 'Subjects' 
        
        
class Holiday(models.Model):

    date = models.DateField()
    name = models.CharField(max_length=200)
    note = models.TextField()
   
    def __str__(self):
        return self.name         
        
        
class AcademicCalendar(models.Model):
    
    academic_year = models.PositiveIntegerField(default=datetime.datetime.now().year, blank=True, null=True)

    # Fields for each term
    term_1_start_date = models.DateField(blank=True, null=True)
    term_1_end_date   = models.DateField(blank=True, null=True)
    term_2_start_date = models.DateField(blank=True, null=True)
    term_2_end_date   = models.DateField(blank=True, null=True)
    term_3_start_date = models.DateField(blank=True, null=True)
    term_3_end_date   = models.DateField(blank=True, null=True)
    term_4_start_date = models.DateField(blank=True, null=True)
    term_4_end_date   = models.DateField(blank=True, null=True)
    holidays          = models.ManyToManyField(Holiday, related_name="academic_calendars")
    is_current        = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.academic_year}'    
    
    
       
    
    
class GradeLevel(models.Model):
    class GradeLevels(models.IntegerChoices):
        EIGHT  = 8, '8'
        NINE   = 9, '9'
        TEN    = 10, '10'
        ELEVEN = 11, '11'
        TWELVE = 12, '12'
        
    grade_level = models.IntegerField(choices=GradeLevels.choices)
   
    
    def __str__(self):
        return str(self.grade_level)    