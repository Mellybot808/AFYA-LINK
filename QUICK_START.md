# AfyaLink Quick Start Guide

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Install Dependencies
```bash
# Clone or navigate to the project
cd "c:\Users\emman\OneDrive\Desktop\AFYA LINK"

# Install required packages
pip install Django djangorestframework
```

### 3. Database Setup
```bash
# Run migrations to create database tables
python manage.py migrate

# Create a superuser account (admin)
python manage.py createsuperuser
# Follow prompts to set username and password
```

### 4. Start Development Server
```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

## Accessing the Platform

### Home Page
```
http://127.0.0.1:8000/
```
Landing page with platform overview and navigation links.

### User Registration
```
http://127.0.0.1:8000/register/
```
Create a new patient or staff account.

### Login
```
http://127.0.0.1:8000/accounts/login/
```
Login with existing credentials.

### Dashboard
```
http://127.0.0.1:8000/dashboard/
```
Personalized dashboard showing:
- **For Patients**: Appointments, health records, notifications
- **For Doctors**: Patient list, upcoming appointments
- **For Admins**: Facility overview, analytics

### API Explorer
```
http://127.0.0.1:8000/api-frontend/
```
Interactive interface to test all API endpoints. Select an endpoint from the dropdown and click "Fetch Data" to see results.

### Admin Panel
```
http://127.0.0.1:8000/admin/
```
Django admin interface for:
- User management
- Adding hospitals, doctors, patients
- Creating appointments, prescriptions, etc.
- Viewing billing and payment records

## Available API Endpoints

### Core Entities
- `GET /api/doctors/` - List all doctors
- `GET /api/patients/` - List all patients
- `GET /api/hospitals/` - List all hospitals
- `GET /api/records/` - List health records

### Patient Portal
- `GET /api/appointments/` - List appointments
- `GET /api/notifications/` - List user notifications

### Home Visit Module
- `GET /api/medics/` - List home visit medics
- `GET /api/visit-requests/` - List visit requests
- `GET /api/visits/` - List completed visits

### Laboratory Module
- `GET /api/lab-tests/` - List lab tests
- `GET /api/lab-results/` - List test results

### Pharmacy Module
- `GET /api/prescriptions/` - List prescriptions
- `GET /api/prescription-items/` - List prescription details
- `GET /api/pharmacy-stock/` - List medication inventory
- `GET /api/pharmacy-dispensing/` - List dispensing records

### Billing Module
- `GET /api/bills/` - List patient bills
- `GET /api/bill-items/` - List bill items
- `GET /api/payments/` - List payment records

### Triage/Nursing Module
- `GET /api/vital-signs/` - List vital signs
- `GET /api/triages/` - List triage records
- `GET /api/ward-beds/` - List ward beds

### Reception Module
- `GET /api/check-ins/` - List patient check-ins
- `GET /api/queues/` - List patient queues

## Using the Admin Panel

### 1. Create a Hospital
Navigate to: **Admin → Hospitals → Add Hospital**
Fill in:
- Name
- Address
- Phone

### 2. Create a Doctor
Navigate to: **Admin → Doctors → Add Doctor**
- Select User (create new user first if needed)
- Enter Specialty
- Select Hospital

### 3. Create a Patient
Navigate to: **Admin → Patients → Add Patient**
- Select User
- Set Date of Birth
- Set Phone
- Select Primary Doctor
- Select Hospital

### 4. Create an Appointment
Navigate to: **Admin → Appointments → Add Appointment**
- Select Patient
- Select Doctor
- Select Hospital
- Set Scheduled Time
- Add Reason/Notes

### 5. Place a Lab Order
Navigate to: **Admin → Lab Tests → Add Lab Test**
- Select Patient
- Select Doctor
- Select Hospital
- Enter Test Name (e.g., "Blood Test")
- Select Test Type
- Set Priority
- Set Expected Completion

### 6. Create a Prescription
Navigate to: **Admin → Prescriptions → Add Prescription**
- Select Patient
- Select Doctor
- Select Hospital
- Add Prescription Items:
  - Drug Name
  - Dosage
  - Frequency
  - Duration
  - Quantity

### 7. Generate a Bill
Navigate to: **Admin → Patient Bills → Add Bill**
- Select Patient
- Select Hospital
- Add Bill Items (drugs, tests, consultations)
- Each item totals automatically

### 8. Record Payment
Navigate to: **Admin → Payments → Add Payment**
- Select Bill
- Enter Amount
- Select Payment Method
- System generates Receipt Number

## Testing with API Explorer

### Example: View All Doctors
1. Go to: http://127.0.0.1:8000/api-frontend/
2. Select "👨‍⚕️ Doctors" from dropdown
3. Click "▶▶ Fetch Data"
4. View JSON response with all doctors

### Example: View Patient Bills
1. Go to: http://127.0.0.1:8000/api-frontend/
2. Select "💰 Patient Bills" from dropdown
3. Click "▶▶ Fetch Data"
4. View JSON with bill details, items, and payments

## File Structure

```
AFYA LINK/
├── afyalink/          # Django project settings
│   ├── settings.py    # Database, apps, security settings
│   ├── urls.py        # Main URL routing
│   └── wsgi.py        # Production server config
│
├── core/              # Main application
│   ├── models.py      # Database models (35+ models)
│   ├── views.py       # API viewsets
│   ├── serializers.py # API serializers
│   ├── urls.py        # API routing
│   ├── admin.py       # Admin interface
│   ├── migrations/    # Database migrations
│   └── apps.py        # App configuration
│
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── core/          # Core app templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── api_frontend.html
│   └── registration/  # Auth templates
│       ├── login.html
│       └── register.html
│
├── manage.py          # Django management script
├── db.sqlite3         # SQLite database (created after migrate)
├── requirements.txt   # Package dependencies
├── README.md          # Project overview
├── IMPLEMENTATION_SUMMARY.md  # Detailed implementation guide
└── DATABASE_SCHEMA.md # Database design documentation
```

## Common Tasks

### Add More Test Data via Admin
1. Login to admin: http://127.0.0.1:8000/admin/
2. Username: (your superuser username)
3. Navigate to desired model
4. Click "Add [Model]"
5. Fill in required fields
6. Click "Save"

### View Patient's Health Data
1. Login as patient or doctor
2. Go to Dashboard: /dashboard/
3. View health records, appointments, notifications

### Check Queue Status
Via API: `GET /api/queues/`
Returns current patient and wait time for each queue.

### Monitor Ward Bed Occupancy
Via API: `GET /api/ward-beds/`
Shows status of each bed (available, occupied, reserved, maintenance).

## Troubleshooting

### Server Won't Start
```
Error: "ModuleNotFoundError: No module named 'django'"
Solution: pip install Django djangorestframework
```

### Database Errors
```
Error: "ProgrammingError: relation does not exist"
Solution: python manage.py migrate
```

### Admin Panel Not Working
```
Error: "TemplateDoesNotExist"
Solution: Ensure templates directory exists and is in TEMPLATES setting
```

### API Returns Empty Data
- Verify data exists in admin panel
- Check user has proper permissions
- Ensure related objects are created (e.g., Hospital before Doctor)

## Next Steps

### For Development
1. Extend models with more fields as needed
2. Add custom viewsets for write operations (POST, PUT, DELETE)
3. Implement authentication tokens for mobile apps
4. Add WebSocket support for real-time updates

### For Deployment
1. Switch to PostgreSQL database
2. Configure static files serving
3. Set up HTTPS/SSL
4. Configure CORS for mobile apps
5. Implement API rate limiting
6. Add comprehensive logging

### For Production
1. Use Gunicorn/uWSGI server
2. Set up Nginx reverse proxy
3. Implement Redis caching
4. Add monitoring and alerting
5. Set up automated backups
6. Implement CDN for static files

## Support & Documentation

- **Main README**: See README.md for project overview
- **Implementation Details**: See IMPLEMENTATION_SUMMARY.md
- **Database Schema**: See DATABASE_SCHEMA.md
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/

---
**Last Updated**: April 24, 2026  
**Platform Version**: 2.0  
**Status**: Ready for Production Testing ✅
