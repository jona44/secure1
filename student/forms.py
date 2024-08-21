
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
            'gender','grade_level', 'date_of_birth', 'address',
            'guardian_name', 'guardian_number', 'guardian_email'
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
            

            'classrooms': forms.Select(attrs={
                'class': 'form-select',
                 
                }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                
                  'rows':  3
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
        }
   
            
            

class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'gender','grade_level', 'date_of_birth', 'address',
            'guardian_name', 'guardian_number', 'guardian_email'
        ]
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 150px; background-color: #474955; color:white;border-color:red;',
                }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 150px; background-color: #474955; color:white; border-color:red;',
                }),
            
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                 'style': 'width: 150px; background-color: #474955; color:white; border-color:red;',
                }),

            'classrooms': forms.Select(attrs={
                'class': 'form-select',
                 'style': 'width: 150px; background-color: #474955; color:white; border-color:red;',
                }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                 'style': 'background-color: #474955; color:white; border-color:red;',
                  'rows':  3
                }),

            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
                
            'guardian_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;focus-ring:red;',
                }),
            'guardian_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
        }


        

class CreateClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom  
        fields = ['name','grd_level','class_teacher']

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super(CreateClassRoomForm, self).__init__(*args, **kwargs)
        if school:
            self.fields['name'].queryset = ClassName.objects.filter(schoolprofile=school)
        self.fields['class_teacher'].queryset = CustomUser.objects.filter(groups__name='teacher')


class EditClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom  # replace with your actual model
        fields = ['name','grd_level','class_teacher',]
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
                
            'grd_level': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red; focus-ring:red;',
                }),
            'class_teacher': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
        }
    def __init__(self, *args, **kwargs):
        super(EditClassRoomForm, self).__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset = CustomUser.objects.filter(groups__name='teacher') 
   

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