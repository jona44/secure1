from django.urls import path

from . import views

urlpatterns = [
    path('student_registration/', views.student_registration, name='student_registration'),
    path('create_student_profile/<int:user_id>/', views.create_student_profile, name='create_student_profile'),
    path('student_details/<int:pk>/',views.student_details, name='student_details'),
    path('edit_student_profile/<int:pk>/', views.edit_student_profile, name='edit_student_profile'),
    path('classrooms',views.classrooms,name='classrooms'),
    path('create_classroom/',views.create_classroom,name='create_classroom'),
    path('classroom_details/<int:pk>/',views.classroom_details,name='classroom_details'),
    path('edit_classroom/<int:pk>',views.edit_classroom,name='edit_classroom'),
   
    path('assign_classroom/<int:pk>/',views.assign_classroom, name='assign_classroom'),
    path('select-classroom/<int:pk>/<int:grade_level_id>/', views.select_classroom, name='select_classroom'),
    path('attendance/<int:classroom_id>/', views.attendance, name='attendance'),
    path('attendance_record/<int:classroom_id>/', views.attendance_record, name='attendance_record'),
    path('student_attendance/<int:student_id>/', views.student_attendance, name='student_attendance'),
    path('students_list/',views.students_list,name='students_list'),
    
    path('create_activity/', views.create_activity, name='create_activity'),
    path('activity_list/', views.activity_list, name='activity_list'),
    path('join-activity/<int:student_profile_id>/', views.join_activity, name='join_activity'),
    path('activity/<int:activity_id>/members/', views.activity_members_list, name='activity_members_list'),
    
    path('transfer-student/<int:pk>/', views.transfer_student, name='transfer_student'),
    path('student/undo-transfer/<int:pk>/', views.undo_transfer, name='undo_transfer'),
    path('suspense-pool/', views.suspense_pool, name='suspense_pool'),
    path('accept-student/<int:student_profile_id>/', views.accept_student, name='accept_student'),

    

]