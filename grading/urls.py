from django.urls import path
from .import views

urlpatterns = [
    path('capture/<int:subject_id>/',views.capture,name='capture'),

    path('edit_capture/<int:capture_id>/', views.edit_capture, name='edit_capture'),
    path('getmark/<int:captured_classroom_id>/', views.getmark, name='getmark'),
    path('success_page/<int:captured_classroom_id>/', views.success_page, name='success_page'),
   
    path('editmark/<int:getmark_id>/<int:student_id>/', views.editmark, name='editmark'),
    path('student_grades/<int:student_id>/<int:subject_id>/', views.student_grades, name='student_grades'),
    path('student_report/<int:student_id>/',views.student_report,name='student_report'),
    path('captured_classroom/<int:capture_id>/', views.captured_classroom, name='captured_classroom'),
    # path('no_captured_classroom/', views.captured_classroom, name='no_captured_classroom'),

]
