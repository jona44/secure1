from django.contrib import admin

from student.models import *

admin.site.register(StudentProfile)
admin.site.register(ClassRoom)
admin.site.register(Attendance)


