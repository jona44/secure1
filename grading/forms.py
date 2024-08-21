from django import forms
from customadmin.models import CustomUser
from .models import *
from django import forms


class CaptureForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields = ['test_type', 'topic', 'total_mark']
       


class CapturedClassroomForm(forms.ModelForm):
    class Meta:
        model = CapturedClassroom
        fields = ['classroom']



class GetMarkForm(forms.ModelForm):
    class Meta:
        model  = GetMark
        fields = [ 'mark'] 
        

class EditMarkForm(forms.ModelForm):
    class Meta:
        model  = GetMark
        fields = [ 'mark'] 

