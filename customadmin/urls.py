from django.urls import path
from .import views



urlpatterns = [
    path('', views.dashboard,name='dashbard'),

    path('dashboard/student/', views.dashboard, name='student_dashboard'),
    path('dashboard/staff/', views.dashboard, name='teacher_dashboard'),
    path('dashboard/school_admin/', views.dashboard, name='school_admin_dashboard'),
    path('dashboard/deputy_head/', views.dashboard, name='deputy_head_dashboard'),
    path('dashboard/school_head/', views.dashboard, name='school_head_dashboard'),
    path('dashboard/district_admin/', views.dashboard, name='district_admin_dashboard'),
    path('default_dashboard/', views.dashboard, name='default_dashboard'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('logout_redirect/', views.login_redirect, name='logout_redirect'),


]