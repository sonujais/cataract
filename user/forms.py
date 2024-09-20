# forms.py
from django import forms

class EyeImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload Eye Image")
