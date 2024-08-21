from multiprocessing import context
from django import views
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from customadmin.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str 
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from customsettings.models import SchoolProfile, SchoolSubject
from district.models import SchoolAdminProfile
from teacher.models import TeacherProfile
from student.models import StudentProfile

from .forms import *

@login_required
def dashboard(request):
    user = request.user
    context = {}
    print(f"User: {user.email}, Groups: {user.groups.all()}")  # Debugging statement:

#--------------------------------------Student Dashboard---------------------------------------
       
    if request.user.groups.filter(name='student').exists():
        try:
            student_profile = StudentProfile.objects.get(student=user)
            school = student_profile.school
            
            # Get Student's Class
            assigned_class = student_profile.assigned_class
            if assigned_class:
                class_students = assigned_class.students.filter(school=school)  # Filter classmates by school
                female_classmates = class_students.filter(gender='female')
                male_classmates = class_students.filter(gender='male')
                classmates_count = class_students.count()
                context['classmates_count'] = classmates_count
                context['female_classmates'] = female_classmates.count()
                context['male_classmates'] = male_classmates.count()
                context['assigned_class'] = assigned_class
                
                return render(request, 'customadmin/dashboard/student_dashboard.html', context)

        except StudentProfile.DoesNotExist:
            pass
        
#-----------------------------------------Teacher Dashboard-------------------------------------


    import logging

    logger = logging.getLogger(__name__)

    if request.user.groups.filter(name='teacher').exists():
        try:
            teacher_profile = TeacherProfile.objects.get(teacher=request.user)
            school = teacher_profile.assigned_school
            
            # Get Classes and Students for Teacher
            my_classes = teacher_profile.classes_taught.all()
            my_classes_students = []
            for class_ in my_classes:
                students = class_.students.all()
                female_students = students.filter(gender='female')
                male_students = students.filter(gender='male')
                students_count = students.count()
                my_classes_students.append({
                    'class_': class_,
                    'students': students,
                    'female_students': female_students,
                    'students_count': students_count,
                    'male_students': male_students,
                })
            
            context = {
                'my_classes_students': my_classes_students,
                'my_subjects': teacher_profile.subjects_taught.all()
            }

            return render(request, 'customadmin/dashboard/teacher_dashboard.html', context)

        except TeacherProfile.DoesNotExist:
            logger.error("TeacherProfile does not exist for user: %s", request.user)
            # Handle the error appropriately, maybe redirect to an error page

       
#---------------------------------school_admin dashboard---------------------------------------


    if request.user.groups.filter(name='school_admin').exists():
        try:
            print(f"User {request.user} is in 'school_admin' group.")
            
            # Get the SchoolAdminProfile associated with the logged-in user
            profile = SchoolAdminProfile.objects.filter(school_admin=request.user).first()
            print(f"SchoolAdminProfile: {profile}")
            
            if not profile:
                context['error'] = "School admin profile does not exist."
                return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)

            # Get the school registration associated with the SchoolAdminProfile
            school_registration = profile.assigned_school_name
            print(f"School Registration: {school_registration}")
           
            # Get the SchoolProfile instance associated with the school_registration
            school = SchoolProfile.objects.filter(school_name=school_registration).first()
            print(f"SchoolProfile: {school}")
            
            if not school:
                # Redirect to schoolProfile_create_step1 if SchoolProfile does not exist
                return redirect('school_profile_create_step1')

            if not school.is_setup_complete:
                # Redirect to setup step if setup is not complete
                return redirect('school_profile_create_step1')

            # Additional data for School Admin dashboard
            allsubjects = SchoolSubject.objects.all()
            students_count = StudentProfile.objects.filter(assigned_school=school).count()
            all_teachers = TeacherProfile.objects.filter(assigned_school=school).count()

            print(f"All Subjects: {allsubjects}")
            print(f"Students Count: {students_count}")
            print(f"All Teachers: {all_teachers}")
            
            # Prepare context for rendering
            context = {
                'all_teachers': all_teachers,
                'students_count': students_count,
                'allsubjects': allsubjects,
            }
            return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)
        except Exception as e:
            print(f"Error: {e}")
            context['error'] = str(e)
            return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)
        else:
            print("User is not in 'school_admin' group.")
            return redirect('login')        
#-----------------------------------------deputy_head dashboard-------------------------------------------     
    

    elif request.user.groups.filter(name='deputy_head').exists():
        # Show deputy_head_dashboard
        return render(request, 'customadmin/dashboard/deputy_head_dashboard.html')
    
    elif request.user.groups.filter(name='school_head').exists():
        # Show school_head_dashboard
        return render(request, 'customadmin/dashboard/school_head_dashboard.html')
   
    elif request.user.groups.filter(name='district_admin').exists():
        # Show school_head_dashboard
        return render(request, 'customadmin/dashboard/district_admin_dashboard.html')
    else:
        # Show default dashboard
        return render(request, 'customadmin/dashboard/default_dashboard.html')
   

@login_required
def login_redirect(request):
    user = request.user
    print(f"User: {user.email}, Groups: {user.groups.all()}")
      # Debugging statement
    if request.user.groups.filter(name='student').exists():
        return redirect('student_dashboard')
    
    elif request.user.groups.filter(name='teacher').exists():
        return redirect('teacher_dashboard')
    
    elif request.user.groups.filter(name='school_admin').exists():
        return redirect('school_admin_dashboard')
    
    elif request.user.groups.filter(name='deputy_head').exists():
        return redirect('deputy_head_dashboard')
    
    elif request.user.groups.filter(name='school_head').exists():
        return redirect('school_head_dashboard')
    
    elif request.user.groups.filter(name='district_admin').exists():
        return redirect('district_admin_dashboard')
    
    else:
        return redirect('default_dashboard')

   
def  registration_complete(request):
    return render(request,'customadmin/registration_complete.html')


  
     



