import logging
from django.conf import settings
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.test import TransactionTestCase
from customadmin.models import CustomUser
from .models import*
from .forms import   *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
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
from .models import GradeLevel

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
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
                'teacher': 'pre_teacherprofile',
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

    return render(request, 'district/registration.html', {'form': form})


logger = logging.getLogger(__name__)


#------------------------------------create_districtAdmin_profile----------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'District_admin')
def create_districtAdmin_profile(request, user_id):
    
    # View to create a DistrictAdminProfile for a newly registered user.

    district_schools = District_School_Registration.objects.all()
    CustomUser = get_user_model()
    district_admin = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = DistrictAdminProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.district_admin = district_admin
            # Fetch the DistrictAdmin associated with the user:
           
            profile.district_admin = district_admin
            profile.save() 

            profile.district_schools.set(district_schools)
            profile.save() 

            return redirect('districtAdmin_profile_detail', profile_id=profile.id)
    else:
        form = DistrictAdminProfileForm()

    context = {
        'form': form,
        'district_admin': district_admin,
    }
    return render(request, 'district/create_district_admin_profile.html', context)


#------------------------------create_schoolAdmin_profile-----------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'District_admin')
def create_schoolAdmin_profile(request, user_id):
    """
    View to create a SchoolAdminProfile for a given CustomUser.
    """
    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = SchoolAdminProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.school_admin = user  # Assign the CustomUser to the profile
            profile.save()
            messages.success(request, 'SchoolAdmin Profile created successfully.')
            return redirect('schoolAdmin_profile_detail',profile_id=profile.id)  # Redirect to profile details
    else:
        form = SchoolAdminProfileForm()

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'district/create_schoolAdmin_profile.html', context)


#--------------------------------create_schoolHead_profile-----------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'District_admin')
def create_schoolHead_profile(request, user_id):
   # View for creating or updating a SchoolHead profile associated with a user.
    user = CustomUser.objects.get(pk=user_id)  # Get the user from the passed user_id
    # Check if a SchoolHead profile already exists for this user
    try:
        school_head = SchoolHeadProfile.objects.get(school_head=user)
        # Existing profile, display update form
        form = SchoolHeadProfileForm(instance=school_head) 
        if request.method == 'POST':
            form = SchoolHeadProfileForm(request.POST, instance=school_head)
            if form.is_valid():
                form.save()
                return redirect('schoolHead_profile_detail', profile_id=school_head.id)  # Redirect to the same view
    except SchoolHeadProfile.DoesNotExist:
        # No existing profile, display creation form
        form = SchoolHeadProfileForm(initial={'school_head': user})  # Set the initial school_head to the user
        if request.method == 'POST':
            form = SchoolHeadProfileForm(request.POST)
            if form.is_valid():
                school_head = form.save(commit=False)
                school_head.school_head = user
                school_head.save()
                return redirect('schoolHead_profile_detail', profile_id=school_head.id) 

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'district/create_schoolHead_profile.html', context)


#----------------------------------- school_list---------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def school_list(request):
    schools = District_School_Registration.objects.all()
    return render(request, 'district/school_list.html', {'schools': schools})


#----------------------------------- school_detail-----------------------------------


def school_detail(request, school_id):
    school = get_object_or_404(District_School_Registration, pk=school_id)
    return render(request, 'district/school_detail.html', {'school': school})


#------------------------------- create_school---------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_school(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school=form.save(commit=False)
            school.save()
            return redirect('school_detail', school_id=school.id)   # Redirect to a list of schools or relevant page
    else:
        form = SchoolRegistrationForm()
    return render(request, 'district/create_school.html', {'form': form})


#-------------------------------activation_sent---------------------------


def activation_sent(request):
    return render(request, 'district/activation_sent.html')  

  
#-------------------------------password_reset---------------------------


def password_reset(request):
    return render(request, 'district/password_reset.html')


#-------------------------------activate_account---------------------------


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Activate the user account
            user.is_active = True
            user.save()

            # Redirect to password reset view
            return redirect('password_reset')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Handle the exception (e.g., log an error or return a specific response)
        return HttpResponse("Invalid activation link")

    # Handle other cases or return an appropriate response
    return HttpResponse("Invalid activation link")


#-------------------------------registration_complete---------------------------


def  registration_complete(request):
    return render(request,'district/registration_complete.html')


#-------------------------------admin_profile----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def admin_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    profile = get_object_or_404(SchoolAdminProfile, user=user)
    return render(request, 'district/admin_profile.html', {'profile': profile})

#------------------------------------create_subject---------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_subject(request):
    all_subjects = Subjects.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject')
    else:
        form = SubjectForm()

    return render(request, 'district/subject_form.html', {'form': form,'all_subjects':all_subjects})


#----------------------------------staff_profile_view---------------------------------------------


def staff_profile_view(request):
    # Retrieve all staff members excluding students
    staff_members = CustomUser.objects.filter(is_student=False)

    return render(request, 'district/staff_profile.html', {'staff_members': staff_members}) 


#----------------------------districtAdmin_profile_detail---------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')

