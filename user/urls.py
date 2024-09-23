# user/urls.py or doctor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/settings/', views.patient_settings, name='patient_settings'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_email/', views.update_email, name='update_email'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('update_username/', views.update_username, name='update_username'), 
    path('update_name/', views.update_name, name='update_name'),
    # path('doctor/appointments/', views.see_appointments, name='see_appointments'),
    # path('doctor/settings/', views.settings, name='settings'),
    # path('logout/', views.logout_view, name='logout'),
    # Other URLs...
]
