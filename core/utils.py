from urllib import request
from django.contrib.auth.models import Group
from district.models import SchoolHeadProfile
from student.models import  StudentProfile
from teacher.models import TeacherProfile
from customsettings.models import  SchoolAdminProfile


def get_user_school(user):
    # Check for user type and return the corresponding school attribute
    if user.groups.filter(name='student').exists():
        return StudentProfile.objects.get(student=user).school  # Use `student=user` and `school`
    
    elif user.groups.filter(name='teacher').exists():
        return TeacherProfile.objects.get(user=user).school
    
    elif user.groups.filter(name='school_admin').exists():
        return SchoolAdminProfile.objects.get(admin=user).school  # Adjust to match the field in SchoolAdminProfile
    
    elif user.groups.filter(name='school_head').exists() or user.groups.filter(name='school_head').exists():
        return SchoolHeadProfile.objects.get(admin=user).school  # Adjust for school_head/deputy_head
    else:
        return None
