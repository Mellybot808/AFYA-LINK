from rest_framework import serializers
from .models import (
    Doctor, Patient, Hospital, HealthRecord, Medic, VisitRequest, Visit, 
    Appointment, Notification, LabTest, LabResult, Prescription, PrescriptionItem,
    PharmacyStock, PharmacyDispensing, PatientBill, BillItem, Payment, VitalSigns,
    Triage, WardBed, PatientCheckIn, Queue, MedicalHistory, Allergy, Medication,
    EmergencyContact, PatientInsurance, InsuranceClaim
)

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

# Medic Home Visit Serializers
class MedicSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Medic
        fields = ['id', 'user', 'license_number', 'specialty', 'hospital', 'phone', 'location_lat', 'location_lng', 'is_available', 'verified']

class VisitRequestSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = VisitRequest
        fields = ['id', 'patient', 'symptoms', 'location_lat', 'location_lng', 'preferred_time', 'urgency_level', 'status', 'created_at', 'notes']

class VisitSerializer(serializers.ModelSerializer):
    request = VisitRequestSerializer(read_only=True)
    medic = MedicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = ['id', 'request', 'medic', 'scheduled_time', 'status', 'arrival_time', 'completion_time', 'diagnosis', 'treatment', 'follow_up_required', 'notes']

# Patient Portal Serializers
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'hospital', 'scheduled_time', 'status', 'reason', 'notes', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'notification_type', 'is_read', 'created_at', 'related_object_id']

# Laboratory Serializers
class LabTestSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = LabTest
        fields = ['id', 'patient', 'doctor', 'hospital', 'test_name', 'test_type', 'description', 'ordered_at', 'expected_completion', 'status', 'priority']

class LabResultSerializer(serializers.ModelSerializer):
    lab_test = LabTestSerializer(read_only=True)

    class Meta:
        model = LabResult
        fields = ['id', 'lab_test', 'result_value', 'reference_range', 'notes', 'completed_at', 'technician_name']

# Pharmacy Serializers
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'drug_name', 'dosage', 'frequency', 'duration', 'quantity', 'instructions']

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'hospital', 'created_at', 'status', 'notes', 'items']

class PharmacyStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyStock
        fields = ['id', 'drug_name', 'dosage', 'quantity_available', 'price', 'expiry_date', 'supplier', 'last_restocked']

class PharmacyDispensingSerializer(serializers.ModelSerializer):
    prescription_item = PrescriptionItemSerializer(read_only=True)
    pharmacy_stock = PharmacyStockSerializer(read_only=True)

    class Meta:
        model = PharmacyDispensing
        fields = ['id', 'prescription_item', 'pharmacy_stock', 'quantity_dispensed', 'dispensed_at', 'dispensed_by', 'status', 'receipt_number']

# Billing Serializers
class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ['id', 'description', 'category', 'quantity', 'unit_price', 'total_price']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'bill', 'amount', 'payment_method', 'reference_number', 'payment_date', 'receipt_number']

class PatientBillSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    items = BillItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = PatientBill
        fields = ['id', 'patient', 'hospital', 'bill_number', 'created_at', 'total_amount', 'paid_amount', 'status', 'due_date', 'notes', 'items', 'payments']

# Triage/Nursing Serializers
class VitalSignsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = VitalSigns
        fields = ['id', 'patient', 'recorded_at', 'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'height', 'recorded_by']

class TriageSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    vital_signs = VitalSignsSerializer(read_only=True)

    class Meta:
        model = Triage
        fields = ['id', 'patient', 'hospital', 'vital_signs', 'chief_complaint', 'priority_level', 'assessment', 'recommended_action', 'triaged_at', 'triaged_by']

class WardBedSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    current_patient = PatientSerializer(read_only=True)

    class Meta:
        model = WardBed
        fields = ['id', 'hospital', 'ward_name', 'bed_number', 'bed_type', 'status', 'current_patient', 'admission_date']

# Reception Serializers
class PatientCheckInSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = PatientCheckIn
        fields = ['id', 'patient', 'hospital', 'check_in_time', 'check_out_time', 'purpose', 'notes']

class QueueSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    current_patient = PatientSerializer(read_only=True)

    class Meta:
        model = Queue
        fields = ['id', 'hospital', 'queue_name', 'current_patient', 'position', 'estimated_wait_time']

# Additional Serializers for New Models

# Medical History Serializers
class MedicalHistorySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    treating_physician = DoctorSerializer(read_only=True)

    class Meta:
        model = MedicalHistory
        fields = ['id', 'patient', 'condition_name', 'condition_type', 'diagnosed_date', 'status', 'severity', 'notes', 'treating_physician', 'created_at', 'updated_at']

class AllergySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Allergy
        fields = ['id', 'patient', 'allergen', 'allergy_type', 'severity', 'reaction', 'notes', 'created_at']

class MedicationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    prescribed_by = DoctorSerializer(read_only=True)

    class Meta:
        model = Medication
        fields = ['id', 'patient', 'medication_name', 'dosage', 'frequency', 'start_date', 'end_date', 'is_active', 'prescribed_by', 'pharmacy', 'notes', 'created_at']

# Emergency Contact Serializer
class EmergencyContactSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = EmergencyContact
        fields = ['id', 'patient', 'name', 'relationship', 'phone_number', 'alternate_phone', 'email', 'address', 'is_primary', 'can_make_medical_decisions', 'created_at']

# Patient Insurance Serializers
class PatientInsuranceSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = PatientInsurance
        fields = ['id', 'patient', 'provider_name', 'policy_number', 'group_number', 'coverage_type', 'coverage_start_date', 'coverage_end_date', 'status', 'coverage_percentage', 'annual_limit', 'deductible', 'primary_holder_name', 'relationship_to_holder', 'verification_status', 'notes', 'created_at', 'updated_at']

class InsuranceClaimSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    insurance = PatientInsuranceSerializer(read_only=True)
    provider = HospitalSerializer(read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = ['id', 'patient', 'insurance', 'claim_number', 'claim_date', 'service_date', 'provider', 'diagnosis', 'procedure_code', 'total_billed_amount', 'approved_amount', 'patient_responsibility', 'status', 'notes', 'processed_date', 'created_at']
