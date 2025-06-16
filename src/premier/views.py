from django.shortcuts import render


# Create your views here.
def base(request):
    return render(request, 'premier/base.html')  

def about(request):
    return render(request, 'premier/about.html')

def contact(request):
    return render(request, 'premier/contact.html')

def appointments(request):
    return render(request, 'premier/appointments.html')