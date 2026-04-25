from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework import viewsets, permissions
from .models import (
    Doctor, Patient, Hospital, HealthRecord, Medic, VisitRequest, Visit, Appointment, 
    Notification, LabTest, LabResult, Prescription, PrescriptionItem, PharmacyStock, 
    PharmacyDispensing, PatientBill, BillItem, Payment, VitalSigns, Triage, WardBed,
    PatientCheckIn, Queue, MedicalHistory, Allergy, Medication, EmergencyContact,
    PatientInsurance, InsuranceClaim
)
from .serializers import (
    DoctorSerializer, PatientSerializer, HospitalSerializer, HealthRecordSerializer, 
    MedicSerializer, VisitRequestSerializer, VisitSerializer, AppointmentSerializer, 
    NotificationSerializer, LabTestSerializer, LabResultSerializer, PrescriptionSerializer,
    PrescriptionItemSerializer, PharmacyStockSerializer, PharmacyDispensingSerializer,
    PatientBillSerializer, BillItemSerializer, PaymentSerializer, VitalSignsSerializer,
    TriageSerializer, WardBedSerializer, PatientCheckInSerializer, QueueSerializer,
    MedicalHistorySerializer, AllergySerializer, MedicationSerializer,
    EmergencyContactSerializer, PatientInsuranceSerializer, InsuranceClaimSerializer
)

class HomeView(TemplateView):
    template_name = 'core/index.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

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
                'appointments': patient.appointments.all()[:5],
                'notifications': user.notifications.filter(is_read=False)[:5],
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

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('hospital', 'user').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('hospital', 'primary_doctor__hospital', 'user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAuthenticated]

class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.select_related('patient__user').all()
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicViewSet(viewsets.ModelViewSet):
    queryset = Medic.objects.select_related('hospital', 'user').all()
    serializer_class = MedicSerializer
    permission_classes = [permissions.IsAuthenticated]

class VisitRequestViewSet(viewsets.ModelViewSet):
    queryset = VisitRequest.objects.select_related('patient__user').all()
    serializer_class = VisitRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related('request__patient__user', 'medic__user').all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient__user', 'doctor__user', 'hospital').all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.select_related('patient__user', 'doctor__user', 'hospital').all()
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticated]

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.select_related('lab_test').all()
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient__user', 'doctor__user', 'hospital').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class PharmacyStockViewSet(viewsets.ModelViewSet):
    queryset = PharmacyStock.objects.all()
    serializer_class = PharmacyStockSerializer
    permission_classes = [permissions.IsAuthenticated]

class PharmacyDispensingViewSet(viewsets.ModelViewSet):
    queryset = PharmacyDispensing.objects.select_related('prescription_item', 'pharmacy_stock').all()
    serializer_class = PharmacyDispensingSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientBillViewSet(viewsets.ModelViewSet):
    queryset = PatientBill.objects.select_related('patient__user', 'hospital').all()
    serializer_class = PatientBillSerializer
    permission_classes = [permissions.IsAuthenticated]

class BillItemViewSet(viewsets.ModelViewSet):
    queryset = BillItem.objects.all()
    serializer_class = BillItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.select_related('patient__user').all()
    serializer_class = VitalSignsSerializer
    permission_classes = [permissions.IsAuthenticated]

class TriageViewSet(viewsets.ModelViewSet):
    queryset = Triage.objects.select_related('patient__user', 'hospital', 'vital_signs').all()
    serializer_class = TriageSerializer
    permission_classes = [permissions.IsAuthenticated]

class WardBedViewSet(viewsets.ModelViewSet):
    queryset = WardBed.objects.select_related('hospital', 'current_patient__user').all()
    serializer_class = WardBedSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientCheckInViewSet(viewsets.ModelViewSet):
    queryset = PatientCheckIn.objects.select_related('patient__user', 'hospital').all()
    serializer_class = PatientCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]

class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.select_related('hospital', 'current_patient__user').all()
    serializer_class = QueueSerializer
    permission_classes = [permissions.IsAuthenticated]

# Additional ViewSets for New Models

# Medical History ViewSets
class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.select_related('patient__user', 'treating_physician__user').all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.select_related('patient__user').all()
    serializer_class = AllergySerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.select_related('patient__user', 'prescribed_by__user').all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Emergency Contact ViewSet
class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.select_related('patient__user').all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]

