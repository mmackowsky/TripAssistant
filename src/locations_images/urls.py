from django.urls import path

from .views import add_image

urlpatterns = [
    path('add-image/<int:location_id>', add_image, name="add_image")
]
