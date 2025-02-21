from django.db import models
import uuid
from .base import BaseModel
from .patient import Patient

class Session(BaseModel):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('REVIEWED', 'Reviewed'),
    ]

    # Core fields needed for quick access/filtering
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    session_type = models.CharField(max_length=20, default='INTAKE')
    chief_complaint = models.TextField(null=True)  # Keep this in DB for quick triage
    
    # Reference to detailed data
    session_data_url = models.CharField(max_length=255)  # Blob storage URL for full conversation/symptoms
    report_url = models.CharField(max_length=255)        # Final report URL
    
    # Important metadata
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

    # Quick access fields for filtering/searching
    priority_level = models.CharField(max_length=20, null=True)
    primary_symptoms = models.CharField(max_length=255, null=True)  # Comma-separated main symptoms
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)