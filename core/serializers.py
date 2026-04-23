from rest_framework import serializers
from .models import Doctor, Patient, Hospital, HealthRecord

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'phone']

class DoctorSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialty', 'hospital']

class PatientSerializer(serializers.ModelSerializer):
    primary_doctor = DoctorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'date_of_birth', 'phone', 'primary_doctor', 'hospital']

class HealthRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = HealthRecord
        fields = ['id', 'patient', 'created_at', 'diagnosis', 'notes', 'data']
