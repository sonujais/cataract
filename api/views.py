from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageUploadForm
from .models import ImageUpload, RecommendationRequest
from authen.models import DoctorProfile
from django.core.mail import send_mail  # For sending email recommendations

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_upload = form.save(commit=False)
                image_upload.user = request.user  # Save the current logged-in user (as a User object)
                image_upload.disease_predict = predict_disease(image_upload.image.path)  # Dummy function for prediction
                image_upload.save()
                messages.success(request, 'Image uploaded and prediction saved successfully.')
                return redirect('history')  # Redirect to the history page after upload
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = ImageUploadForm()

    return render(request, 'patient/dashboard.html', {
        'form': form,
    })

def history(request):
    uploaded_images = ImageUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'patient/history.html', {
        'uploaded_images': uploaded_images,
    })

def result(request, image_id):
    detection_result = get_object_or_404(ImageUpload, id=image_id)
    return render(request, 'patient/result.html', {
        'detection_result': detection_result,
    })

@login_required
def request_recommendation(request, image_id):
    image = get_object_or_404(ImageUpload, id=image_id, user=request.user)

    # Assuming there is only one doctor, or you can adjust this to allow patient to select the doctor
    try:
        doctor = DoctorProfile.objects.first()  # You can customize this part
        if doctor:
            # Create the recommendation request
            recommendation_request = RecommendationRequest.objects.create(
                image=image,
                patient=request.user,
                doctor=doctor,
                message=f"Please review this image and provide your recommendation."
            )
            messages.success(request, 'Request has been sent to the doctor.')
        else:
            messages.error(request, 'No doctor is available at the moment.')
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Unable to find the doctor.')

    return redirect('history')

@login_required
def respond_request(request, request_id):
    recommendation_request = get_object_or_404(RecommendationRequest, id=request_id, doctor__user=request.user)

    if request.method == 'POST':
        comment = request.POST.get('doctor_comment')
        recommendation_request.image.doctor_comment = comment
        recommendation_request.image.save()
        recommendation_request.is_reviewed = True
        recommendation_request.save()
        messages.success(request, 'Your recommendation has been sent to the patient.')
        return redirect('doctor_dashboard')

    return render(request, 'doctor/respond_request.html', {'request': recommendation_request})


def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ImageUpload, id=image_id)
        image.delete()  # Delete the image
        messages.success(request, 'Image deleted successfully.')
        return redirect('history')
    
    


# Dummy function for prediction
def predict_disease(image_path):
    # You would load your model here and return a result (e.g., 'Cataract', 'Normal')
    return "Cataract"  # Example result
