from django.contrib import admin
from .models import Appointment, contact

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'date')
    search_fields = ('first_name', 'last_name', 'email')
    admin.site.register(Appointment)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number')
    search_fields = ('full_name', 'email')
admin.site.register(contact)

# Register your models here.
# admin.site.register(Appointment, AppointmentAdmin)    
   
