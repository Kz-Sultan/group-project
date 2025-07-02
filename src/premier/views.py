from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Contact



# Create your views here.
def base(request):
    return render(request, 'premier/base.html')  

def about(request):
    return render(request, 'premier/about.html')



from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Contact

from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('fullName')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Validate required fields
            if not all([name, email, subject, message]):
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)
                return render(request, 'premier/contact.html', {'error': 'Missing required fields.'})

            contact = Contact(
                name=name,
                email=email,
                phone_number=phone_number,
                subject=subject,
                message=message
            )
            contact.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('inbox')
        except Exception as e:
            print("Error saving contact:", e)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            return render(request, 'premier/contact.html', {'error': str(e)})
    return render(request, 'premier/contact.html')

def appointments(request):
    cancel_message = None
    appointment_sent = False

    # Handle appointment booking
    if request.method == 'POST':
        # If this is a cancel request
        if 'cancelEmail' in request.POST:
            email = request.POST.get('cancelEmail')
            date = request.POST.get('cancelDate')
            try:
                appointment = Appointment.objects.get(email=email, appointmentDate=date)
                appointment.is_cancelled = True
                appointment.save()
                cancel_message = "Your appointment has been cancelled."
            except Appointment.DoesNotExist:
                cancel_message = "No matching appointment found."
        # If this is a booking request (adjust field names as needed)
        elif 'firstName' in request.POST and 'appointmentType' in request.POST:
            Appointment.objects.create(
                first_name=request.POST.get('firstName'),
                last_name=request.POST.get('lastName'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                appointmentType=request.POST.get('appointmentType'),
                doctor=request.POST.get('doctor'),
                appointmentDate=request.POST.get('appointmentDate'),
                timePreference=request.POST.get('timePreference'),
            )
            appointment_sent = True

    return render(request, 'premier/appointments.html', {
        'cancel_message': cancel_message,
        'appointment_sent': appointment_sent
    })

def appointments_list(request):
    from .models import Appointment  # Ensure Appointment is imported

    cancel_message = None

    appointments = Appointment.objects.all().order_by('-appointmentDate')

    if request.method == 'POST':
        # Handle user-side cancellation
        cancel_email = request.POST.get('cancelEmail')
        cancel_phone = request.POST.get('cancelPhone')
        cancel_reason = request.POST.get('cancelReason')
        if cancel_email and cancel_phone:
            appointment = Appointment.objects.filter(
                email=cancel_email,
                phone=cancel_phone,
                is_cancelled=False
            ).order_by('-appointmentDate').first()
            if appointment:
                appointment.is_cancelled = True
                appointment.status_message = f"Cancelled: {cancel_reason}"
                appointment.save()
                cancel_message = 'Appointment cancelled by patient!'
            else:
                cancel_message = 'No matching appointment found or already cancelled.'

        # Handle manual creation (admin-side)
        elif request.POST.get('manual_create') == '1':
            Appointment.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                appointmentType=request.POST.get('appointmentType'),
                doctor=request.POST.get('doctor'),
                appointmentDate=request.POST.get('appointmentDate'),
                timePreference=request.POST.get('timePreference'),
            )
            return redirect('appointments_list')

        # Handle admin actions (confirm/cancel/delete)
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        if appointment_id and action:
            appointment = Appointment.objects.get(id=appointment_id)
            if action == 'confirm':
                appointment.is_confirmed = True
                appointment.is_cancelled = False
                appointment.status_message = "Your appointment has been approved."
                appointment.save()
            elif action == 'cancel':
                appointment.is_cancelled = True
                appointment.is_confirmed = False
                appointment.status_message = "Your appointment has been cancelled."
                appointment.save()
            elif action == 'delete':
                appointment.delete()
            return redirect('appointments_list')

    return render(request, 'premier/appointments_list.html', {
        'appointments_list': appointments,
        'cancel_message': cancel_message
    })



def book_appointment(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        appointmentType = request.POST.get('appointmentType')
        doctor = request.POST.get('doctor')
        appointmentDate = request.POST.get('appointmentDate')
        timePreference = request.POST.get('timePreference')

        appointment = Appointment(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            appointmentType=appointmentType,
            doctor=doctor,
            appointmentDate=appointmentDate,
            timePreference=timePreference,
            
        )
        appointment.save()
        return redirect('appointments_list')

    return render(request, 'premier/book_appointment.html')
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.is_cancelled = True
        appointment.save()
        return redirect('appointments_list')
    
    return render(request, 'premier/cancel_appointment.html', {'appointment': appointment})

def inbox(request):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            message=message
        )
        contact.save()
        return redirect('inbox')
    
    contacts = Contact.objects.all().order_by('-id')
    return render(request, 'premier/inbox.html', {'contacts': contacts})

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Contact

@csrf_exempt
def mark_message_read(request, pk):
    if request.method == 'POST':
        try:
            contact = Contact.objects.get(pk=pk)
            contact.read = True
            contact.save()
            return JsonResponse({'success': True})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def mark_message_unread(request, pk):
    if request.method == 'POST':
        try:
            contact = Contact.objects.get(pk=pk)
            contact.read = False
            contact.save()
            return JsonResponse({'success': True})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def delete_message(request, pk):
    if request.method == 'POST':
        try:
            contact = Contact.objects.get(pk=pk)
            contact.delete()
            return JsonResponse({'success': True})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return HttpResponseNotAllowed(['POST'])


    # Assuming you have a Notification model to fetch notifications
    # notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # For now, we'll just return an empty list
    notifications = []
    return render(request, 'premier/notifications.html', {'notifications': notifications})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def reply_message(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        contact.reply = reply_text
        contact.save()
    return redirect('inbox')

from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    appointments = Appointment.objects.filter(email=request.user.email).order_by('-appointmentDate')
    contacts = Contact.objects.filter(email=request.user.email).order_by('-created_at')
    return render(request, 'premier/notifications.html', {
        'appointments': appointments,
        'contacts': contacts,
    })

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    