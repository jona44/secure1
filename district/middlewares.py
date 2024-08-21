# middlewares.py in the 'District' app
from django.utils.deprecation import MiddlewareMixin
import logging

from district.models import SchoolAdminProfile

logger = logging.getLogger(__name__)

class SetSchoolInSessionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.session.get('school_id'):
            try:
                school_admin = SchoolAdminProfile.objects.get(admin=request.user)
                request.session['school_id'] = school_admin.school.id
            except SchoolAdminProfile.DoesNotExist:
                logger.warning(f"SchoolAdminProfile does not exist for user {request.user}")
            except SchoolAdminProfile.MultipleObjectsReturned:
                logger.error(f"Multiple SchoolAdminProfiles found for user {request.user}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")