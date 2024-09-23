from django.db import models
from django.contrib.auth.models import User

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    disease_predict = models.CharField(max_length=100, blank=True, null=True)
    doctor_comment = models.TextField(null=True, blank=True)  # Doctor's comment field
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    # ForeignKey to the User model

    def __str__(self):
        return f"{self.user.username} - {self.disease_predict}"
