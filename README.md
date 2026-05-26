# AfyaLink Django Platform

A Django-based health platform scaffold for AfyaLink.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

## Features

- Django authentication with login/logout and user registration
- Patient and doctor dashboard views at `/dashboard/`
- REST API explorer frontend at `/api-frontend/`
- Comprehensive API endpoints for all major modules
- Medic Home Visit module: Patient-requested home visits with medic dispatch and GPS matching
- Patient Portal: Appointment booking, visit history, and notifications
- Laboratory module: Test ordering, result management, and tracking
- Pharmacy module: Prescription management, drug stock management, and dispensing
- Billing module: Automated invoicing, payment tracking, and receipt generation
- Triage/Nursing module: Vital signs capture, patient prioritization, ward assignment
- Reception module: Check-in management, queue management, and patient routing

## Future Feature Directions

Since you're in the idea-collection phase, here are some feature directions to explore for AfyaLink:

### 🌍 User-Centered Features
- **Personalized Health Dashboards**: Allow users to track vitals, appointments, and medication schedules in one place.
- **Multilingual Support**: Especially important in Kenya and East Africa, where multiple languages are spoken.
- **Offline Access**: Enable basic functionality without internet, syncing later when online.

### 🔗 Integration & Connectivity
- **Telemedicine Integration**: Video consultations with doctors directly through the platform.
- **Wearable Device Sync**: Pull in data from fitness trackers or smartwatches for proactive health monitoring.
- **Pharmacy & Lab Linkages**: Connect users to nearby pharmacies and labs for prescriptions and test results.

### 🧠 Smart Tools
- **AI Symptom Checker**: A guided tool that helps users understand possible conditions before visiting a doctor.
- **Decision Support for Clinicians**: Provide doctors with predictive analytics for diagnosis and treatment planning.
- **Chatbot for FAQs**: Quick answers to common health questions, appointment reminders, or insurance queries.

### 📊 Community & Education
- **Health Literacy Modules**: Bite‑sized lessons on nutrition, preventive care, and chronic disease management.
- **Community Forums**: Safe spaces for patients to share experiences and support each other.
- **Gamification**: Reward users for healthy habits (e.g., completing daily steps, attending checkups).

### 🔒 Trust & Security
- **End-to-End Encryption**: For sensitive health data.
- **Consent Management**: Users control who can access their records.
- **Audit Trails**: Transparency for all data interactions.

## URLs

- Home: `/`
- Dashboard: `/dashboard/`
- Register: `/register/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`
- API: `/api/`
- API frontend: `/api-frontend/`
- Admin: `/admin/`

### API Endpoints

**Core Entities**
- `/api/doctors/` - Doctor management
- `/api/patients/` - Patient management
- `/api/hospitals/` - Hospital management
- `/api/records/` - Health records

**Patient Portal**
- `/api/appointments/` - Appointment management
- `/api/notifications/` - User notifications

**Home Visit Module**
- `/api/medics/` - Medic profiles for home visits
- `/api/visit-requests/` - Home visit requests
- `/api/visits/` - Scheduled home visits

**Laboratory Module**
- `/api/lab-tests/` - Lab test orders
- `/api/lab-results/` - Lab results

**Pharmacy Module**
- `/api/prescriptions/` - Patient prescriptions
- `/api/prescription-items/` - Prescription details
- `/api/pharmacy-stock/` - Medication inventory
- `/api/pharmacy-dispensing/` - Prescription fulfillment records

**Billing Module**
- `/api/bills/` - Patient billing
- `/api/bill-items/` - Bill line items
- `/api/payments/` - Payment records

**Triage/Nursing Module**
- `/api/vital-signs/` - Patient vital signs
- `/api/triages/` - Triage assessments
- `/api/ward-beds/` - Ward bed management

**Reception Module**
- `/api/check-ins/` - Patient check-ins
- `/api/queues/` - Patient queue management

## Notes

- The project uses SQLite by default for local development.
- Add app-specific features in `core/models.py`, `core/views.py`, and `core/urls.py`.

## Production and Deployment

This project is now container-ready for modern hospital deployments.

### Recommended production stack

- PostgreSQL for persistent database storage
- Redis for Celery task brokering and caching
- Gunicorn as the WSGI server
- WhiteNoise for static file serving in production
- Docker and Docker Compose for reproducible deployment

### Available deployment files

- `Dockerfile` — builds the Python application container
- `docker-compose.yml` — orchestrates web, worker, beat, PostgreSQL, and Redis
- `.env.example` — environment variables for production and local Docker
- `Procfile` — Heroku-style process declarations
- `.dockerignore` — files to exclude from Docker contexts

### How to run locally with Docker

1. Copy `.env.example` to `.env` and update secrets.
2. Build and start the stack:

```bash
docker compose up --build
```

3. Visit the application at:

```text
http://localhost:8000/
```

4. Check the service health endpoint:

```text
http://localhost:8000/health/
```

### Notes on environment variables

- `SECRET_KEY` should be a long unique secret in production.
- `ALLOWED_HOSTS` should include your production hostnames.
- `DATABASE_URL` should point to your PostgreSQL database.
- `REDIS_URL` should point to your Redis instance.

### Fast local startup without Docker

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
