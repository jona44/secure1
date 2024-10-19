from district.models import SchoolAdminProfile, SchoolHeadProfile
from teacher.models import TeacherProfile
from student.models import StudentProfile

def get_user_school_profile(user):
    try:
        if user.user_type == 'student':
            return StudentProfile.objects.get(student=user).school
        elif user.user_type == 'teacher':
            return TeacherProfile.objects.get(teacher=user).school
        elif user.user_type == 'school_admin':
            return SchoolAdminProfile.objects.get(school_admin=user).school
        elif user.user_type == 'school_head':
            return SchoolHeadProfile.objects.get(user=user).school
        
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist,
            SchoolAdminProfile.DoesNotExist, SchoolHeadProfile.DoesNotExist
            ) as e:
        # Handle the case where the profile does not exist
        return None
    return None

def school_profile(request):
    if request.user.is_authenticated:
        profile = get_user_school_profile(request.user)
        if profile:
            return {'school_profile': profile}
    return {}


