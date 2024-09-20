
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from authen.models import DoctorProfile
from .models import Appointment
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        # Update the user's profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'edit_profile.html')

def settings(request):
    return render(request, 'settings.html')

@login_required
def update_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        confirm_username = request.POST.get('confirm_username')
        
        user = request.user

        # Check if the new username matches the confirmation
        if new_username and new_username == confirm_username:
            old_username = user.username
            user.username = new_username
            user.save()

            # Send an email notification
            send_mail(
                'Username Changed',
                f'Your username has been changed from {old_username} to {new_username}.',
                'nayanai.innovate@gmail.com',  # Replace with your sender email
                [user.email],  # Send to the user's registered email
                fail_silently=False,
            )

            messages.success(request, "Username updated successfully")
        else:
            messages.error(request, "Usernames do not match")
        
        return redirect('settings')
    
    return render(request, 'settings.html')

@login_required
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
            return redirect('settings')

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            
            # Update the session to prevent logout after password change
            update_session_auth_hash(request, user)
            
            # Send an email notification
            send_mail(
                'Password Changed',
                'Your password has been changed successfully.',
                'nayanai.innovate@gmail.com',  # Replace with your sender email
                [user.email],  # Send to the user's registered email
                fail_silently=False,
            )
            messages.success(request, "Password updated successfully")
        elif new_password and new_password != confirm_password:
            messages.error(request, "New passwords do not match")
        
        return redirect('settings')
    
    return render(request, 'settings.html')


@login_required
def update_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Name updated successfully.')
        return redirect('settings')

    return render(request, 'settings.html')

@login_required

def upload_img(request):
    return render(request, 'upload.html')

@login_required
def update_email(request):
    if request.method == 'POST':
        current_email = request.POST.get('current_email')
        new_email = request.POST.get('new_email')
        confirm_email = request.POST.get('confirm_email')
        
        user = request.user

        if current_email != user.email:
            messages.error(request, "Current email is incorrect")
            return redirect('settings')

        if new_email and new_email == confirm_email:
            user.email = new_email
            user.save()

            send_mail(
                'Email Changed',
                'Your email has been changed successfully.',
                'nayanai.innovate@gmail.com',
                [new_email],
                fail_silently=False,
            )
            messages.success(request, "Email updated successfully")
        elif new_email and new_email != confirm_email:
            messages.error(request, "New emails do not match")
        
        return redirect('settings')
    
    return render(request, 'settings.html')
def doctor_dashboard(request):
    return render(request, 'doctor/dashboard.html')

def patient_dashboard(request):
    return render(request, 'patient/dashboard.html')

def prediction(request):
    return render(request, 'patient/prediction.html')

def history(request):
    return render(request, 'patient/history.html')

def patient_settings(request):
    return render(request, 'patient/settings.html')

def book_appointment(request):
    doctors = DoctorProfile.objects.all()
    available_slots = None

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        selected_doctor = DoctorProfile.objects.get(user_id=doctor_id)
        
        # Fetch available slots for the selected doctor
        available_slots = Appointment.objects.filter(doctor=selected_doctor, is_booked=False)
        
        if available_slots:
            return render(request, 'patient/book_appointment.html', {
                'doctors': doctors,
                'available_slots': available_slots,
            })
        
        # Handle the booking logic
        # Check if slot is available, book it and redirect or show success message
        # Example:
        # new_appointment = Appointment.objects.create(doctor=selected_doctor, ...)

    return render(request, 'patient/appointment.html', {
        'doctors': doctors,
        'available_slots': available_slots,
    })

def see_appointments(request):
    return render(request, 'doctor/appointments.html')

def doctor_settings(request):
    return render(request, 'doctor/settings.html')

import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def get_available_timeslots(request):
    date = request.GET.get('date')
    doctor_id = request.GET.get('doctor_id')

    # Ensure both date and doctor_id are provided
    if date and doctor_id:
        # Generate random time slots
        all_possible_slots = [
            "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
            "11:00 AM", "11:30 AM", "01:00 PM", "01:30 PM",
            "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
            "04:00 PM", "04:30 PM"
        ]
        
        # For demo purposes, return a random selection of 5 slots
        num_slots = 5
        random_slots = random.sample(all_possible_slots, min(num_slots, len(all_possible_slots)))
        
        return JsonResponse({'time_slots': random_slots})
    else:
        return JsonResponse({'time_slots': []}, status=400)


# def logout_view(request):
#     auth_logout(request)
#     return redirect('login')
