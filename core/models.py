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

# Medic Home Visit Models
class Medic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    specialty = models.CharField(max_length=120)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=50)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Medic {self.user.get_full_name() or self.user.username} - {self.specialty}'

class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptoms = models.TextField()
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    preferred_time = models.DateTimeField(null=True, blank=True)
    urgency_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Visit Request {self.id} by {self.patient}'

class Visit(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('en_route', 'En Route'),
        ('arrived', 'Arrived'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request = models.OneToOneField(VisitRequest, on_delete=models.CASCADE)
    medic = models.ForeignKey(Medic, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    arrival_time = models.DateTimeField(null=True, blank=True)
    completion_time = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Visit {self.id} for {self.request.patient} by {self.medic}'

# Patient Portal Models
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return f'Appointment {self.id}: {self.patient} with {self.doctor} at {self.scheduled_time}'

class Notification(models.Model):
    TYPE_CHOICES = [
        ('appointment_reminder', 'Appointment Reminder'),
        ('appointment_confirmed', 'Appointment Confirmed'),
        ('appointment_cancelled', 'Appointment Cancelled'),
        ('test_results', 'Test Results Available'),
        ('prescription_ready', 'Prescription Ready'),
        ('visit_scheduled', 'Home Visit Scheduled'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)  # For linking to appointments, etc.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user}: {self.title}'

# Laboratory Module
class LabTest(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ordered_tests')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    test_type = models.CharField(max_length=100)  # e.g., "Blood Test", "Urine Test", "X-Ray"
    description = models.TextField(blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    expected_completion = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium')

    class Meta:
        ordering = ['-ordered_at']

    def __str__(self):
        return f'{self.test_name} for {self.patient} - {self.status}'

class LabResult(models.Model):
    lab_test = models.OneToOneField(LabTest, on_delete=models.CASCADE, related_name='result')
    result_value = models.TextField()
    reference_range = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    technician_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Result for {self.lab_test.test_name}'

# Pharmacy Module
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Prescription for {self.patient} by {self.doctor}'

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    drug_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)  # e.g., "500mg", "10ml"
    frequency = models.CharField(max_length=100)  # e.g., "Twice daily", "Every 8 hours"
    duration = models.CharField(max_length=100)  # e.g., "7 days", "2 weeks"
    quantity = models.IntegerField()
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f'{self.drug_name} - {self.dosage}'

class PharmacyStock(models.Model):
    drug_name = models.CharField(max_length=255, unique=True)
    dosage = models.CharField(max_length=100)
    quantity_available = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=255, blank=True)
    last_restocked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.drug_name} - {self.dosage} (Stock: {self.quantity_available})'

class PharmacyDispensing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
        ('returned', 'Returned'),
    ]
    
    prescription_item = models.ForeignKey(PrescriptionItem, on_delete=models.CASCADE)
    pharmacy_stock = models.ForeignKey(PharmacyStock, on_delete=models.SET_NULL, null=True)
    quantity_dispensed = models.IntegerField()
    dispensed_at = models.DateTimeField(auto_now_add=True)
    dispensed_by = models.CharField(max_length=255)  # Pharmacist name
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'Dispensing #{self.receipt_number}'

# Billing Module
class PatientBill(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Bill #{self.bill_number} for {self.patient}'

class BillItem(models.Model):
    bill = models.ForeignKey(PatientBill, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)  # e.g., "Doctor Consultation", "Lab Test", "Medication"
    category = models.CharField(max_length=50, choices=[('consultation', 'Consultation'), ('test', 'Test'), ('medication', 'Medication'), ('procedure', 'Procedure'), ('other', 'Other')])
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.description} - {self.total_price}'

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('insurance', 'Insurance'),
        ('mpesa', 'M-Pesa'),
        ('other', 'Other'),
    ]
    
    bill = models.ForeignKey(PatientBill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'Payment {self.receipt_number} - {self.amount}'

# Triage / Nursing Module
class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    recorded_at = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius")
    blood_pressure_systolic = models.IntegerField(help_text="Systolic pressure (mmHg)")
    blood_pressure_diastolic = models.IntegerField(help_text="Diastolic pressure (mmHg)")
    heart_rate = models.IntegerField(help_text="Beats per minute")
    respiratory_rate = models.IntegerField(help_text="Breaths per minute")
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, help_text="SpO2 percentage")
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Height in m")
    recorded_by = models.CharField(max_length=255)  # Nurse name

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f'Vital Signs for {self.patient} - {self.recorded_at}'

class Triage(models.Model):
    PRIORITY_CHOICES = [
        ('emergency', 'Emergency'),
        ('urgent', 'Urgent'),
        ('semi_urgent', 'Semi-Urgent'),
        ('routine', 'Routine'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='triages')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    vital_signs = models.ForeignKey(VitalSigns, on_delete=models.SET_NULL, null=True, blank=True)
    chief_complaint = models.TextField()
    priority_level = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='routine')
    assessment = models.TextField(blank=True)
    recommended_action = models.CharField(max_length=255, blank=True)  # e.g., "Admit", "See Doctor", "Go Home"
    triaged_at = models.DateTimeField(auto_now_add=True)
    triaged_by = models.CharField(max_length=255)  # Nurse name

    class Meta:
        ordering = ['-triaged_at']

    def __str__(self):
        return f'Triage for {self.patient} - {self.priority_level}'

class WardBed(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='beds')
    ward_name = models.CharField(max_length=100)  # e.g., "Pediatrics Ward", "ICU", "General Ward"
    bed_number = models.CharField(max_length=20)
    bed_type = models.CharField(max_length=50, choices=[('single', 'Single'), ('double', 'Double'), ('isolation', 'Isolation')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('hospital', 'ward_name', 'bed_number')

    def __str__(self):
        return f'{self.ward_name} - Bed {self.bed_number}'

# Reception Module
class PatientCheckIn(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='check_ins')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=255, blank=True)  # e.g., "Follow-up", "New Patient"
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-check_in_time']

    def __str__(self):
        return f'Check-In: {self.patient} at {self.check_in_time}'

class Queue(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    queue_name = models.CharField(max_length=100)  # e.g., "Doctor Queue", "Lab Queue"
    current_patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.IntegerField(default=0)
    estimated_wait_time = models.IntegerField(help_text="Estimated time in minutes")

    def __str__(self):
        return f'{self.queue_name} at {self.hospital.name}'

# AI Symptom Checker Module
class Symptom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    severity_levels = models.CharField(max_length=255, default="mild, moderate, severe")
    category = models.CharField(max_length=100, choices=[
        ('respiratory', 'Respiratory'),
        ('cardiovascular', 'Cardiovascular'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('neurological', 'Neurological'),
        ('musculoskeletal', 'Musculoskeletal'),
        ('skin', 'Skin'),
        ('general', 'General'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PossibleCondition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low - Mild'),
        ('medium', 'Medium - Moderate'),
        ('high', 'High - Severe'),
        ('critical', 'Critical - Emergency'),
    ], default='medium')
    recommended_action = models.CharField(max_length=255)  # e.g., "Consult Doctor", "Go to ER"
    requires_emergency = models.BooleanField(default=False)
    common_symptoms = models.ManyToManyField(Symptom, related_name='conditions')

    def __str__(self):
        return self.name

class SymptomCheckerSession(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='symptom_sessions', null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    symptoms_selected = models.ManyToManyField(Symptom, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    possible_conditions = models.ManyToManyField(PossibleCondition, blank=True)
    severity_assessment = models.CharField(max_length=20, blank=True)
    doctor_referral_recommended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Symptom Check Session {self.session_id}'

# Decision Support for Clinicians Module
class ClinicalGuideline(models.Model):
    title = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    description = models.TextField()
    diagnostic_criteria = models.TextField()
    treatment_recommendations = models.TextField()
    medication_options = models.TextField(blank=True)
    follow_up_protocol = models.TextField(blank=True)
    evidence_level = models.CharField(max_length=50, choices=[
        ('strong', 'Strong Evidence'),
        ('moderate', 'Moderate Evidence'),
        ('weak', 'Weak Evidence'),
    ])
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PatientRiskAssessment(models.Model):
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='risk_assessments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='risk_assessments')
    assessment_date = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='medium')
    risk_factors = models.TextField()  # Identified risk factors
    predicted_outcomes = models.TextField(blank=True)
    recommendations = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # 0.0 to 1.0

    class Meta:
        ordering = ['-assessment_date']

    def __str__(self):
        return f'Risk Assessment for {self.patient} - {self.condition}'

class DiagnosticSuggestion(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diagnostic_suggestions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition_suspected = models.CharField(max_length=255)
    suggested_tests = models.TextField()  # Comma-separated or JSON
    rationale = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT'),
    ], default='routine')
    generated_at = models.DateTimeField(auto_now_add=True)
    doctor_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Diagnostic Suggestion for {self.patient}'

# Chatbot Module
class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # emoji or icon name

    def __str__(self):
        return self.name

class FAQQuestion(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    keywords = models.CharField(max_length=255, blank=True)  # comma-separated for search
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-helpful_count', '-created_at']

    def __str__(self):
        return self.question[:100]

class ChatbotConversation(models.Model):
    INTENT_CHOICES = [
        ('appointment', 'Appointment'),
        ('insurance', 'Insurance Query'),
        ('health_info', 'Health Information'),
        ('billing', 'Billing'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbot_conversations', null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    intent = models.CharField(max_length=50, choices=INTENT_CHOICES, default='general')
    user_message = models.TextField()
    bot_response = models.TextField()
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    was_helpful = models.BooleanField(null=True, blank=True)  # User feedback
    created_at = models.DateTimeField(auto_now_add=True)
    escalated_to_human = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Chat {self.session_id}'

class AppointmentReminder(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='reminder')
    reminder_sent = models.BooleanField(default=False)
    reminder_date = models.DateTimeField()  # When to send reminder
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=50, choices=[
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('notification', 'In-App Notification'),
    ], default='notification')

    def __str__(self):
        return f'Reminder for {self.appointment}'

class InsuranceInfo(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('coverage', 'Coverage'),
        ('claims', 'Claims Process'),
        ('eligibility', 'Eligibility'),
        ('providers', 'Providers'),
        ('general', 'General'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Additional Models for Extended Functionality

# Medical History Module
class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition_name = models.CharField(max_length=255)
    condition_type = models.CharField(max_length=50, choices=[
        ('chronic', 'Chronic'),
        ('acute', 'Acute'),
        ('hereditary', 'Hereditary'),
        ('environmental', 'Environmental'),
    ])
    diagnosed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('managed', 'Managed'),
        ('monitoring', 'Under Monitoring'),
    ], default='active')
    severity = models.CharField(max_length=20, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ], blank=True)
    notes = models.TextField(blank=True)
    treating_physician = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='treated_conditions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.condition_name} - {self.patient}'

class Allergy(models.Model):
    ALLERGY_TYPE_CHOICES = [
        ('medication', 'Medication'),
        ('food', 'Food'),
        ('environmental', 'Environmental'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('life_threatening', 'Life Threatening'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=255)
    allergy_type = models.CharField(max_length=20, choices=ALLERGY_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    reaction = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.allergen} allergy - {self.patient}'

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    pharmacy = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.medication_name} - {self.patient}'

# Emergency Contact Module
class EmergencyContact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('child', 'Child'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    phone_number = models.CharField(max_length=50)
    alternate_phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    can_make_medical_decisions = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.relationship}) - {self.patient}'

# Patient Insurance Module
class PatientInsurance(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending Verification'),
        ('suspended', 'Suspended'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurances')
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    group_number = models.CharField(max_length=100, blank=True)
    coverage_type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('family', 'Family'),
        ('group', 'Group'),
    ])
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    annual_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deductible = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    primary_holder_name = models.CharField(max_length=255, blank=True)
    relationship_to_holder = models.CharField(max_length=50, blank=True)
    verification_status = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.provider_name} - {self.policy_number} ({self.patient})'

class InsuranceClaim(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('partial', 'Partial Payment'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_claims')
    insurance = models.ForeignKey(PatientInsurance, on_delete=models.CASCADE, related_name='claims')
    claim_number = models.CharField(max_length=50, unique=True)
    claim_date = models.DateField()
    service_date = models.DateField()
    provider = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    procedure_code = models.CharField(max_length=50, blank=True)
    total_billed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    patient_responsibility = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    notes = models.TextField(blank=True)
    processed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-claim_date']

    def __str__(self):
        return f'Claim #{self.claim_number} - {self.patient}'
