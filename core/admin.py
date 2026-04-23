from django.contrib import admin
from .models import Doctor, Patient, Hospital, HealthRecord

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'hospital')
    search_fields = ('user__username', 'specialty')
    list_filter = ('hospital',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'primary_doctor', 'hospital')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('hospital',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'created_at')
    search_fields = ('patient__user__username', 'diagnosis')
    list_filter = ('created_at',)
