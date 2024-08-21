

from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def get_dashboard_url(user):
    if user.groups.filter(name='student').exists():
        return reverse('high_level_dashboard')
    elif user.groups.filter(name='staff').exists():
        return reverse('teacher_dashboard')
    elif user.groups.filter(name='school_admin').exists():
        return reverse('school_admin_dashboard')
    elif user.groups.filter(name='deputy_head').exists():
        return reverse('deputy_head_dashboard')
    elif user.groups.filter(name='school_head').exists():
        return reverse('school_head_dashboard')
    else:
        return reverse('default_dashboard')
