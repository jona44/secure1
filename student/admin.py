from django.contrib import admin


from student.models import AcademicRecord,ClassRoom,ExtraCurricularActivity,Attendance,StudentProfile

admin.site.register(StudentProfile)
admin.site.register(ClassRoom)
admin.site.register(Attendance)
admin.site.register(ExtraCurricularActivity)
admin.site.register(AcademicRecord)



