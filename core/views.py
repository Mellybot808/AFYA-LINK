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


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/patient_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if not hasattr(user, 'patient'):
            return context
            
        patient = user.patient
        
        # Medical info
        context['medical_conditions_count'] = MedicalHistory.objects.filter(patient=patient, status='active').count()
        context['allergies_count'] = Allergy.objects.filter(patient=patient).count()
        context['medications_count'] = Medication.objects.filter(patient=patient, is_active=True).count()
        context['severe_allergies'] = Allergy.objects.filter(patient=patient, severity='severe').count()
        
        # Appointments
        upcoming_apts = Appointment.objects.filter(patient=patient, appointment_date__gte=timezone.now()).select_related('doctor__user', 'hospital')
        context['appointments_count'] = upcoming_apts.count()
        context['upcoming_appointments'] = upcoming_apts[:5]
        
        # Billing
        bills = PatientBill.objects.filter(patient=patient)
        total_billed = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        paid_amount = Payment.objects.filter(bill__patient=patient, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_billed'] = f"KES {total_billed:,.0f}"
        context['amount_paid'] = f"KES {paid_amount:,.0f}"
        context['pending_amount'] = f"KES {total_billed - paid_amount:,.0f}"
        
        # Emergency contact
        context['primary_contact'] = EmergencyContact.objects.filter(patient=patient, is_primary=True).first()
        
        # Insurance
        context['insurance'] = PatientInsurance.objects.filter(patient=patient, status='active').first()
        
        # Blood type
        context['blood_type'] = patient.blood_type
        
        return context


class DoctorPortalView(LoginRequiredMixin, TemplateView):
    template_name = 'core/doctor_portal.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if not hasattr(user, 'doctor'):
            return context
            
        doctor = user.doctor
        
        # Appointment stats
        all_appointments = Appointment.objects.filter(doctor=doctor)
        context['total_patients'] = Patient.objects.filter(primary_doctor=doctor).count()
        context['appointments_today'] = all_appointments.filter(appointment_date__date=timezone.now().date()).count()
        context['total_appointments'] = all_appointments.count()
        context['completed_appointments'] = all_appointments.filter(status='completed').count()
        context['completion_rate'] = f"{(all_appointments.filter(status='completed').count() / all_appointments.count() * 100):.0f}%" if all_appointments.count() > 0 else "0%"
        
        # Prescription and lab test stats
        context['total_prescriptions'] = Prescription.objects.filter(doctor=doctor).count()
        context['total_lab_tests'] = LabTest.objects.filter(doctor=doctor).count()
        context['pending_lab_tests'] = LabTest.objects.filter(doctor=doctor, result_status__in=['pending', 'in_progress']).count()
        
        # Today's appointments
        today_apts = all_appointments.filter(appointment_date__date=timezone.now().date()).select_related('patient__user', 'hospital')[:5]
        context['today_appointments'] = today_apts
        
        # Revenue
        revenue = PatientBill.objects.filter(created_at__year=timezone.now().year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['ytd_revenue'] = f"KES {revenue:,.0f}"
        context['monthly_revenue'] = f"KES {revenue / 12:,.0f}"
        
        # Patients
        context['patients'] = Patient.objects.filter(primary_doctor=doctor)[:10]
        
        return context


class AdminReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/admin_reports.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Patient and doctor stats
        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        
        # Hospital stats
        hospital = Hospital.objects.first()
        context['total_beds'] = WardBed.objects.filter(hospital=hospital).count() if hospital else 0
        occupied_beds = WardBed.objects.filter(hospital=hospital, is_occupied=True).count() if hospital else 0
        total_beds = context['total_beds']
        context['occupancy_rate'] = f"{(occupied_beds / total_beds * 100):.1f}%" if total_beds > 0 else "0%"
        context['occupied_beds'] = occupied_beds
        
        # Financial stats
        bills = PatientBill.objects.all()
        total_billed = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        paid_amount = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_billed'] = f"KES {total_billed:,.0f}"
        context['total_revenue'] = f"KES {total_billed:,.0f}"
        context['amount_paid'] = f"KES {paid_amount:,.0f}"
        context['pending_amount'] = f"KES {total_billed - paid_amount:,.0f}"
        
        # Pharmacy alerts
        context['low_stock_items'] = PharmacyStock.objects.filter(quantity__lt=10).count()
        context['out_of_stock_items'] = PharmacyStock.objects.filter(quantity=0).count()
        
        # Department stats
        departments = Doctor.objects.values('specialization').annotate(count=Count('id'))
        context['departments'] = departments
        
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


# ============================================
# Analytics & Reports API Views
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_performance_report(request):
    """Get doctor performance metrics and statistics"""
    user = request.user
    
    if not hasattr(user, 'doctor'):
        return Response({'error': 'Doctor profile not found'}, status=404)
    
    doctor = user.doctor
    
    # Appointment statistics
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='completed').count()
    cancelled_appointments = Appointment.objects.filter(doctor=doctor, status='cancelled').count()
    pending_appointments = Appointment.objects.filter(doctor=doctor, status='pending').count()
    
    # Patient statistics
    unique_patients = Appointment.objects.filter(doctor=doctor).values('patient').distinct().count()
    
    # Revenue (from bills related to doctor's appointments)
    revenue = PatientBill.objects.filter(
        created_at__year=timezone.now().year
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Prescription statistics
    total_prescriptions = Prescription.objects.filter(doctor=doctor).count()
    active_prescriptions = Prescription.objects.filter(doctor=doctor, is_active=True).count()
    
    # Lab test statistics
    total_lab_tests = LabTest.objects.filter(doctor=doctor).count()
    completed_lab_tests = LabTest.objects.filter(doctor=doctor, result_status='completed').count()
    
    return Response({
        'doctor': {
            'id': doctor.id,
            'name': f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
            'specialization': doctor.specialization,
            'hospital': doctor.hospital.name,
            'license_number': doctor.license_number,
        },
        'appointments': {
            'total': total_appointments,
            'completed': completed_appointments,
            'pending': pending_appointments,
            'cancelled': cancelled_appointments,
            'completion_rate': f"{(completed_appointments / total_appointments * 100):.1f}%" if total_appointments > 0 else "0%",
        },
        'patients': {
            'total_unique': unique_patients,
        },
        'prescriptions': {
            'total': total_prescriptions,
            'active': active_prescriptions,
        },
        'lab_tests': {
            'total': total_lab_tests,
            'completed': completed_lab_tests,
        },
        'revenue': float(revenue),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hospital_analytics(request):
    """Get hospital-wide analytics and statistics"""
    user = request.user
    
    if not hasattr(user, 'doctor') and not user.is_staff:
        return Response({'error': 'Access denied'}, status=403)
    
    hospital = user.doctor.hospital if hasattr(user, 'doctor') else Hospital.objects.first()
    
    # Appointment statistics
    total_appointments = Appointment.objects.filter(hospital=hospital).count()
    completed_appointments = Appointment.objects.filter(hospital=hospital, status='completed').count()
    
    # Patient statistics
    total_patients = Patient.objects.filter(hospital=hospital).count()
    
    # Doctor statistics
    total_doctors = Doctor.objects.filter(hospital=hospital).count()
    
    # Revenue
    total_revenue = PatientBill.objects.filter(hospital=hospital).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    paid_revenue = Payment.objects.filter(bill__hospital=hospital, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_revenue = total_revenue - paid_revenue
    
    # Ward occupancy
    total_beds = WardBed.objects.filter(hospital=hospital).count()
    occupied_beds = WardBed.objects.filter(hospital=hospital, is_occupied=True).count()
    occupancy_rate = (occupied_beds / total_beds * 100) if total_beds > 0 else 0
    
    # Department stats
    departments = Doctor.objects.filter(hospital=hospital).values('specialization').annotate(count=Count('id'))
    
    return Response({
        'hospital': {
            'id': hospital.id,
            'name': hospital.name,
            'address': hospital.address,
            'phone': hospital.phone,
        },
        'appointments': {
            'total': total_appointments,
            'completed': completed_appointments,
        },
        'patients': {
            'total': total_patients,
        },
        'staff': {
            'total_doctors': total_doctors,
        },
        'revenue': {
            'total': float(total_revenue),
            'paid': float(paid_revenue),
            'pending': float(pending_revenue),
        },
        'ward_occupancy': {
            'total_beds': total_beds,
            'occupied_beds': occupied_beds,
            'occupancy_rate': f"{occupancy_rate:.1f}%",
        },
        'departments': [
            {
                'specialization': dept['specialization'],
                'doctor_count': dept['count'],
            } for dept in departments
        ],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pharmacy_inventory(request):
    """Get pharmacy inventory and stock levels"""
    user = request.user
    
    if not user.is_staff and not hasattr(user, 'doctor'):
        return Response({'error': 'Access denied'}, status=403)
    
    # All pharmacy stock
    stock_items = PharmacyStock.objects.all().order_by('-quantity')
    
    # Low stock items (less than 10 units)
    low_stock = PharmacyStock.objects.filter(quantity__lt=10)
    
    # Out of stock items
    out_of_stock = PharmacyStock.objects.filter(quantity=0)
    
    # Total inventory value
    total_value = sum([item.quantity * item.unit_price for item in stock_items])
    
    return Response({
        'summary': {
            'total_items': stock_items.count(),
            'low_stock_count': low_stock.count(),
            'out_of_stock_count': out_of_stock.count(),
            'total_inventory_value': float(total_value),
        },
        'inventory': [
            {
                'id': item.id,
                'medicine_name': item.medicine_name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'batch_number': item.batch_number,
                'expiry_date': item.expiry_date,
                'total_value': float(item.quantity * item.unit_price),
                'status': 'out_of_stock' if item.quantity == 0 else 'low_stock' if item.quantity < 10 else 'in_stock',
            } for item in stock_items
        ],
        'low_stock_alert': [
            {
                'id': item.id,
                'medicine_name': item.medicine_name,
                'current_quantity': item.quantity,
                'reorder_level': 10,
            } for item in low_stock
        ],
    })


# ============================================
# Data Export Views (PDF & CSV)
# ============================================

from django.http import HttpResponse, FileResponse
from io import BytesIO, StringIO
import csv
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_patient_records_pdf(request):
    """Export patient medical records as PDF"""
    user = request.user
    
    if not hasattr(user, 'patient'):
        return Response({'error': 'Patient profile not found'}, status=404)
    
    patient = user.patient
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f766e'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Title
    elements.append(Paragraph("MEDICAL RECORDS", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Info
    patient_info = f"""
    <b>Patient Name:</b> {patient.user.get_full_name()}<br/>
    <b>Date of Birth:</b> {patient.date_of_birth}<br/>
    <b>Blood Type:</b> {patient.blood_type}<br/>
    <b>Contact:</b> {patient.phone}<br/>
    <b>Report Date:</b> {timezone.now().strftime('%B %d, %Y')}
    """
    elements.append(Paragraph(patient_info, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Medical History
    medical_histories = MedicalHistory.objects.filter(patient=patient)
    if medical_histories.exists():
        elements.append(Paragraph("<b>Medical History</b>", styles['Heading2']))
        mh_data = [['Condition', 'Type', 'Status', 'Severity', 'Diagnosed Date']]
        for mh in medical_histories:
            mh_data.append([
                mh.condition_name,
                mh.condition_type,
                mh.status,
                mh.severity,
                mh.diagnosed_date.strftime('%b %d, %Y')
            ])
        mh_table = Table(mh_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1.2*inch])
        mh_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elements.append(mh_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Allergies
    allergies = Allergy.objects.filter(patient=patient)
    if allergies.exists():
        elements.append(Paragraph("<b>Allergies</b>", styles['Heading2']))
        allergy_data = [['Allergen', 'Type', 'Severity', 'Reaction']]
        for a in allergies:
            allergy_data.append([a.allergen, a.allergy_type, a.severity, a.reaction])
        allergy_table = Table(allergy_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
        allergy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5576c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(allergy_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Medications
    medications = Medication.objects.filter(patient=patient, is_active=True)
    if medications.exists():
        elements.append(Paragraph("<b>Current Medications</b>", styles['Heading2']))
        med_data = [['Medication', 'Dosage', 'Frequency', 'Start Date']]
        for med in medications:
            med_data.append([
                med.medication_name,
                med.dosage,
                med.frequency,
                med.start_date.strftime('%b %d, %Y')
            ])
        med_table = Table(med_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        med_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4facfe')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(med_table)
    
    # Build PDF
    doc.build(elements)
    
    # Return PDF as response
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="medical_records_{patient.user.username}.pdf"'
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_patient_bills_pdf(request):
    """Export patient bills as PDF"""
    user = request.user
    
    if not hasattr(user, 'patient'):
        return Response({'error': 'Patient profile not found'}, status=404)
    
    patient = user.patient
    bills = PatientBill.objects.filter(patient=patient).select_related('hospital').prefetch_related('items')
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f766e'),
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph("BILLING SUMMARY", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    total_billed = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    paid = Payment.objects.filter(bill__patient=patient, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    summary_info = f"""
    <b>Patient:</b> {patient.user.get_full_name()}<br/>
    <b>Total Billed:</b> KES {total_billed:,.2f}<br/>
    <b>Amount Paid:</b> KES {paid:,.2f}<br/>
    <b>Outstanding:</b> KES {total_billed - paid:,.2f}<br/>
    <b>Report Date:</b> {timezone.now().strftime('%B %d, %Y')}
    """
    elements.append(Paragraph(summary_info, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Bills table
    bill_data = [['Bill #', 'Hospital', 'Amount', 'Status', 'Due Date']]
    for bill in bills:
        bill_data.append([
            bill.bill_number,
            bill.hospital.name,
            f"KES {bill.total_amount:,.2f}",
            bill.status.upper(),
            bill.due_date.strftime('%b %d, %Y') if bill.due_date else 'N/A'
        ])
    
    bill_table = Table(bill_data, colWidths=[1*inch, 2*inch, 1.5*inch, 1*inch, 1.2*inch])
    bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(bill_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="billing_summary_{patient.user.username}.pdf"'
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_appointments_csv(request):
    """Export appointments as CSV"""
    user = request.user
    
    if not hasattr(user, 'patient') and not hasattr(user, 'doctor'):
        return Response({'error': 'Patient or Doctor profile not found'}, status=404)
    
    # Get appointments based on user role
    if hasattr(user, 'patient'):
        appointments = Appointment.objects.filter(patient=user.patient).select_related('doctor__user', 'hospital')
    else:
        appointments = Appointment.objects.filter(doctor=user.doctor).select_related('patient__user', 'hospital')
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="appointments_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    if hasattr(user, 'patient'):
        writer.writerow(['Doctor', 'Hospital', 'Date', 'Time', 'Type', 'Status', 'Reason'])
        for apt in appointments:
            writer.writerow([
                f"Dr. {apt.doctor.user.get_full_name()}",
                apt.hospital.name,
                apt.appointment_date.strftime('%Y-%m-%d'),
                apt.appointment_date.strftime('%H:%M'),
                apt.appointment_type,
                apt.status,
                apt.reason or 'N/A'
            ])
    else:
        writer.writerow(['Patient', 'Hospital', 'Date', 'Time', 'Type', 'Status', 'Reason'])
        for apt in appointments:
            writer.writerow([
                apt.patient.user.get_full_name(),
                apt.hospital.name,
                apt.appointment_date.strftime('%Y-%m-%d'),
                apt.appointment_date.strftime('%H:%M'),
                apt.appointment_type,
                apt.status,
                apt.reason or 'N/A'
            ])
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_prescriptions_csv(request):
    """Export prescriptions as CSV"""
    user = request.user
    
    if not hasattr(user, 'patient') and not hasattr(user, 'doctor'):
        return Response({'error': 'Patient or Doctor profile not found'}, status=404)
    
    # Get prescriptions
    if hasattr(user, 'patient'):
        prescriptions = Prescription.objects.filter(patient=user.patient).select_related('doctor__user', 'hospital')
    else:
        prescriptions = Prescription.objects.filter(doctor=user.doctor).select_related('patient__user', 'hospital')
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="prescriptions_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    if hasattr(user, 'patient'):
        writer.writerow(['Doctor', 'Hospital', 'Date', 'Active', 'Medications'])
        for rx in prescriptions:
            meds = ', '.join([item.medication for item in rx.items.all()])
            writer.writerow([
                f"Dr. {rx.doctor.user.get_full_name()}",
                rx.hospital.name,
                rx.prescribed_date.strftime('%Y-%m-%d'),
                'Yes' if rx.is_active else 'No',
                meds or 'N/A'
            ])
    else:
        writer.writerow(['Patient', 'Hospital', 'Date', 'Active', 'Medications'])
        for rx in prescriptions:
            meds = ', '.join([item.medication for item in rx.items.all()])
            writer.writerow([
                rx.patient.user.get_full_name(),
                rx.hospital.name,
                rx.prescribed_date.strftime('%Y-%m-%d'),
                'Yes' if rx.is_active else 'No',
                meds or 'N/A'
            ])
