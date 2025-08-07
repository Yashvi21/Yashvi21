from django.db import models
from django.conf import settings
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Initial Consultation'),
        ('follow_up', 'Follow-up'),
        ('document_review', 'Document Review'),
        ('legal_advice', 'Legal Advice'),
        ('case_discussion', 'Case Discussion'),
        ('emergency', 'Emergency'),
    ]
    
    MEETING_TYPE_CHOICES = [
        ('in_person', 'In Person'),
        ('video_call', 'Video Call'),
        ('phone_call', 'Phone Call'),
    ]
    
    # Core fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_user')
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_lawyer')
    
    # Appointment details
    title = models.CharField(max_length=200)
    description = models.TextField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    meeting_type = models.CharField(max_length=15, choices=MEETING_TYPE_CHOICES, default='video_call')
    
    # Scheduling
    requested_date = models.DateField()
    requested_time = models.TimeField()
    confirmed_date = models.DateField(blank=True, null=True)
    confirmed_time = models.TimeField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    
    # Status and management
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')
    ], default='normal')
    
    # Meeting details
    meeting_link = models.URLField(blank=True, null=True)
    meeting_location = models.TextField(blank=True, null=True)
    meeting_notes = models.TextField(blank=True, null=True)
    
    # Fees and payment
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    # Reminders and notifications
    reminder_sent_to_user = models.BooleanField(default=False)
    reminder_sent_to_lawyer = models.BooleanField(default=False)
    
    # Additional information
    documents_shared = models.ManyToManyField('documents.Document', blank=True, related_name='related_appointments')
    
    # Cancellation/Rescheduling
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='cancelled_appointments')
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Appointment: {self.user.username} with {self.lawyer.username} - {self.title}"
    
    @property
    def is_upcoming(self):
        if self.confirmed_date and self.confirmed_time:
            appointment_datetime = timezone.datetime.combine(self.confirmed_date, self.confirmed_time)
            return appointment_datetime > timezone.now()
        return False
    
    @property
    def is_overdue(self):
        if self.confirmed_date and self.confirmed_time:
            appointment_datetime = timezone.datetime.combine(self.confirmed_date, self.confirmed_time)
            return appointment_datetime < timezone.now() and self.status in ['pending', 'confirmed']
        return False

class AppointmentFeedback(models.Model):
    """Feedback after appointment completion"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='feedback')
    
    # User feedback about lawyer
    user_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    user_feedback = models.TextField(blank=True, null=True)
    user_would_recommend = models.BooleanField(blank=True, null=True)
    
    # Lawyer feedback about user
    lawyer_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    lawyer_feedback = models.TextField(blank=True, null=True)
    
    # General feedback
    meeting_quality = models.CharField(max_length=10, choices=[
        ('poor', 'Poor'), ('fair', 'Fair'), ('good', 'Good'), ('excellent', 'Excellent')
    ], blank=True, null=True)
    
    technical_issues = models.BooleanField(default=False)
    technical_issues_description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.appointment.title}"

class LawyerAvailability(models.Model):
    """Track lawyer availability for appointment scheduling"""
    WEEKDAY_CHOICES = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
        (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availability_slots')
    weekday = models.PositiveIntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Break times
    break_start_time = models.TimeField(blank=True, null=True)
    break_end_time = models.TimeField(blank=True, null=True)
    
    # Special dates
    special_date = models.DateField(blank=True, null=True)  # For specific date availability
    is_holiday = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['lawyer', 'weekday', 'start_time']
    
    def __str__(self):
        return f"{self.lawyer.username} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"

class AppointmentRescheduleRequest(models.Model):
    """Track reschedule requests"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reschedule_requests')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    new_requested_date = models.DateField()
    new_requested_time = models.TimeField()
    reason = models.TextField()
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    response_message = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='responded_reschedules')
    responded_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reschedule request for {self.appointment.title}"
