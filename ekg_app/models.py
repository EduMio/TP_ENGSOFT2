import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validate_cpf(value):
    cpf_pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    if not re.match(cpf_pattern, value):
        raise ValidationError("CPF deve estar no formato ###.###.###-##.")

class Patient(models.Model):
    RISK_LEVEL_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low')
    ]
    id_patient = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)
    cpf = models.CharField(
        max_length=14,
        validators=[validate_cpf], 
        unique=True  
    )
    birth_date = models.DateField() 
    risk_level = models.IntegerField(choices=RISK_LEVEL_CHOICES, default=3)

    def __str__(self):
        return f"{self.name} - Risk Level: {self.risk_level}"
    
class EKG(models.Model):
    STATUS_CHOICES = [
        (1, 'In queue'),
        (2, 'Completed'),
    ]
     
    id_ekg = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ekg_data = models.FileField(upload_to='ekg_files/')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    motive = models.TextField()
    comorbidities = models.TextField()
    medications = models.TextField()
    symptoms = models.TextField()
    observations = models.TextField()
    
    def __str__(self):
        return (f"Paciente: {self.patient.name} - Grau de risco: {self.patient.risk_level} - "
                f"Status: {self.status} - Motivo: {self.motive}")

class MedicalReport(models.Model):
    ekg = models.ForeignKey(EKG, on_delete=models.CASCADE)
    heart_rate = models.TextField()
    p_wave = models.TextField()
    pr_interval = models.TextField()
    qrs_complex = models.TextField()
    qt_interval = models.TextField()
    conclusions = models.TextField()
    
    def save(self, *args, **kwargs):
        self.ekg.status = 2 
        self.ekg.save()
        super().save(*args, **kwargs)  

    def __str__(self):
        return (f"Report of {self.ekg.patient.name} - Heart Rate: {self.heart_rate}, "
                f"P Wave: {self.p_wave}, PR Interval: {self.pr_interval}, "
                f"QRS Complex: {self.qrs_complex}, QT Interval: {self.qt_interval}")

