from django.shortcuts import render, redirect, get_object_or_404
from customsettings.models import AcademicCalendar, SchoolProfile
from district.models import SchoolAdminProfile
from .forms import *
from .models import TeacherProfile
from customadmin.models import CustomUser 
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from .models import*
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger(__name__)



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def registration(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until activation
            user.save()

            # Assign the user to the desired group
            group_name = form.cleaned_data.get('user_type')
            desired_group = Group.objects.get(name=group_name)
            user.groups.add(desired_group)

            # Determine the appropriate profile creation view based on user type
            profile_view_mapping = {
                'student': 'create_student_profile', 
                'teacher': 'create_teacher_profile',
                'school_admin': 'create_schoolAdmin_profile',
                'deputy_head': 'create_deputyHead_profile',
                'school_head': 'create_schoolHead_profile',
                'district_admin': 'create_districtAdmin_profile', 
            }
            profile_view_name = profile_view_mapping.get(group_name, None)

            if profile_view_name:
                # Send activation email
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http' 
                subject = 'Activate Your Account'
                message = render_to_string('district/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': protocol,
                })
                send_mail(
                    subject,
                    '',  # The message parameter will be used for the email body
                    settings.EMAIL_HOST_USER,  # Replace with your email address
                    [user.email],  # Send to the user's email address
                    fail_silently=False,
                    html_message=message,  # Pass the 'message' as HTML content
                )

                # Redirect to the appropriate profile creation view
                return redirect(profile_view_name, user_id=user.id)
            else:
                messages.error(request, 'Invalid user type selected. Please contact support.')
        else:
            messages.error(request, 'Form submission failed. Please correct the errors below.')

    return render(request, 'customsettings/registration.html', {'form': form})


logger = logging.getLogger(__name__)



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type in ['school_admin'])
def create_teacher_profile(request, user_id):
    teacher = get_object_or_404(CustomUser, pk=user_id)
    
    # Get the school assigned to the current school admin
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    school_registration = school_admin_profile.school
    school = SchoolProfile.objects.get(school=school_registration)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST )
        if form.is_valid():
            with transaction.atomic():
                teacher_profile = form.save(commit=False)
                teacher_profile.teacher = teacher

                # Automatically set the assigned school
                teacher_profile.school = school

                # Set the current academic year
                academic_year = AcademicCalendar.objects.get(is_current=True)
                teacher_profile.academic_year = academic_year

                teacher_profile.save()

                # Assign the classes and subjects taught
                teacher_profile.classes_taught.set(form.cleaned_data['classes_taught'])
                teacher_profile.subjects_taught.set(form.cleaned_data['subjects_taught'])

            return redirect('view_teacher_profile', pk=teacher_profile.pk)
    else:
        form = TeacherProfileForm( )
        print(school)
    return render(request, 'teacher/create_teacher_profile.html', {'form': form, 'user_id': user_id})



#-----------------------------------view_teacher_profile-------------------------------------------


def view_teacher_profile(request, pk):
    teacher_profile = get_object_or_404(TeacherProfile, pk=pk)
    print("teacher Profile PK:", pk)  # Debugging statement
    return render(request, 'teacher/view_teacher_profile.html', {'teacher_profile': teacher_profile})


# --------------------------------- update_teacher_profile-------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def update_teacher_profile(request,pk):
    teacher_profile = get_object_or_404(TeacherProfile, pk=pk)
    if request.method == 'POST':
        form = UpdateStaffProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            form.save()
            return redirect('view_teacher_profile',pk=teacher_profile.pk)
    else:
        form =  UpdateStaffProfileForm(instance=teacher_profile)
    return render(request, 'teacher/update_teacher_profile.html', {'form': form})


#---------------------------------teacher_list--------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def teacher_list(request):
    try:
        school_admin = SchoolAdminProfile.objects.get(school_admin=request.user)
        school = school_admin.school
        all_teachers = TeacherProfile.objects.filter(school=school.id)
    except SchoolAdminProfile.DoesNotExist:
        all_teachers = None  # Or handle the case where the user is not a school admin

    context = {
        'all_teachers':all_teachers,
        # 'school_admin': school_admin if all_teachers else None,  # Pass the school admin if teachers exist
    }
    print(school)
    return render(request, 'teacher/teacher_list.html', {'all_teachers': all_teachers})
