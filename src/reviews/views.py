from typing import List, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, UpdateView

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


@login_required
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
            print(review_form.errors)
    else:
        review_form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {"form": review_form, "location_name": location.location_name},
    )


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Reviews
    template_name = "reviews/delete_confirm.html"

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user.profile)

    def get_success_url(self) -> str:
        review = self.get_object()
        return "/reviews/{}".format(review.location_id)

    def form_valid(self, form) -> HttpResponseRedirect:
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Review delete successfully!")
        return HttpResponseRedirect(success_url)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Reviews
    template_name = "reviews/edit_review.html"
    fields = ["content", "stars"]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user.profile)

    def get_success_url(self) -> str:
        review = self.get_object()
        return "/reviews/{}".format(review.location_id)

    def form_valid(self, form):
        success_url = self.get_success_url()
        form.instance.user.profile = self.request.user.profile
        form.save()
        messages.success(self.request, "Review successfully updated!")
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form) -> None:
        print(form.errors)
        super().form_invalid(form)
