import logging
from typing import Any, Dict, List, Optional, Tuple

import requests
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.views.generic.list import ListView

from .forms import SearchForm
from .models import Location


class SearchView(FormView):
    model = Location
    context_object_name = "locations"
    form_class = SearchForm
    template_name = "home.html"

    def __parse_response_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_data = []
        for item in data:
            try:
                parsed_item = {
                    "location_name": item["name"],
                    "place_type": item["type"],
                    "city": item["address"].get("city") or item["address"].get("town"),
                    "street": item["address"]["road"],
                    "postcode": item["address"]["postcode"],
                }
                parsed_data.append(parsed_item)
            except KeyError as e:
                logging.error(f"{e} while parsing response data.")
                continue
        return parsed_data

    def _get_from_api(
        self, place_type: str, location_name: str
    ) -> List[Dict[str, Any]]:
        query = f"{place_type} near {location_name}"
        api_url = f"{settings.NOMINATIM_URL}/search?q={query}&format=json&addressdetails=1&limit=50&key={settings.NOMINATIM_API_KEY}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            return []

    def fetch_and_save_from_api(self, place_type: str, location_name: str) -> None:
        data = self._get_from_api(place_type, location_name)
        parsed_data = self.__parse_response_data(data)
        self.__save_to_db(parsed_data)

    def __save_to_db(self, data: List[Dict[str, Any]]) -> None:
        Location.objects.bulk_create([Location(**item) for item in data])

    def extract_form_data(self, form: SearchForm) -> Tuple[str, str]:
        location_name = form.cleaned_data.get("location_name").capitalize()
        place_type = form.cleaned_data.get("place_type").lower()
        return location_name, place_type

    def post(self, request, *args, **kwargs):
        form = SearchForm(self.request.POST)
        if form.is_valid():
            location_name, place_type = self.extract_form_data(form)

            return redirect(
                "search", location_name=location_name, place_type=place_type
            )

        messages.warning(
            request,
            "Before search, you have to write name and type of places that you're looking for.",
        )
        return render(request, self.template_name, {"form": form})


class LocationListView(ListView, SearchView):
    model = Location
    context_object_name = "locations"
    template_name = "home.html"

    def get_queryset(self, location_name=None, place_type=None):
        queryset = super().get_queryset()

        if location_name and place_type:
            queryset = Location.objects.filter(
                Q(city__icontains=location_name) & Q(place_type=place_type)
            )

            if not queryset.exists():
                SearchView().fetch_and_save_from_api(place_type, location_name)
                queryset = Location.objects.filter(
                    Q(city__icontains=location_name) & Q(place_type=place_type)
                )

        return queryset

    def __calculate_paginate_by(self, screen: int | str):
        """
        Return number of elements in pagination based on current screen width.
        """
        try:
            screen = int(screen)
            if screen < 1499:
                return 4
        except (TypeError, ValueError):
            return 6
        return 6

    def get(
        self,
        request,
        location_name: Optional[str] = None,
        place_type: Optional[str] = None,
    ):
        queryset = self.get_queryset(location_name, place_type)
        screen = request.GET.get("screen_width")

        paginator = Paginator(queryset, self.__calculate_paginate_by(screen))
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "form": SearchForm(
                initial={
                    "location_name": location_name,
                    "place_type": place_type,
                }
            ),
            "screen_width": screen,
            "locations": page_obj,
            "location_name": location_name,
            "place_type": place_type,
        }

        return render(self.request, self.template_name, context)
