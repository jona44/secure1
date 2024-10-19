# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *



class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')  



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','user_type', 'position', 'password1', 'password2', )
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
        

