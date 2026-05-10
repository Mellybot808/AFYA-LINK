from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import (
    APIFrontendView,
    DashboardView,
    HomeView,
    RegisterView,
    PatientDashboardView,
    DoctorPortalView,
    AdminReportsView,
    DoctorViewSet,
    PatientViewSet,
    HospitalViewSet,
    HealthRecordViewSet,
    MedicViewSet,
    VisitRequestViewSet,
    VisitViewSet,
    AppointmentViewSet,
    NotificationViewSet,
    LabTestViewSet,
    LabResultViewSet,
    PrescriptionViewSet,
    PrescriptionItemViewSet,
    PharmacyStockViewSet,
    PharmacyDispensingViewSet,
    PatientBillViewSet,
    BillItemViewSet,
    PaymentViewSet,
    VitalSignsViewSet,
    TriageViewSet,
    WardBedViewSet,
    PatientCheckInViewSet,
    QueueViewSet,
    MedicalHistoryViewSet,
    AllergyViewSet,
    MedicationViewSet,
    EmergencyContactViewSet,
    PatientInsuranceViewSet,
    InsuranceClaimViewSet,
    patient_portal_summary,
    patient_medical_records,
    patient_billing_details,
    doctor_performance_report,
    hospital_analytics,
    pharmacy_inventory,
    export_patient_records_pdf,
    export_patient_bills_pdf,
    export_appointments_csv,
    export_prescriptions_csv,
)

router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'hospitals', HospitalViewSet, basename='hospital')
router.register(r'records', HealthRecordViewSet, basename='healthrecord')
router.register(r'medics', MedicViewSet, basename='medic')
router.register(r'visit-requests', VisitRequestViewSet, basename='visitrequest')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'lab-tests', LabTestViewSet, basename='labtest')
router.register(r'lab-results', LabResultViewSet, basename='labresult')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'prescription-items', PrescriptionItemViewSet, basename='prescriptionitem')
router.register(r'pharmacy-stock', PharmacyStockViewSet, basename='pharmacystock')
router.register(r'pharmacy-dispensing', PharmacyDispensingViewSet, basename='pharmacydispensing')
router.register(r'bills', PatientBillViewSet, basename='bill')
router.register(r'bill-items', BillItemViewSet, basename='billitem')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'vital-signs', VitalSignsViewSet, basename='vitalsigns')
router.register(r'triages', TriageViewSet, basename='triage')
router.register(r'ward-beds', WardBedViewSet, basename='wardbed')
router.register(r'check-ins', PatientCheckInViewSet, basename='checkin')
router.register(r'queues', QueueViewSet, basename='queue')
router.register(r'medical-histories', MedicalHistoryViewSet, basename='medicalhistory')
router.register(r'allergies', AllergyViewSet, basename='allergy')
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergencycontact')
router.register(r'patient-insurances', PatientInsuranceViewSet, basename='patientinsurance')
router.register(r'insurance-claims', InsuranceClaimViewSet, basename='insuranceclaim')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('patient-dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctor-portal/', DoctorPortalView.as_view(), name='doctor_portal'),
    path('admin-reports/', AdminReportsView.as_view(), name='admin_reports'),
    path('api-frontend/', APIFrontendView.as_view(), name='api_frontend'),
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # Patient Portal API endpoints
    path('api/patient/portal/', patient_portal_summary, name='patient_portal_summary'),
    path('api/patient/records/', patient_medical_records, name='patient_medical_records'),
    path('api/patient/billing/', patient_billing_details, name='patient_billing_details'),
    # Analytics & Reports API endpoints
    path('api/doctor/performance/', doctor_performance_report, name='doctor_performance_report'),
    path('api/hospital/analytics/', hospital_analytics, name='hospital_analytics'),
    path('api/pharmacy/inventory/', pharmacy_inventory, name='pharmacy_inventory'),
    # Data Export endpoints
    path('api/export/patient-records-pdf/', export_patient_records_pdf, name='export_patient_records_pdf'),
    path('api/export/patient-bills-pdf/', export_patient_bills_pdf, name='export_patient_bills_pdf'),
    path('api/export/appointments-csv/', export_appointments_csv, name='export_appointments_csv'),
    path('api/export/prescriptions-csv/', export_prescriptions_csv, name='export_prescriptions_csv'),
]
