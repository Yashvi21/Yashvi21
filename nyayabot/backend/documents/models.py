from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('legal_notice', 'Legal Notice'),
        ('contract', 'Contract'),
        ('court_order', 'Court Order'),
        ('complaint', 'Complaint'),
        ('affidavit', 'Affidavit'),
        ('agreement', 'Agreement'),
        ('lease_deed', 'Lease Deed'),
        ('property_document', 'Property Document'),
        ('identity_proof', 'Identity Proof'),
        ('income_proof', 'Income Proof'),
        ('medical_report', 'Medical Report'),
        ('police_report', 'Police Report'),
        ('other', 'Other'),
    ]
    
    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('shared_with_lawyer', 'Shared with Lawyer'),
        ('public', 'Public'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = CloudinaryField('raw')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=10)  # pdf, doc, jpg, etc.
    privacy_level = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='private')
    
    # AI Analysis
    is_analyzed = models.BooleanField(default=False)
    ai_summary = models.TextField(blank=True, null=True)
    ai_extracted_text = models.TextField(blank=True, null=True)
    ai_key_points = models.JSONField(default=list, blank=True)
    ai_legal_issues = models.JSONField(default=list, blank=True)
    ai_confidence_score = models.FloatField(blank=True, null=True)
    
    # Sharing
    shared_with_lawyers = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                               related_name='shared_documents', 
                                               blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class DocumentAnalysis(models.Model):
    """Detailed AI analysis of documents"""
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='analysis')
    
    # Text extraction and processing
    extracted_text = models.TextField()
    word_count = models.PositiveIntegerField(default=0)
    language_detected = models.CharField(max_length=10, default='en')
    
    # Legal analysis
    legal_category = models.CharField(max_length=100, blank=True, null=True)
    key_clauses = models.JSONField(default=list)
    potential_issues = models.JSONField(default=list)
    missing_elements = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    # Entities and dates
    parties_involved = models.JSONField(default=list)
    important_dates = models.JSONField(default=list)
    monetary_amounts = models.JSONField(default=list)
    legal_references = models.JSONField(default=list)
    
    # Risk assessment
    risk_level = models.CharField(max_length=10, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
    ], blank=True, null=True)
    risk_factors = models.JSONField(default=list)
    
    # AI processing metadata
    processing_time = models.FloatField()
    ai_model_used = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis of {self.document.title}"

class DocumentShare(models.Model):
    """Track document sharing between users and lawyers"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_documents_by')
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_documents_with')
    
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('comment', 'View and Comment'),
        ('edit', 'View and Edit'),
    ]
    
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='view')
    message = models.TextField(blank=True, null=True)
    is_revoked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['document', 'shared_with']
    
    def __str__(self):
        return f"{self.document.title} shared with {self.shared_with.username}"

class DocumentComment(models.Model):
    """Comments on documents by lawyers or users"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    is_internal = models.BooleanField(default=False)  # Internal lawyer notes
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.document.title}"
