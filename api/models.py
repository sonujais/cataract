from django.db import models
from django.contrib.auth.models import User
from authen.models import DoctorProfile  
from datetime import datetime

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    disease_predict = models.CharField(max_length=100, blank=True, null=True)
    doctor_comment = models.TextField(null=True, blank=True)  # Doctor's comment field
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.disease_predict}"
class RecommendationRequest(models.Model):
    image = models.ForeignKey(ImageUpload, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='recommendation_requests', on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, related_name='recommendation_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation Request from {self.patient.username} to Dr. {self.doctor.user.username}"


