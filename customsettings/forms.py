from django import forms
from .models import *

class SchoolProfileForm(forms.ModelForm):
   

    class Meta:
        model = SchoolProfile
        fields = ['school_logo', 'facebook', 'twitter', 'instagram']

    def save(self, commit=True):
        instance = super(SchoolProfileForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # Save the many-to-many relationships
        return instance
    

class SchoolSubjectForm(forms.ModelForm):
    school_subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = SchoolSubject
        fields = ['school_subjects']


class ClassNameForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['grd_level','classname']


class GradeLevelForm(forms.ModelForm):
    class Meta:
        model = GradeLevel
        fields = ['grade_level']  

from .models import ExtraCurricularActivity

class ExtraCurricularActivityForm(forms.ModelForm):
    class Meta:
        model = ExtraCurricularActivity
        fields = ['activity_name', 'description', 'instructor', 'requirements', 'category']        
        widgets = {
            'activity_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
                
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red; focus-ring:red;',
                 'rows':  3
                }),
            'instructor': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                 'rows':  3
                }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #474955; color:white; border-color:red;',
                }),
        }
