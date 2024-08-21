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

        
