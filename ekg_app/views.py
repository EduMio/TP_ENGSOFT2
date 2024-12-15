
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
def patient_dashboard(request):
    patients = Patient.objects.all().order_by('risk_level')
    return render(request, 'ekg_app/dashboard.html', {{ 'patients': patients }})