
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    risk_level = models.IntegerField()  # 1: High, 2: Medium, 3: Low
    ekg_data = models.FileField(upload_to='ekg_files/')

    def __str__(self):
        return f"{self.user.username} - Risk Level: {self.risk_level}"
