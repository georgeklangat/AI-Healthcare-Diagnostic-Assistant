from django.db import models
from django.contrib.auth.models import User

class PatientCase(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    symptoms = models.TextField()
    diagnosis_results = models.JSONField(null=True, blank=True)  # To store AI predictions


    def __str__(self):
        return f"{self.name} ({self.age}, {self.gender})"
