from django.urls import path
from .import views


urlpatterns = [
    path('update_schoolprofile/<int:pk>/', views.update_schoolprofile, name='update_schoolprofile'),
    path('school_profile_create_step1/', views.school_profile_create_step1, name='school_profile_create_step1'),
    path('schoolprofile_details/<int:id>/', views.schoolprofile_details, name='schoolprofile_details'),
   
    path('class_name/', views.class_name, name='class_name'),
    path('setup_step7/', views.setup_step7, name='setup_step7'),
    path('create_schoolsubjects_step2/',views.create_schoolsubjects_step2,name='create_schoolsubjects_step2'),
    path('subject_list/',views.subject_list,name='subject_list'),
    path('edit_schoolsubjects/<int:pk>/', views.edit_schoolsubjects, name='edit_schoolsubjects'),
   
]
