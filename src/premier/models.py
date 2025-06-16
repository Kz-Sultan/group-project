from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment for {self.first_name} {self.last_name} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    def get_absolute_url(self):
        return reverse('appointments')  # Redirect to the appointments page after creating an appointment

class contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"

    def get_absolute_url(self):
        return reverse('contact')  # Redirect to the contact page after submitting a contact form


