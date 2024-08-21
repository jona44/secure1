from django.shortcuts import redirect, render
from customsettings.forms import SchoolSubjectForm
from customsettings.models import SchoolProfile



def create_schoolsubjects(request):
    user_profile = request.user.school_admin_profile
    school = user_profile.school

    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data['subjects']
            school_name_instance, created = SchoolProfile.objects.get_or_create(school=user_profile)

            for subject in subjects:
                school_subject = SchoolSubjects.objects.create(school=school_name_instance) # type: ignore
                school_subject.subjects.add(subject)
                school_subject.save()

            return redirect('subject_list')  # Replace with your success URL
    else:
        form = SchoolSubjectForm()

    return render(request, 'customsettings/schoolsubjects_form.html', {'form':form})




# def __init__(self, *args, **kwargs):
#         assigned_school = kwargs.pop('assigned_school', None)
#         super().__init__(*args, **kwargs)
#         if assigned_school:
#             school_profile = SchoolProfile.objects.filter(school_name=assigned_school).first()
#             if school_profile:
#                 self.fields['subjects_taught'].queryset = school_profile.school_subjects.all()
#                 self.fields['base_subject'].queryset = school_profile.school_subjects.all()



# <div class="row m-4  justify-content-center">
#     <div class="col-md-8 ">
#       <h1 class="text-primary text-center">Create Teacher Profile</h1>
#       <form method="post" action="{% url 'create_teacher_profile' user_id %}">
#             {% csrf_token %}
#             <div class="form-group m-2">
#                 <h5 class="text-primary">assigned_school:</h5>
#                 {{ form.assigned_school }}
#             </div>
#             <div class="form-group m-2">
#                 <h5 class="text-primary">Contact Number:</h5>
#                 {{ form.contact_number }}
#             </div>
#             <div class="form-group m-2">
#                 <h5 class="text-primary">assigned_class:</h5>
#                 {{ form.assigned_class }}
#             </div>
#             <div class="row justify-content-center">
#                 <div class="col-md">
#                   <div class="form-group  flex-wrap align-items-center gap-2 m-2">
#                     <h5 class="text-primary text-center">Classes Taught:</h5>
#                     <div class="col-md d-flex flex-wrap bg1 p-4  rounded">
#                         {% for checkbox in form.classes_taught %}
#                         <div class="form-check p-3 ">
#                             {{ checkbox }} Grade
#                         </div>
#                         {% endfor %}
#                      </div>
#                    </div>
#                 </div>
#               </div>
#             <div class="form-group m-2 ">
#                 <h5 class="text-primary">Base Subject:</h5>
#                 {{ form.base_subject }}
#             </div>
#             <div class="form-group m-2">
#                 <h5 class="text-primary">Subjects Taught:</h5><br>
#                 <div class="col-md d-flex flex-wrap bg1 p-4 m-2 rounded">
#                 {% for checkbox in form.subjects_taught %}
#                 &nbsp;&nbsp; <div class="form-check">
#                     &nbsp;&nbsp;{{ checkbox }}
                       
#                     </div>
#                 {% endfor %}
#                 </div>
#             </div>
#             <button type="submit" class="btn btn-primary">Submit</button>
#         </form>
#    </div>
# </div>
