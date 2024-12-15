from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Patient, EKG, MedicalReport
from django.urls import path
from django.shortcuts import render, redirect
from django.db.models import Q

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.site_header = "ECG management system"
admin.site.site_title = "ECG management system"
admin.site.index_title = ""

admin.site.register(Patient)
@admin.register(EKG)
class EKGAdmin(admin.ModelAdmin):
    list_filter = ('patient__risk_level',)    

    def changelist_view(self, request, extra_context=None):
        if not request.GET:
            ekg_in_queue = EKG.objects.filter(status=1)
            ekg_completed = EKG.objects.filter(status=2)
            high_risk_ekg_list = ekg_in_queue.filter(patient__risk_level=1)
            medium_risk_ekg_list = ekg_in_queue.filter(patient__risk_level=2)
            low_risk_ekg_list = ekg_in_queue.filter(patient__risk_level=3)


            context = {
                'title': 'EKG Dashboard',
                'ekg_in_queue': ekg_in_queue,
                'ekg_completed': ekg_completed,
                'high_risk_ekg_list': high_risk_ekg_list, 
                'medium_risk_ekg_list': medium_risk_ekg_list, 
                'low_risk_ekg_list': low_risk_ekg_list,
            }


            if extra_context:
                context.update(extra_context)

            return render(request, 'ekg_app/ekg_dashboard.html', context)
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(MedicalReport)