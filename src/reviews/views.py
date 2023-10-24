import logging
from typing import List, Union

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from locations.models import Location

from .forms import ReviewForm
from .models import Reviews


class ReviewsListView(View):
    def get(self, request: HttpRequest, location_id: int) -> HttpResponse:
        location = Location.objects.get(id=location_id)
        reviews = Reviews.objects.filter(location=location)
        average_rating = self.get_stars_average(reviews)
        logging.debug(f"Filtering reviews by {location} id.")

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

    def get_stars_average(self, reviews: List[Reviews]) -> Union[float, str]:
        reviews = reviews.values("stars")
        stars_list = [review["stars"] for review in reviews]
        if not stars_list or sum(stars_list) == 0:
            return "Not rated yet"
        average = round(sum(stars_list) / len(stars_list), 2)
        return average


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Reviews
    form_class = ReviewForm
    template_name = "reviews/add_review.html"

    def get_success_url(self):
        location_id = self.kwargs["location_id"]
        return reverse("reviews", args=[location_id])

    def form_valid(self, form):
        location_id = self.kwargs["location_id"]
        location = Location.objects.get(id=location_id)
        form.instance.user = self.request.user.profile
        form.instance.location = location

        if Reviews.objects.filter(
            user=self.request.user.profile, location=location
        ).exists():
            messages.error(
                self.request,
                "You have already added a review to this place. Thank you!",
            )
            return redirect("reviews", location_id=location_id)

        messages.info(self.request, "Review added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.kwargs["location_id"]
        location = Location.objects.get(id=location_id)
        context["location_name"] = location.location_name
        return context

    def form_invalid(self, form) -> None:
        location_id = self.kwargs["location_id"]
        location = Location.objects.get(id=location_id)

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        context = self.get_context_data()
        context['form'] = form
        context['location_name'] = location.location_name
        return self.render_to_response(context)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Jeśli użytkownik nie jest zalogowany, przechowaj bieżący URL w sesji
            self.request.session['next'] = self.request.get_full_path()
            return redirect('login')
        return super().handle_no_permission()


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

    def form_invalid(self, form) -> None:
        logging.error(form.errors)
        super().form_invalid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Reviews
    template_name = "reviews/edit_review.html"
    form_class = ReviewForm

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user.profile)

    def get_success_url(self) -> str:
        review = self.get_object()
        return "/reviews/{}".format(review.location_id)

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        success_url = self.get_success_url()
        form.instance.user.profile = self.request.user.profile
        form.save()
        messages.success(self.request, "Review successfully updated!")
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        super().form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))
