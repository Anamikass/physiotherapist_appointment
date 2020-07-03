from django.contrib import admin

# Register your models here.
from .models import state,city,area,patient_master,physio_master,degree,security_question,specialization,contact,treatment,appointment,sub_treatment

admin.site.register(state)
admin.site.register(city)
admin.site.register(area)
admin.site.register(patient_master)
admin.site.register(physio_master)
admin.site.register(degree)
admin.site.register(security_question)
admin.site.register(specialization)
admin.site.register(contact)
admin.site.register(treatment)
admin.site.register(appointment)
admin.site.register(sub_treatment)

# Changing admin header
admin.site.site_header = "Physio Plus Admin"