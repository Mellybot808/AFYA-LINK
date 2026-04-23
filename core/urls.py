from django.urls import include, path
from rest_framework import routers
from .views import (
    APIFrontendView,
    DashboardView,
    HomeView,
    DoctorViewSet,
    PatientViewSet,
    HospitalViewSet,
    HealthRecordViewSet,
)

router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'hospitals', HospitalViewSet, basename='hospital')
router.register(r'records', HealthRecordViewSet, basename='healthrecord')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api-frontend/', APIFrontendView.as_view(), name='api_frontend'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
]
