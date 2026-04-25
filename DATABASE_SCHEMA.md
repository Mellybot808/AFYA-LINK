# AfyaLink Database Schema Overview

## Core Entities

### User Management
```
User (Django Auth)
├── username
├── email
├── password
└── is_staff, is_active
```

### Facility Management
```
Hospital
├── name
├── address
├── phone
└── relationships:
    ├── doctors (reverse ForeignKey)
    ├── patients (reverse ForeignKey)
    ├── beds (reverse ForeignKey)
    └── queues (reverse ForeignKey)
```

```
Doctor
├── user (OneToOne User)
├── specialty
├── hospital (ForeignKey)
└── relationships:
    ├── appointments (reverse ForeignKey)
    ├── prescriptions (reverse ForeignKey)
    ├── lab_orders (reverse ForeignKey)
    └── triages (reverse ForeignKey)
```

```
Patient
├── user (OneToOne User)
├── date_of_birth
├── phone
├── primary_doctor (ForeignKey Doctor)
├── hospital (ForeignKey)
└── relationships:
    ├── appointments (reverse ForeignKey)
    ├── records (reverse ForeignKey)
    ├── prescriptions (reverse ForeignKey)
    ├── lab_tests (reverse ForeignKey)
    ├── vital_signs (reverse ForeignKey)
    ├── triages (reverse ForeignKey)
    ├── bills (reverse ForeignKey)
    ├── check_ins (reverse ForeignKey)
    └── visit_requests (reverse ForeignKey)
```

## Module-Specific Models

### Patient Portal
```
Appointment
├── patient (ForeignKey)
├── doctor (ForeignKey)
├── hospital (ForeignKey)
├── scheduled_time
├── status (scheduled, confirmed, in_progress, completed, cancelled, no_show)
├── reason
└── notes

Notification
├── user (ForeignKey User)
├── title
├── message
├── notification_type (appointment_reminder, test_results, prescription_ready, etc.)
├── is_read
├── created_at
└── related_object_id (for linking to specific events)
```

### Home Visit Module
```
Medic
├── user (OneToOne User)
├── license_number
├── specialty
├── hospital (ForeignKey)
├── phone
├── location_lat (decimal)
├── location_lng (decimal)
├── is_available (bool)
└── verified (bool)

VisitRequest
├── patient (ForeignKey)
├── symptoms
├── location_lat (decimal)
├── location_lng (decimal)
├── preferred_time (datetime)
├── urgency_level (low, medium, high)
├── status (pending, assigned, in_progress, completed, cancelled)
├── created_at
└── notes

Visit
├── request (OneToOne VisitRequest)
├── medic (ForeignKey)
├── scheduled_time
├── status (scheduled, en_route, arrived, in_progress, completed, cancelled)
├── arrival_time
├── completion_time
├── diagnosis
├── treatment
├── follow_up_required (bool)
└── notes
```

### Laboratory Module
```
LabTest
├── patient (ForeignKey)
├── doctor (ForeignKey)
├── hospital (ForeignKey)
├── test_name
├── test_type (Blood Test, Urine Test, X-Ray, etc.)
├── description
├── ordered_at
├── expected_completion
├── status (ordered, in_progress, completed, cancelled)
├── priority (low, medium, high, urgent)
└── relationship:
    └── result (OneToOne LabResult)

LabResult
├── lab_test (OneToOne)
├── result_value
├── reference_range
├── notes
├── completed_at
└── technician_name
```

### Pharmacy Module
```
Prescription
├── patient (ForeignKey)
├── doctor (ForeignKey)
├── hospital (ForeignKey)
├── created_at
├── status (active, completed, cancelled)
├── notes
└── relationships:
    └── items (reverse ForeignKey PrescriptionItem)

PrescriptionItem
├── prescription (ForeignKey)
├── drug_name
├── dosage (e.g., "500mg")
├── frequency (e.g., "Twice daily")
├── duration (e.g., "7 days")
├── quantity
└── instructions

PharmacyStock
├── drug_name
├── dosage
├── quantity_available
├── price
├── expiry_date
├── supplier
└── last_restocked

PharmacyDispensing
├── prescription_item (ForeignKey)
├── pharmacy_stock (ForeignKey)
├── quantity_dispensed
├── dispensed_at
├── dispensed_by
├── status (pending, dispensed, returned)
└── receipt_number
```