def districtAdmin_profile_detail(request, profile_id):
    """Displays the details of a DistrictAdminProfile."""
    profile = DistrictAdminProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'district/districtAdmin_profile_detail.html', context)


#---------------------------schoolAdmin_profile_detail-------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def schoolAdmin_profile_detail(request, profile_id):
    """Displays the details of a DistrictAdminProfile."""
    profile = SchoolAdminProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'district/schoolAdmin_profile_detail.html', context)


#---------------------------------schoolHead_profile_detail----------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def schoolHead_profile_detail(request, profile_id):
    """Displays the details of a DistrictAdminProfile."""
    profile = SchoolAdminProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'district/schoolHead_profile_detail.html', context)


#--------------------------create_academic_calendar_step2----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_academic_calendar(request):
    if request.method == 'POST':
        # Check if 'create_all_terms' is in the request data
        create_all_terms = request.POST.get('create_all_terms')

        # Create the first term calendar
        form = AcademicCalendarForm(request.POST)
        if form.is_valid():
            academic_calendar = form.save(commit=False)
           
            academic_calendar.term = '1'
            academic_calendar.save()

            # Create the remaining terms if 'create_all_terms' is checked
            if create_all_terms:
                for term_number in ['2', '3']:
                    new_calendar = AcademicCalendar(
                       
                        academic_year=academic_calendar.academic_year,
                        term=term_number,
                        start_date=academic_calendar.start_date,
                        end_date=academic_calendar.end_date,
                        is_current=False,
                    )
                    new_calendar.save()

            return redirect('create_holidays', academic_calendar.id) 
    else:
        form = AcademicCalendarForm()

    return render(request, 'district/create_academic_calendar.html', {
        'form': form
    })
    
    
  #--------------------------------------create_holidays------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_holidays(request, academic_calendar_id):
    # Retrieve the academic calendar instance
    academic_calendar = get_object_or_404(AcademicCalendar, pk=academic_calendar_id)
    
    HolidayFormFactory = modelformset_factory(Holiday, form=HolidayForm, extra=3)
    if request.method == 'POST':
        formset = HolidayFormFactory(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.academic_calendar = academic_calendar  # Set the academic calendar
                instance.save()
            return redirect('district_admin_dashboard')
    else:
        formset = HolidayFormFactory(queryset= Holiday.objects.none())

    return render(request, 'district/create_holidays.html', {'formset': formset,})


#-----------------------------------update_academic_calendar--------------------------------------------

    
@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def update_academic_calendar(request, pk):
    academic_calendar = get_object_or_404(AcademicCalendar, pk=pk)
    if request.method == 'POST':
        form = AcademicCalendarForm(request.POST, instance=academic_calendar)
        if form.is_valid():
            form.save()
            return redirect('academic_calendar_list')
    else:
        form = AcademicCalendarForm(instance=academic_calendar)
    return render(request, 'customsettings/update_academic_calendar.html', {'form': form})


#------------------------------------academic_calendar_details-------------------------------------    

    
def academic_calendar_details(request, academic_calendar_id):
    # Retrieve the academic calendar instance
    academic_calendar = get_object_or_404(AcademicCalendar, pk=academic_calendar_id)
    # Render the template with the academic calendar instance
    return render(request, 'customsettings/academic_calendar_details.html', {'academic_calendar': academic_calendar})


#-----------------------------------grade_level-----------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='district_admin').exists())
def grade_level(request):
    created_instances = []
    for choice in GradeLevel.GradeLevels.choices: 
        grade_level, created = GradeLevel.objects.get_or_create(grade_level=choice[0])
        if created:
            created_instances.append(f'Created GradeLevel instance for {choice[1]} ({choice[0]})')
        else:
            created_instances.append(f'GradeLevel instance for {choice[1]} ({choice[0]}) already exists')

    context = {
        'created_instances': created_instances
    }
    
    return render(request, 'district/grade_level.html', context)

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


@require_POST 
def logout_view(request):
    logout(request)
    return redirect('login')  


from teacher.models import TeacherProfile

def teacher_list_view(request):
    # Retrieve all teacher profiles
    teachers = TeacherProfile.objects.select_related('teacher', 'school', 'base_subject', 'assigned_class').all()

    # Get distinct schools and subjects
    distinct_schools = TeacherProfile.objects.values_list('school', 'school').distinct()
    distinct_subjects = TeacherProfile.objects.values_list('base_subject', 'base_subject').distinct()

    # Apply filters based on query parameters
    base_subject = request.GET.get('base_subject')
    school = request.GET.get('school')
    position = request.GET.get('position')
    assigned_class = request.GET.get('assigned_class')

    if base_subject:
        teachers = teachers.filter(base_subject__id=base_subject)
    if school:
        teachers = teachers.filter(school__id=school)
    if position:
        teachers = teachers.filter(position=position)
    if assigned_class:
        teachers = teachers.filter(assigned_class__id=assigned_class)

    # Render the results to the template
    context = {
        'teachers': teachers,
        'distinct_schools': distinct_schools,
        'distinct_subjects': distinct_subjects,
    }
    return render(request, 'district/all_teachers.html', context)