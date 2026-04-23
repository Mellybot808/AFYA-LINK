from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import Doctor, Patient, Hospital, HealthRecord
from .serializers import DoctorSerializer, PatientSerializer, HospitalSerializer, HealthRecordSerializer

class HomeView(TemplateView):
    template_name = 'core/index.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'patient'):
            patient = user.patient
            context.update({
                'patient': patient,
                'records': patient.records.all()[:10],
                'primary_doctor': patient.primary_doctor,
            })
        elif hasattr(user, 'doctor'):
            doctor = user.doctor
            context.update({
                'doctor': doctor,
                'patients': Patient.objects.filter(primary_doctor=doctor),
            })
        return context

class APIFrontendView(LoginRequiredMixin, TemplateView):
    template_name = 'core/api_frontend.html'
    login_url = 'login'
    redirect_field_name = 'next'

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.select_related('hospital', 'user').all()
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patient.objects.select_related('hospital', 'primary_doctor__hospital', 'user').all()
    serializer_class = PatientSerializer

class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class HealthRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthRecord.objects.select_related('patient__user').all()
    serializer_class = HealthRecordSerializer
