from django.db import models
from django.core.validators import RegexValidator
from .base import BaseModel

class Patient(BaseModel):
    # Basic Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ])

    # Contact Information
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    # Emergency Contact (crucial for medical applications)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17)
    emergency_contact_relationship = models.CharField(max_length=50)

    # Basic Medical Information
    medical_record_number = models.CharField(max_length=50, unique=True)
    has_allergies = models.BooleanField(default=False)
    current_medications = models.TextField(blank=True, null=True, 
        help_text="List of current medications, if any")

    # System Fields
    is_active = models.BooleanField(default=True)
    last_visit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['medical_record_number']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} (MRN: {self.medical_record_number})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
