import json
from typing import Any, Dict
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import SearchForm, ReviewForm
from .models import Location, Reviews
from core import settings


class LocationListView(ListView):
    model = Location
    context_object_name = 'locations'
    template_name = 'home.html'
    paginate_by = 6
    ordering = ['location_name']

    def __parse_response_data(self, data):
        parsed_data = []
        try:
            for item in data:
                parsed_item = {
                    'location_name': item['name'],
                    'place_type': item['type'],
                    'city': item['address'].get('city') or item['address'].get('town'),
                    'street': item['address']['road'],
                    'postcode': item['address']['postcode']
                }
                parsed_data.append(parsed_item)
        except KeyError:
            pass

        self.__save_to_db(parsed_data)

    def _get_from_api(self, place_type, location_name):
        query = f"{place_type} near {location_name}"
        api_url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=24&key={settings.NOMINATIM_API_KEY}'
        data = requests.get(api_url).json()
        self.__parse_response_data(data)

    def __save_to_db(self, data):
        Location.objects.bulk_create([
            Location(**item) for item in data
        ])

    def get_queryset(self):
        queryset = Location.objects.all()
        form = SearchForm(self.request.POST)
        if form.is_valid():
            location_name = form.cleaned_data.get('location_name')
            place_type = form.cleaned_data.get('place_type')
            queryset = Location.objects.filter(Q(city__icontains=location_name) & Q(place_type=place_type))

            if not queryset.exists():
                self._get_from_api(place_type, location_name)
                queryset = Location.objects.filter(Q(city__icontains=location_name) & Q(place_type=place_type))

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(initial={
            'location_name': self.request.session.get('location_name', ''),
            'place_type': self.request.session.get('place_type', '')
        })
        return context

    def post(self, request, *args: Any, **kwargs: Any):
        form = SearchForm(self.request.POST)
        if form.is_valid():
            queryset = self.get_queryset()
            if not queryset:
                messages.warning(self.request, 'Places not found.')
            location_name = form.cleaned_data.get('location_name')
            place_type = form.cleaned_data.get('place_type')
            paginator = Paginator(queryset, self.paginate_by)
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(self.request, "home.html", {
                'form': form,
                'locations': page_obj,
                'location_name': location_name,
                'place_type': place_type
            })
        return render(self.request, "home.html", {'form': form})


class ReviewListView(ListView):
    model = Reviews
    context_object_name = 'reviews'
    template_name = 'reviews.html'
    # paginate_by = 6

    def get_reviews(self, request, location_id):
        location = Location.objects.get(id=location_id)
        reviews = Reviews.objects.filter(location=location)
        return render(request, self.template_name, {'location': location, 'reviews': reviews})

    @login_required()
    def add_review(self, request):
        if request.method == "POST":
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                messages.info(request, "Review added.")
                return redirect('place_reviews')
        else:
            review_form = ReviewForm()

        return render(request, 'reviews.html', {'form': review_form})
