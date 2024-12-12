# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import forms

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient')])
    doctor_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Patient1(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    symptoms = models.TextField()
    notes = models.TextField(blank=True, null=True)
    diagnosis_status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the patient was added
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient1, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    symptoms = models.TextField(default='')
    def __str__(self):
        return f"Diagnosis Request for {self.patient.name}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',default=1)  # Assuming 'doctor' relates to the User model
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



