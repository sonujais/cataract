from django.db import models
from authen.models import *
from django.contrib.auth.models import User

    
class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
class Notification(models.Model):
    patient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification from {self.patient.username} to {self.doctor.username}'

    def __str__(self):
        return f'{self.doctor.user.first_name} {self.doctor.user.last_name} - {self.date} {self.time}'