# Patient Insurance ViewSets
class PatientInsuranceViewSet(viewsets.ModelViewSet):
    queryset = PatientInsurance.objects.select_related('patient__user').all()
    serializer_class = PatientInsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]

class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.select_related('patient__user', 'insurance', 'provider').all()
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAuthenticated]


# ============================================
# Patient Portal API Views
# ============================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_portal_summary(request):
    """Get patient portal summary - medical history, appointments, billing"""
    user = request.user
    
    if not hasattr(user, 'patient'):
        return Response({'error': 'Patient profile not found'}, status=404)
    
    patient = user.patient
    
    # Medical History Summary
    medical_histories = MedicalHistory.objects.filter(patient=patient)
    allergies = Allergy.objects.filter(patient=patient)
    medications = Medication.objects.filter(patient=patient, is_active=True)
    
    # Upcoming Appointments
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=timezone.now()
    ).select_related('doctor__user', 'hospital').order_by('appointment_date')[:10]
    
    # Past Appointments
    past_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__lt=timezone.now()
    ).select_related('doctor__user', 'hospital').order_by('-appointment_date')[:5]
    
    # Billing Summary
    bills = PatientBill.objects.filter(patient=patient)
    total_billed = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    paid_amount = Payment.objects.filter(bill__patient=patient, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_amount = total_billed - paid_amount
    
    # Active Prescriptions
    prescriptions = Prescription.objects.filter(
        patient=patient,
        is_active=True
    ).select_related('doctor__user', 'hospital')[:10]
    
    # Emergency Contacts
    emergency_contacts = EmergencyContact.objects.filter(patient=patient)
    primary_contact = emergency_contacts.filter(is_primary=True).first()
    
    # Insurance Info
    insurances = PatientInsurance.objects.filter(patient=patient, status='active')
    active_insurance = insurances.first()
    
    return Response({
        'patient': {
            'id': patient.id,
            'name': f"{patient.user.first_name} {patient.user.last_name}",
            'email': patient.user.email,
            'phone': patient.phone,
            'date_of_birth': patient.date_of_birth,
            'blood_type': patient.blood_type,
        },
        'medical_history': {
            'conditions_count': medical_histories.count(),
            'active_conditions': medical_histories.filter(status='active').count(),
            'allergies_count': allergies.count(),
            'severe_allergies': allergies.filter(severity='severe').count(),
            'active_medications': medications.count(),
        },
        'appointments': {
            'upcoming': [
                {
                    'id': apt.id,
                    'doctor': f"Dr. {apt.doctor.user.first_name} {apt.doctor.user.last_name}",
                    'specialization': apt.doctor.specialization,
                    'hospital': apt.hospital.name,
                    'date': apt.appointment_date,
                    'status': apt.status,
                    'type': apt.appointment_type,
                } for apt in upcoming_appointments
            ],
            'past': [
                {
                    'id': apt.id,
                    'doctor': f"Dr. {apt.doctor.user.first_name} {apt.doctor.user.last_name}",
                    'hospital': apt.hospital.name,
                    'date': apt.appointment_date,
                    'status': apt.status,
                } for apt in past_appointments
            ],
        },
        'billing': {
            'total_billed': float(total_billed),
            'paid': float(paid_amount),
            'pending': float(pending_amount),
            'unpaid_bills': bills.filter(status='pending').count(),
        },
        'prescriptions': [
            {
                'id': rx.id,
                'doctor': f"Dr. {rx.doctor.user.first_name} {rx.doctor.user.last_name}",
                'hospital': rx.hospital.name,
                'date': rx.prescribed_date,
                'is_active': rx.is_active,
                'items_count': rx.items.count(),
            } for rx in prescriptions
        ],
        'emergency_contact': {
            'name': primary_contact.name if primary_contact else None,
            'relationship': primary_contact.relationship if primary_contact else None,
            'phone': primary_contact.phone_number if primary_contact else None,
            'can_make_decisions': primary_contact.can_make_medical_decisions if primary_contact else False,
        } if primary_contact else None,
        'insurance': {
            'provider': active_insurance.provider_name if active_insurance else None,
            'policy_number': active_insurance.policy_number if active_insurance else None,
            'coverage_type': active_insurance.coverage_type if active_insurance else None,
            'coverage_percentage': active_insurance.coverage_percentage if active_insurance else None,
            'status': active_insurance.status if active_insurance else None,
        } if active_insurance else None,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_medical_records(request):
    """Get detailed patient medical records"""
    user = request.user
    
    if not hasattr(user, 'patient'):
        return Response({'error': 'Patient profile not found'}, status=404)
    
    patient = user.patient
    
    # Medical History
    medical_histories = MedicalHistory.objects.filter(
        patient=patient
    ).select_related('treating_physician__user').order_by('-diagnosed_date')
    
    # Allergies
    allergies = Allergy.objects.filter(patient=patient)
    
    # Medications (all, not just active)
    medications = Medication.objects.filter(
        patient=patient
    ).select_related('prescribed_by__user').order_by('-start_date')
    
    # Vital Signs history
    vital_signs = VitalSigns.objects.filter(
        patient=patient
    ).order_by('-recorded_at')[:20]
    
    return Response({
        'medical_history': [
            {
                'id': mh.id,
                'condition_name': mh.condition_name,
                'condition_type': mh.condition_type,
                'diagnosed_date': mh.diagnosed_date,
                'status': mh.status,
                'severity': mh.severity,
                'notes': mh.notes,
                'treating_physician': f"Dr. {mh.treating_physician.user.first_name} {mh.treating_physician.user.last_name}" if mh.treating_physician else None,
            } for mh in medical_histories
        ],
        'allergies': [
            {
                'id': a.id,
                'allergen': a.allergen,
                'allergy_type': a.allergy_type,
                'severity': a.severity,
                'reaction': a.reaction,
                'notes': a.notes,
            } for a in allergies
        ],
        'medications': [
            {
                'id': med.id,
                'medication_name': med.medication_name,
                'dosage': med.dosage,
                'frequency': med.frequency,
                'start_date': med.start_date,
                'end_date': med.end_date,
                'is_active': med.is_active,
                'prescribed_by': f"Dr. {med.prescribed_by.user.first_name} {med.prescribed_by.user.last_name}" if med.prescribed_by else None,
            } for med in medications
        ],
        'vital_signs': [
            {
                'id': vs.id,
                'recorded_at': vs.recorded_at,
                'blood_pressure_systolic': vs.blood_pressure_systolic,
                'blood_pressure_diastolic': vs.blood_pressure_diastolic,
                'heart_rate': vs.heart_rate,
                'temperature': vs.temperature,
                'respiratory_rate': vs.respiratory_rate,
                'oxygen_saturation': vs.oxygen_saturation,
                'weight': vs.weight,
                'height': vs.height,
            } for vs in vital_signs
        ],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_billing_details(request):
    """Get detailed patient billing information"""
    user = request.user
    
    if not hasattr(user, 'patient'):
        return Response({'error': 'Patient profile not found'}, status=404)
    
    patient = user.patient
    
    # All bills with items
    bills = PatientBill.objects.filter(
        patient=patient
    ).select_related('hospital').prefetch_related('items').order_by('-created_at')
    
    # Payments
    payments = Payment.objects.filter(
        bill__patient=patient
    ).select_related('bill').order_by('-payment_date')
    
    # Insurance claims
    claims = InsuranceClaim.objects.filter(
        patient=patient
    ).order_by('-claim_date')
    
    return Response({
        'bills': [
            {
                'id': bill.id,
                'bill_number': bill.bill_number,
                'hospital': bill.hospital.name,
                'total_amount': float(bill.total_amount),
                'status': bill.status,
                'created_at': bill.created_at,
                'due_date': bill.due_date,
                'items': [
                    {
                        'description': item.description,
                        'quantity': item.quantity,
                        'unit_price': float(item.unit_price),
                        'total_price': float(item.total_price),
                    } for item in bill.items.all()
                ],
            } for bill in bills
        ],
        'payments': [
            {
                'id': pay.id,
                'bill_number': pay.bill.bill_number,
                'amount': float(pay.amount),
                'payment_method': pay.payment_method,
                'status': pay.status,
                'payment_date': pay.payment_date,
                'transaction_id': pay.transaction_id,
            } for pay in payments
        ],
        'insurance_claims': [
            {
                'id': claim.id,
                'claim_number': claim.claim_number,
                'claim_date': claim.claim_date,
                'service_date': claim.service_date,
                'provider': claim.provider.name if claim.provider else None,
                'diagnosis': claim.diagnosis,
                'total_billed_amount': float(claim.total_billed_amount),
                'approved_amount': float(claim.approved_amount) if claim.approved_amount else None,
                'patient_responsibility': float(claim.patient_responsibility) if claim.patient_responsibility else None,
                'status': claim.status,
            } for claim in claims
        ],
    })
