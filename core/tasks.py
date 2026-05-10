from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Appointment, PatientBill, Payment, Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_appointment_reminders():
    """Send reminders for appointments tomorrow"""
    tomorrow = timezone.now() + timedelta(days=1)
    start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999)
    
    appointments = Appointment.objects.filter(
        appointment_date__range=[start_of_day, end_of_day],
        status__in=['pending', 'confirmed']
    ).select_related('patient__user', 'doctor__user', 'hospital')
    
    for appointment in appointments:
        # Create notification for patient
        Notification.objects.create(
            user=appointment.patient.user,
            title="Appointment Reminder",
            message=f"You have an appointment with Dr. {appointment.doctor.user.get_full_name()} tomorrow at {appointment.appointment_date.strftime('%I:%M %p')}",
            notification_type='appointment_reminder',
            related_appointment=appointment
        )
        
        # Create notification for doctor
        Notification.objects.create(
            user=appointment.doctor.user,
            title="Appointment Reminder",
            message=f"You have an appointment with {appointment.patient.user.get_full_name()} tomorrow at {appointment.appointment_date.strftime('%I:%M %p')}",
            notification_type='appointment_reminder',
            related_appointment=appointment
        )
    
    return f"Sent {appointments.count()} appointment reminders"


@shared_task
def send_bill_reminders():
    """Send reminders for unpaid bills"""
    pending_bills = PatientBill.objects.filter(
        status='pending',
        due_date__lt=timezone.now().date()
    ).select_related('patient__user', 'hospital')
    
    for bill in pending_bills:
        outstanding = bill.total_amount - (
            Payment.objects.filter(bill=bill, status='completed').aggregate(
                total=Sum('amount')
            )['total'] or 0
        )
        
        # Create notification for patient
        Notification.objects.create(
            user=bill.patient.user,
            title="Payment Reminder",
            message=f"Your bill #{bill.bill_number} from {bill.hospital.name} is overdue. Outstanding amount: KES {outstanding:,.2f}",
            notification_type='bill_reminder',
            related_bill=bill
        )
    
    return f"Sent {pending_bills.count()} bill reminders"


@shared_task
def update_appointment_status():
    """Update appointment status to completed if time has passed"""
    now = timezone.now()
    
    # Mark past appointments as completed if they're still pending
    past_appointments = Appointment.objects.filter(
        appointment_date__lt=now,
        status__in=['pending', 'confirmed']
    )
    
    updated_count = past_appointments.update(status='completed')
    
    return f"Updated {updated_count} appointments to completed"


@shared_task
def generate_daily_report():
    """Generate daily report of hospital activities"""
    today = timezone.now().date()
    
    appointments_today = Appointment.objects.filter(
        appointment_date__date=today
    ).count()
    
    checkins_today = PatientCheckIn.objects.filter(
        check_in_time__date=today
    ).count()
    
    revenue_today = PatientBill.objects.filter(
        created_at__date=today
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return {
        'date': str(today),
        'appointments': appointments_today,
        'checkins': checkins_today,
        'revenue': float(revenue_today),
    }


# Import Sum for aggregation
from django.db.models import Sum
