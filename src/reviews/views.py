from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView

from .forms import ReviewForm
from .models import Reviews
from locations.models import Location


class ReviewListView(ListView):
    model = Reviews
    context_object_name = 'reviews'
    template_name = 'reviews/reviews.html'
    # paginate_by = 6


def get_reviews(request, location_id):
    location = Location.objects.get(id=location_id)
    reviews = Reviews.objects.filter(location=location)
    return render(request, 'reviews/reviews.html', {
        'location_id': location_id,
        'reviews': reviews,
        'location_name': location.location_name
    })


@login_required()
def add_review(request, location_id):
    location = Location.objects.get(id=location_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user.profile
            review.location = location
            review.save()
            messages.info(request, "Review added.")
            return redirect('reviews', location_id=location_id)
    else:
        review_form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'form': review_form, 'location_name': location.location_name})
