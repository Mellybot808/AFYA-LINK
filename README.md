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

- Django authentication with login/logout
- Patient and doctor dashboard views at `/dashboard/`
- REST API explorer frontend at `/api-frontend/`
- API endpoints for doctors, patients, hospitals, and health records

## URLs

- Home: `/`
- Dashboard: `/dashboard/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`
- API: `/api/`
- API frontend: `/api-frontend/`
- Admin: `/admin/`

## Notes

- The project uses SQLite by default for local development.
- Add app-specific features in `core/models.py`, `core/views.py`, and `core/urls.py`.
