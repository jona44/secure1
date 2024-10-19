from django import forms
from django.contrib.auth.forms import UserCreationForm
from customadmin.models import CustomUser
from teacher.models import TeacherProfile
from . models import AcademicCalendar, District_School_Registration, DistrictAdminProfile, Holiday, SchoolAdminProfile, SchoolHeadProfile, Subjects




class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model  = District_School_Registration
        fields = [ 'school', 'address', 'phone_number', 'email']

        widgets = {
                'school': forms.TextInput(attrs={
                'class': 'form-control',
                  
                }),
                
                'address': forms.Textarea(attrs={
                'class': 'form-control',
                 
                  'rows':  3
                }),
                'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                 
                }),

                'email': forms.EmailInput(attrs={
                'class': 'form-control',
                 
                  
                }),
                }
        

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
        


class SchoolAdminProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolAdminProfile
        fields = [ 'contact_number','school','admin']
        
        
        
class SchoolHeadProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolHeadProfile
        fields = ['phone_number', 'email', 'school'] 
                


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['subjects']


class DistrictAdminProfileForm(forms.ModelForm):
    class Meta:
        model = DistrictAdminProfile
        fields = ['contact_number','district_name']
        widgets = {
            'district_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
           
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
            
        }        
        
class AcademicCalendarForm(forms.ModelForm):
    class Meta:
        model = AcademicCalendar
        fields = [
            
            'academic_year',
            'term_1_start_date',
            'term_1_end_date',
            'term_2_start_date',
            'term_2_end_date',
            'term_3_start_date',
            'term_3_end_date',
            'term_4_start_date',
            'term_4_end_date',
        ]
        widgets = {
            'academic_year': forms.DateInput(attrs={
                'class': 'form-control',
               
                
                }),
            'term_1_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px','class':'form-control',}),
            'term_1_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_2_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_2_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_3_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_3_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_4_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_4_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
        }
        
        
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('name', 'date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': ' background-color: #474955; color:white ;',
                }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'width: 150px; background-color: #474955; color:white',
                }),
        }        
        
        
class PreTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields= ['school','contact_number']