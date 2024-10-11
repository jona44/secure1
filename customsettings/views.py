import datetime
from pyexpat.errors import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from district.forms import SubjectForm
from .forms import *
from .models import *
from district.models import AcademicCalendar, District_School_Registration, GradeLevel, SchoolAdminProfile,Subjects
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import filter_by_school # type: ignore



@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def school_profile_create_step1(request):
    """
    Handles the creation and updating of a school profile.
    Only allows one school profile per registered school.
    """
    # Get the SchoolAdminProfile associated with the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)

    # Get the registered school related to the logged-in school admin
    registered_school = school_admin_profile.assigned_school_name

    # Try to get an existing school profile for this school
    try:
        school_profile = SchoolProfile.objects.get(school=registered_school)
    except SchoolProfile.DoesNotExist:
        school_profile = None

    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES, instance=school_profile)  # Include request.FILES
        if form.is_valid():
            schoolprofile = form.save(commit=False)

            # Automatically set the school from the logged-in school admin's profile
            schoolprofile.school = registered_school

            schoolprofile.save()  # Save the SchoolProfile instance first
            # Assign many-to-many relationships
            selected_subjects_ids = form.cleaned_data.get('school_subjects')
            if selected_subjects_ids:
                schoolprofile.school_subjects.set(selected_subjects_ids)
            schoolprofile.save()
            return redirect('schoolprofile_details', id=schoolprofile.id)  # Redirect to a success page or another step
        else:
            print("Form is invalid:")
            print(form.errors)
    else:
        form = SchoolProfileForm(instance=school_profile)

    return render(request, 'customsettings/school_profile_form_step1.html', {
        'form': form,
        'registered_school': registered_school
    })
    
#---------------------------------schoolprofile_details------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def schoolprofile_details(request, id):
    # Get the SchoolAdminProfile associated with the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # Get the registered school related to the logged-in school admin
    registered_school = school_admin_profile.assigned_school_name
    print(registered_school)
    # Get the school profile associated with the registered school and the provided ID
    schoolprofile = get_object_or_404(SchoolProfile, school=registered_school, id=id)
    print(schoolprofile)
    return render(request, 'customsettings/schoolprofile_details.html', {'schoolprofile': schoolprofile})


#---------------------------------update_schoolprofile--------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def update_schoolprofile(request, pk):
    schoolprofile = get_object_or_404(SchoolProfile, pk=pk)
    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES, instance=schoolprofile)
        if form.is_valid():
            form.save()
            return redirect('schoolprofile_details',id=schoolprofile.id)
    else:
        form = SchoolProfileForm(instance=schoolprofile)
    return render(request, 'customsettings/update_schoolprofile.html', {'form': form})


#-----------------------------------create_schoolsubjects_step2------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def create_schoolsubjects_step2(request):
    """
    Handles the creation of SchoolSubject instances for a specific school.

    Ensures each SchoolSubject instance is created per subject.
    """
    # Get the school admin profile for the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # Get the registered school related to the logged-in school admin
    registered_school = school_admin_profile.assigned_school_name

    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data['school_subjects']
            
            try:
                school_profile = SchoolProfile.objects.get(school=registered_school)
            except SchoolProfile.DoesNotExist:
                return render(request, 'customsettings/error.html', {'message': 'School profile does not exist.'})

            # Delete existing SchoolSubject instances for this school profile
            SchoolSubject.objects.filter(schoolprofile_name=school_profile).delete()

            # Create new SchoolSubject instances for each subject
            for subject in subjects:
                school_subject = SchoolSubject.objects.create(schoolprofile_name=school_profile)
                school_subject.subjects.set([subject])
                school_subject.save()

            return redirect('subject_list')
    else:
        form = SchoolSubjectForm()

    return render(request, 'customsettings/create_schoolsubjects_step2.html', {'form': form})


#-----------------------------------subject_list------------------------------------------

def subject_list(request):
    # Get the school admin profile for the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # Get the registered school related to the logged-in school admin
    current_school = school_admin_profile.assigned_school_name
    school  = SchoolProfile.objects.get(school=current_school)
    all_subjects = SchoolSubject.objects.filter(schoolprofile_name=school)
    print("All Subjects:", all_subjects)  # Debugging line
    for school_subject in all_subjects:
        print("School Subject:", school_subject)
        for subject in school_subject.subjects.all():
            print("Subject:", subject)
    return render(request, 'customsettings/subject_list.html', {'all_subjects': all_subjects})


#-------------------------- edit_schoolsubjects------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def edit_schoolsubjects(request, pk):
    school_subject = SchoolSubject.objects.get(pk=pk)

    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST, instance=school_subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # Replace with your success URL
    else:
        form = SchoolSubjectForm(instance=school_subject)

    return render(request, 'customsettings/edit_schoolsubjects.html', {'form': form})


#-----------------------------------ClassName----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def class_name(request):
    """
    View to manually create class names based on GradeLevels and SchoolName
    """
    # Retrieve the SchoolAdminProfile for the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    school = school_admin_profile.school  # This should be a SchoolProfile instance
    registered_school = SchoolProfile.objects.filter(school=school).first()
                                               # Ensure there's a current academic year defined
    try:
        academic_year = AcademicCalendar.objects.get(is_current=True)
    except AcademicCalendar.DoesNotExist:
        messages.error(request, "No current academic year found. Please define one.")
        return redirect('class_name')  # Or handle the error differently

    if request.method == 'POST':
        form = ClassNameForm(request.POST)
        if form.is_valid():
            grade_level = form.cleaned_data['grd_level']
            classname = form.cleaned_data['classname']

            # Check if the class name already exists for the combination
            existing_class = ClassName.objects.filter(
                schoolprofile=registered_school,
                grd_level=grade_level,
                classname=classname,
                academic_year=academic_year
            ).first()

            if existing_class:
                messages.error(request, "Class name already exists.")
            else:
                new_class = ClassName(
                    schoolprofile=registered_school,
                    grd_level=grade_level,
                    classname=classname,
                    academic_year=academic_year
                )
                new_class.save()
                messages.success(request, "Class name has been created successfully.")
                return redirect('class_name')
    else:
        form = ClassNameForm()
        allclasses = ClassName.objects.filter(schoolprofile=registered_school)
    return render(request, 'customsettings/class_name.html', {'form': form, 'allclasses':allclasses})

#-----------------------------------is_setup_complete------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def setup_step7(request):
    try:
        # Get the SchoolAdminProfile associated with the current user
        school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
        registered_school = school_admin_profile.assigned_school_name
        # Retrieve the existing SchoolName instance associated with the SchoolAdminProfile
        try:
            school = SchoolProfile.objects.get(school=registered_school)
        except SchoolProfile.DoesNotExist:
            # Handle the case where no SchoolName instance exists
            return render(request, 'customsettings/setup_step6.html', {
                'error': 'No SchoolName instance found for the current SchoolAdminProfile.'
            })
        
        if request.method == 'POST':
            school.is_setup_complete = True
            school.save()
            return redirect('school_admin_dashboard')
    
    except SchoolAdminProfile.DoesNotExist:
        # Handle the case where the SchoolAdminProfile does not exist
        return render(request, 'customsettings/setup_step6.html', {
            'error': 'SchoolAdminProfile not found for the current user.'
        })

    return render(request, 'customsettings/setup_step7.html')
