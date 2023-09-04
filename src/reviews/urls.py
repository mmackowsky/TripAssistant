from django.urls import path

from .views import ReviewListView, add_review, get_reviews

urlpatterns = [
    path('reviews/<int:location_id>', get_reviews, name="reviews"),
    path('add_review/<int:location_id>', add_review, name='add-review')
]
