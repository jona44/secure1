from urllib import request
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import get_object_or_404
from customadmin.models import CustomUser
from customsettings.models import ClassName, SchoolProfile
from district.models import SchoolAdminProfile
from student.models import ClassRoom
from .models import TeacherProfile



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','user_type', 'position','password1','password2' )
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
            'user_type': forms.Select(attrs={
                'class': 'form-control',
               
                }),
            'position': forms.Select(attrs={
                'class': 'form-control',
                
                }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',  
                }),
       
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
               
                }),
         }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['school', 'contact_number', 'assigned_class', 'classes_taught', 'base_subject', 'subjects_taught']
        widgets = {
            'school': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }),
            'assigned_class': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }),
            'classes_taught': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
            'base_subject': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }),
            'subjects_taught': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
        }
        def __init__(self, *args, **kwargs):
            def __init__(self, *args, **kwargs):
                school = kwargs.pop('school', None)
                super(TeacherProfileForm, self).__init__(*args, **kwargs)
                if school:  
                    self.fields['assigned_class'].queryset = ClassRoom.objects.filter(school=school)
                  
                

class UpdateStaffProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['contact_number','assigned_class','classes_taught', 'base_subject', 'subjects_taught']
        widgets = {
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
               }),

            
            'assigned_class': forms.Select(attrs={
                'class': 'form-control', 'style': 'width:150px',
                  'style': 'width:350px;',}),
        
            'classes_taught': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'}),

            'base_subject': forms.Select(attrs={
                'class': 'form-control', 'style': 'width:150px',
                'style': 'width:350px;',
                }),

            'subjects_taught': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'}),
        }
   