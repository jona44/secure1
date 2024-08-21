from django.contrib import admin


from customsettings.models import SchoolProfile,SchoolSubject,GradeLevel,ClassName

# Register your models here.
admin.site.register(SchoolProfile)
admin.site.register(SchoolSubject)
admin.site.register(GradeLevel)
admin.site.register(ClassName)
