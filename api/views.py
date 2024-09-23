from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ImageUploadForm
from .models import ImageUpload
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

def request_recommendation(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ImageUpload, id=image_id)
        # Logic to send a recommendation request, e.g., email to doctor
        send_mail(
            'Recommendation Request',
            f'A recommendation has been requested for the image uploaded on {image.uploaded_at}.',
            'from@example.com',  # Replace with your from email
            ['doctor@example.com'],  # Replace with the doctor's email
            fail_silently=False,
        )
        messages.success(request, 'Recommendation request sent successfully.')
        return redirect('history')

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
