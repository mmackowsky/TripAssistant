from typing import List, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from locations.models import Location

from .forms import ReviewForm
from .models import Reviews


def get_stars_average(reviews: List[Reviews]) -> Union[float, str]:
    reviews = reviews.values("stars")
    stars_list = [review["stars"] for review in reviews]
    if not stars_list or sum(stars_list) == 0:
        return "Not rated yet"
    average = round(sum(stars_list) / len(stars_list), 2)
    return average


def get_reviews(request: HttpRequest, location_id: int) -> render:
    location = Location.objects.get(id=location_id)
    reviews = Reviews.objects.filter(location=location)
    average_rating = get_stars_average(reviews)

    paginator = Paginator(reviews, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "reviews/reviews.html",
        {
            "location_id": location_id,
            "reviews": page_obj,
            "page_number": page_number,
            "location_name": location.location_name,
            "average_rating": average_rating,
        },
    )


@login_required()
def add_review(request: HttpRequest, location_id: int) -> render:
    location = Location.objects.get(id=location_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            if Reviews.objects.filter(
                user=request.user.profile, location=location
            ).exists():
                messages.error(
                    request, "You have already add review to this place. Thank you!"
                )
                return redirect("reviews", location_id=location_id)
            review = review_form.save(commit=False)
            review.user = request.user.profile
            review.location = location
            review.save()
            messages.info(request, "Review added.")
            return redirect("reviews", location_id=location_id)
    else:
        review_form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {"form": review_form, "location_name": location.location_name},
    )


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reviews
    template_name = "reviews/delete_confirm.html"

    def get_success_url(self) -> str:
        review = self.get_object()
        return "/reviews/{}".format(review.location_id)

    def form_valid(self, form) -> HttpResponseRedirect:
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Review delete successfully!")
        return HttpResponseRedirect(success_url)

    def test_func(self) -> bool:
        review = self.get_object()
        return self.request.user.profile == review.user


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reviews
    template_name = "reviews/add_review.html"
    fields = ["content", "location"]

    def get_success_url(self) -> str:
        review = self.get_object()
        return "/reviews/{}".format(review.location_id)

    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.user.profile = self.request.user.profile
        messages.success(self.request, "Review successfully updated!")
        return super().form_valid(form)

    def test_func(self) -> bool:
        review = self.get_object()
        return self.request.user.profile == review.user
