from urllib import request
from django import forms
from django.shortcuts import get_object_or_404
from customadmin.models import CustomUser
from customsettings.models import Subjects
from district.models import SchoolAdminProfile
from .models import *
from django.http import HttpResponseRedirect


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                
                }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                
                }),
        
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'gender', 'grade_level', 'date_of_birth', 'address',
            'guardian_name', 'guardian_number', 'guardian_email', 'student_photo'
        ]
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'guardian_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'guardian_email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'student_photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
   
            
            

class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'gender', 'grade_level', 'date_of_birth', 'address',
            'guardian_name', 'guardian_number', 'guardian_email', 'student_photo'
        ]
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'style': ' background-color: #474955; color:white;border-color:orange;',
                }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select',
                'style': ' background-color: #474955; color:white; border-color:orange;',
                }),
            
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                 'style': 'width: 640px; background-color: #474955; color:white; border-color:orange;',
                }),

            'classrooms': forms.Select(attrs={
                'class': 'form-select',
                 'style': 'width: 150px; background-color: #474955; color:white; border-color:orange;',
                }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                 'style': 'background-color: #474955; color:white; border-color:orange;',
                  'rows':  3
                }),

            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:orange;',
                }),
                
            'guardian_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:orange;focus-ring:orange;',
                }),
            'guardian_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:orange;',
                }),
            
            'student_photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }


class CreateClassRoomForm(forms.ModelForm):
    class Meta:
        model  = ClassRoom  
        fields = ['name', 'grd_level', 'class_teacher']

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        year = kwargs.pop('year', None)  # Add year to filter teachers based on the academic year
        super(CreateClassRoomForm, self).__init__(*args, **kwargs)
        
        if school and year:
            # Exclude classrooms that already exist for the given school and year
            existing_classrooms = ClassRoom.objects.filter(school=school, year=year).values_list('name', flat=True)
            self.fields['name'].queryset = ClassName.objects.filter(schoolprofile=school).exclude(id__in=existing_classrooms)
            
            # Exclude teachers already assigned to a classroom in the same school and year
            assigned_teachers = ClassRoom.objects.filter(school=school, year=year).exclude(class_teacher__isnull=True).values_list('class_teacher', flat=True)
            self.fields['class_teacher'].queryset = CustomUser.objects.filter(
                groups__name='teacher', 
                teacherprofile__school=school.id
            ).exclude(id__in=assigned_teachers)
                 
            
            
class EditClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'grd_level', 'class_teacher']
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',
                
                }),
                
            'grd_level': forms.Select(attrs={
                'class': 'form-control',
               
                }),
            'class_teacher': forms.Select(attrs={
                'class': 'form-control',
                
                }),
        }

    def __init__(self, *args, **kwargs):
        super(EditClassRoomForm, self).__init__(*args, **kwargs)
        # Get the current classroom instance
        classroom = kwargs.get('instance')
        
        # Get all teachers assigned to a classroom, excluding the current classroom's teacher
        assigned_teachers = CustomUser.objects.filter(assigned_class__isnull=False).exclude(assigned_class=classroom)
        
        # Exclude these teachers from the queryset
        self.fields['class_teacher'].queryset = CustomUser.objects.filter(
            groups__name='teacher'
        ).exclude(id__in=assigned_teachers)

   

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']
        widgets ={
            'student':forms.Select(attrs={
                'class':'form-control',
                
            }),
            'status':forms.RadioSelect(attrs={
                'class':'form-control',
            })
            
        }
       
       
class ExtraCurricularActivityForm(forms.ModelForm):
    class Meta:
        model = ExtraCurricularActivity
        fields = ['activity_name', 'description', 'instructor', 'requirements', 'category']
        widgets = {
            'activity_name': forms.TextInput(attrs={
                'class': 'form-control',
                 
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'instructor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter out students from the instructor field
        self.fields['instructor'].queryset = CustomUser.objects.filter(user_type__in=['teacher', 'deputy_head', 'school_head',])
      

class JoinActivityForm(forms.Form):
   
    activity_id = forms.ModelChoiceField(queryset=ExtraCurricularActivity.objects.all(), label="Activity")