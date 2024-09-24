from django.urls import path
from .views import upload_image, history, result, request_recommendation, delete_image, respond_request

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('history/', history, name='history'),
    path('result/<int:image_id>/', result, name='result'),

    path('request-recommendation/<int:image_id>/', request_recommendation, name='request_recommendation'),
    path('respond-request/<int:request_id>/', respond_request, name='respond_request'),


    path('delete_image/<int:image_id>/', delete_image, name='delete_image'),
]
