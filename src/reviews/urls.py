from django.urls import path

from .views import ReviewDeleteView, ReviewUpdateView, add_review, get_reviews

urlpatterns = [
    path("reviews/<int:location_id>", get_reviews, name="reviews"),
    path("reviews/<int:location_id>/create", add_review, name="add-review"),
    path("reviews/<int:pk>/delete", ReviewDeleteView.as_view(), name="delete-review"),
    path("reviews/<int:pk>/edit", ReviewUpdateView.as_view(), name="edit-review"),
]
