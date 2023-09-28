from django.urls import path

from .views import AddReviewView, ReviewDeleteView, ReviewsListView, ReviewUpdateView

urlpatterns = [
    path("reviews/<int:location_id>", ReviewsListView.as_view(), name="reviews"),
    path(
        "reviews/<int:location_id>/create", AddReviewView.as_view(), name="add-review"
    ),
    path("reviews/<int:pk>/delete", ReviewDeleteView.as_view(), name="delete-review"),
    path("reviews/<int:pk>/edit", ReviewUpdateView.as_view(), name="edit-review"),
]
