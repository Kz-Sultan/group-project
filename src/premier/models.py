from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    appointmentType = models.CharField(max_length=100, default='General Checkup')
    doctor = models.CharField(max_length=100, blank=True, null=True)
    appointmentDate = models.DateField(null=True, blank=True)
    timePreference = models.TimeField(blank=True, null=True)

    is_cancelled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    status_message = models.CharField(max_length=255, blank=True, default='')


    def __str__(self):
        return f"Appointment for {self.first_name} {self.last_name} on {self.appointmentDate} at {self.timePreference}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
