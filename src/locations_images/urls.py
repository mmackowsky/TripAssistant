from django.urls import path

from .views import MultiUploadView

urlpatterns = [
    path("add-image/<int:location_id>", MultiUploadView.as_view(), name="add-image")
]
