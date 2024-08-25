
from django import forms
from customsettings.models import SchoolProfile
from student.models import ClassRoom
from .models import TeacherProfile

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['assigned_school', 'contact_number', 'assigned_class', 'classes_taught', 'base_subject', 'subjects_taught']
        widgets = {
            'assigned_school': forms.Select(attrs={
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
            

class UpdateStaffProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['contact_number','assigned_school','assigned_class','classes_taught', 'base_subject', 'subjects_taught']
        widgets = {
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
               }),

            'assigned_school': forms.Select(attrs={
                'class': 'form-control', 'style': 'width:150px',
                  'style': 'width:350px;',}),
            
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
   