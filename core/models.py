from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=120)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - {self.specialty}'

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    primary_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, related_name='records', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Record {self.id} for {self.patient}'
