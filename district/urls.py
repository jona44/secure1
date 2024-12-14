from django.urls import path
from . import views
from . import calendar_views
from .views import logout_view
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    
    path('registration_complete/',views.registration_complete,name='registration_complete'),
    path('staff_profile_view/',views.staff_profile_view,name='staff_profile_view'),

    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('password_reset/',views.password_reset, name='password_reset'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='district/password_reset.html' ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='district/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='district/password_reset_confirm.html'
         ),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='district/password_reset_complete.html'),name='password_reset_complete'),
    
    path('activation-sent/',views.activation_sent, name='activation_sent'),

    path('schools/', views.school_list, name='school_list'),
    path('school_detail/<int:school_id>/', views.school_detail, name='school_detail'),
    path('create_school/', views.create_school, name='create_school'),
    path('create_district/', views.create_district, name='create_district'),
    path('subject/',views.create_subject,name='subject'),
    path('registration/', views.registration,name='registration'),
    
    path('create_schoolAdmin_profile/<int:user_id>/', views.create_schoolAdmin_profile, name='create_schoolAdmin_profile'),
    
    path('create_districtAdmin_profile/<int:user_id>/', views.create_districtAdmin_profile,name='create_districtAdmin_profile'),
    path('create_schoolHead_profile/<int:user_id>/', views.create_schoolHead_profile, name='create_schoolHead_profile'),

    path('schoolAdmin_profile_detail/<int:profile_id>/', views.schoolAdmin_profile_detail,name='schoolAdmin_profile_detail'),
    path('districtAdmin_profile_detail/<int:profile_id>/', views.districtAdmin_profile_detail,name='districtAdmin_profile_detail'),
    path('schoolHead_profile_detail/<int:profile_id>/', views.schoolHead_profile_detail,name='schoolHead_profile_detail'),
    path('create_academic_calendar/', views.create_academic_calendar, name='create_academic_calendar'),
    
    path('create_holidays/', calendar_views.create_holidays, name='create_holidays'),
    path('holiday_list/', calendar_views.holiday_list, name='holiday_list'),
    path('holidays/<int:pk>/edit/', calendar_views.holiday_update, name='holiday_update'),
    path('holidays/<int:pk>/delete/', calendar_views.holiday_delete, name='holiday_delete'),
    path('academic-calendars/', calendar_views.academic_calendar_list, name='academic_calendar_list'),
    path('create_academic_calendar', calendar_views.create_academic_calendar, name='create_academic_calendar'),
    path('academic-calendars/<int:pk>/edit/', calendar_views.academic_calendar_update, name='academic_calendar_update'),
    path('academic-calendars/<int:pk>/delete/', calendar_views.academic_calendar_delete, name='academic_calendar_delete'),
    
    # path('academic_calendar/<int:pk>/update/', views.update_academic_calendar, name='update_academic_calendar'),
    path('academic_calendar/<int:academic_calendar_id>/', views.academic_calendar_details, name='academic_calendar_details'),
    path('grade_level/', views.grade_level, name='grade_level'),
    
    path('teachers/', views.teacher_list_view, name='all_teachers'),

]