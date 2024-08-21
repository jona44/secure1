

from functools import wraps
from django.http import HttpResponseForbidden
from .utils import get_user_school

def filter_by_school(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        school = get_user_school(request.user)
        if school is None and not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this data.")
        request.school = school
        return view_func(request, *args, **kwargs)
    return _wrapped_view
