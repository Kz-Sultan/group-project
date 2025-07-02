from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments_list/', views.appointments_list, name='appointments_list'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments_list', views.appointments_list, name='appointments_list'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<int:pk>/mark_read/', views.mark_message_read, name='mark_message_read'),
    path('messages/<int:pk>/mark_unread/', views.mark_message_unread),
    path('messages/<int:pk>/delete/', views.delete_message, name='delete_message'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('notifications/', views.notifications, name='Notifications'),
    path('message/<int:pk>/reply/', views.reply_message, name='reply_message'),

]