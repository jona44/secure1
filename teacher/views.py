from django.shortcuts import render, redirect, get_object_or_404
from customsettings.models import AcademicCalendar, SchoolProfile
from district.models import District_School_Registration, SchoolAdminProfile
from student.models import ClassRoom
from .forms import *
from .models import TeacherProfile
from customadmin.models import CustomUser 
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type in ['district_admin', 'school_admin'])
def create_teacher_profile(request, user_id):
    teacher = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                teacher_profile = form.save(commit=False)
                teacher_profile.teacher = teacher

                academic_year = AcademicCalendar.objects.get(is_current=True)
                teacher_profile.academic_year = academic_year

                teacher_profile.save()

                teacher_profile.classes_taught.set(form.cleaned_data['classes_taught'])
                teacher_profile.subjects_taught.set(form.cleaned_data['subjects_taught'])

            return redirect('view_teacher_profile', pk=teacher_profile.pk)
    else:
        form = TeacherProfileForm()

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
        assigned_school = school_admin.assigned_school_name
        all_teachers = TeacherProfile.objects.filter(assigned_school=assigned_school)
    except SchoolAdminProfile.DoesNotExist:
        all_teachers = None  # Or handle the case where the user is not a school admin

    context = {
        'all_teachers':all_teachers,
        'school_admin': school_admin if all_teachers else None,  # Pass the school admin if teachers exist
    }
    
    return render(request, 'teacher/teacher_list.html', {'all_teachers': all_teachers})
