from django.contrib import admin


from student.models import AcademicRecord,ClassRoom,ExtraCurricularActivity,Attendance,StudentProfile,StudentSchoolHistory

admin.site.register(StudentProfile)
admin.site.register(ClassRoom)
admin.site.register(Attendance)
admin.site.register(ExtraCurricularActivity)
admin.site.register(AcademicRecord)
admin.site.register(StudentSchoolHistory)



