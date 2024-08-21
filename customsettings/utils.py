

from district.models import SchoolAdminProfile

def get_user_school(user):
    if user.is_school_superuser:
        return None
    try:
        return SchoolAdminProfile.objects.get(user=user).school
    except SchoolAdminProfile.DoesNotExist:
        return None
