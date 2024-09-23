from django import forms
from authen.models import TimeSlot

class BookingForm(forms.Form):
    slot_id = forms.ModelChoiceField(queryset=TimeSlot.objects.none(), label='Select Time Slot')

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if doctor:
            self.fields['slot_id'].queryset = TimeSlot.objects.filter(doctor=doctor, is_booked=False)