### Billing Module
```
PatientBill
├── patient (ForeignKey)
├── hospital (ForeignKey)
├── bill_number (unique)
├── created_at
├── total_amount (decimal)
├── paid_amount (decimal)
├── status (draft, pending, partially_paid, paid, overdue, cancelled)
├── due_date
├── notes
└── relationships:
    ├── items (reverse ForeignKey BillItem)
    └── payments (reverse ForeignKey Payment)

BillItem
├── bill (ForeignKey)
├── description
├── category (consultation, test, medication, procedure, other)
├── quantity
├── unit_price
└── total_price

Payment
├── bill (ForeignKey)
├── amount
├── payment_method (cash, card, bank_transfer, insurance, mpesa, other)
├── reference_number
├── payment_date
└── receipt_number (unique)
```

### Triage/Nursing Module
```
VitalSigns
├── patient (ForeignKey)
├── recorded_at
├── temperature (celsius)
├── blood_pressure_systolic (mmHg)
├── blood_pressure_diastolic (mmHg)
├── heart_rate (bpm)
├── respiratory_rate (bpm)
├── oxygen_saturation (%)
├── weight (kg)
├── height (m)
└── recorded_by

Triage
├── patient (ForeignKey)
├── hospital (ForeignKey)
├── appointment (ForeignKey, nullable)
├── vital_signs (ForeignKey, nullable)
├── chief_complaint
├── priority_level (emergency, urgent, semi_urgent, routine)
├── assessment
├── recommended_action
├── triaged_at
└── triaged_by

WardBed
├── hospital (ForeignKey)
├── ward_name
├── bed_number
├── bed_type (single, double, isolation)
├── status (available, occupied, reserved, maintenance)
├── current_patient (ForeignKey, nullable)
└── admission_date
```

### Reception Module
```
PatientCheckIn
├── patient (ForeignKey)
├── hospital (ForeignKey)
├── appointment (ForeignKey, nullable)
├── check_in_time
├── check_out_time
├── purpose
└── notes

Queue
├── hospital (ForeignKey)
├── queue_name (e.g., "Doctor Queue")
├── current_patient (ForeignKey, nullable)
├── position
└── estimated_wait_time (minutes)
```

## Health Records
```
HealthRecord
├── patient (ForeignKey)
├── created_at
├── diagnosis
├── notes
└── data (JSON field for flexible storage)
```

## Relationships Summary

### One-to-One (User Types)
- Doctor ↔ User
- Patient ↔ User
- Medic ↔ User
- LabResult ↔ LabTest
- Visit ↔ VisitRequest

### Foreign Keys (Many-to-One)
- Doctor → Hospital
- Patient → Doctor (primary)
- Patient → Hospital
- Appointment → Patient
- Appointment → Doctor
- Appointment → Hospital
- Notification → User
- VisitRequest → Patient
- Visit → Medic
- LabTest → Patient/Doctor/Hospital
- Prescription → Patient/Doctor/Hospital
- PrescriptionItem → Prescription
- PharmacyDispensing → PrescriptionItem/PharmacyStock
- PatientBill → Patient/Hospital
- BillItem → PatientBill
- Payment → PatientBill
- VitalSigns → Patient
- Triage → Patient/Hospital/VitalSigns
- WardBed → Hospital
- PatientCheckIn → Patient/Hospital/Appointment
- Queue → Hospital/Patient
- HealthRecord → Patient

## Access Patterns

### Patient Access
- Own appointments, health records, notifications
- Visit history and current home visit status
- Pending lab results
- Active prescriptions
- Current billing information

### Doctor Access
- Assigned patients and their records
- Appointments and patient visits
- Lab results for ordered tests
- Prescriptions written
- Triage observations
- Patient vital signs

### Hospital Administrator Access
- All facility data
- Queue management
- Ward bed occupancy
- Billing reports
- Pharmacy inventory
- Staff performance

### System Administrator Access
- User management
- Facility configuration
- System settings
- Audit logs

## Query Optimization Notes

### Implemented select_related() for:
- Doctor → User, Hospital
- Patient → User, Doctor, Hospital
- Appointment → Patient, Doctor, Hospital
- LabTest → Patient, Doctor, Hospital
- Prescription → Patient, Doctor, Hospital
- PatientBill → Patient, Hospital
- Triage → Patient, Hospital, VitalSigns
- WardBed → Hospital, Patient
- PatientCheckIn → Patient, Hospital
- Queue → Hospital, Patient

### Indexes Needed (for production):
- LabTest.status, priority
- Prescription.status, created_at
- PatientBill.status, due_date
- Appointment.scheduled_time, status
- PatientCheckIn.check_in_time, check_out_time
- Queue.position
- VitalSigns.recorded_at
- Triage.priority_level, triaged_at

---
**Database Title**: AfyaLink Smart Hospital Management Platform  
**Last Updated**: April 24, 2026  
**Models**: 35+  
**Relationships**: Fully interconnected for complete hospital workflow
