from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.

class LawyerProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('family', 'Family Law'),
        ('criminal', 'Criminal Law'),
        ('civil', 'Civil Law'),
        ('corporate', 'Corporate Law'),
        ('property', 'Property Law'),
        ('labour', 'Labour Law'),
        ('tax', 'Tax Law'),
        ('consumer', 'Consumer Protection'),
        ('cyber', 'Cyber Law'),
        ('immigration', 'Immigration Law'),
        ('environmental', 'Environmental Law'),
        ('intellectual', 'Intellectual Property'),
        ('constitutional', 'Constitutional Law'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lawyer_profile')
    bar_council_id = models.CharField(max_length=50, unique=True)
    bar_council_certificate = CloudinaryField('image')
    specializations = models.JSONField(default=list)  # Store multiple specializations
    years_of_experience = models.PositiveIntegerField()
    education = models.TextField()
    law_firm_name = models.CharField(max_length=200, blank=True, null=True)
    office_address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    languages_spoken = models.JSONField(default=list)
    bio = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Availability
    available_days = models.JSONField(default=list)  # e.g., ['monday', 'tuesday', 'wednesday']
    available_time_start = models.TimeField(blank=True, null=True)
    available_time_end = models.TimeField(blank=True, null=True)
    
    # Verification documents
    identity_proof = CloudinaryField('image', blank=True, null=True)
    degree_certificate = CloudinaryField('image', blank=True, null=True)
    
    # Ratings and reviews
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_consultations = models.PositiveIntegerField(default=0)
    
    # Admin fields
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='verified_lawyers')
    verification_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-average_rating', '-total_reviews']
    
    def __str__(self):
        return f"Lawyer: {self.user.get_full_name()} - {self.bar_council_id}"

class LawyerRating(models.Model):
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['lawyer', 'user']
    
    def __str__(self):
        return f"{self.user.username} rated {self.lawyer.user.username}: {self.rating} stars"
