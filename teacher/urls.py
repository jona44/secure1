from django.urls import path
from .import views

urlpatterns = [
    path('create_teacher_profile/<int:user_id>/', views.create_teacher_profile, name='create_teacher_profile'),
    path('update_teacher_profile/<int:pk>/',views.update_teacher_profile,name='update_teacher_profile'),
    path('view_teacher_profile/<int:pk>/',views.view_teacher_profile,name='view_teacher_profile'),
    path('teacher_list/',views.teacher_list, name='teacher_list')

]
