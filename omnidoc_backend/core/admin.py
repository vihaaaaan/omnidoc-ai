from django.contrib import admin
from .models import Patient, Session


# Register your models here.
admin.site.register(Patient)
admin.site.register(Session)
