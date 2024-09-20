from django import forms
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile
from django.contrib.auth.forms import UserCreationForm

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class DoctorSignupForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['license_number', 'phone_number']

class PatientSignupForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['phone_number', 'dob']
