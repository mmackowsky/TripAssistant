import logging
from typing import Any, Dict, List, Tuple

import requests
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView

from .forms import SearchForm
from .models import Location


class LocationListView(ListView):
    model = Location
    context_object_name = "locations"
    template_name = "home.html"
    paginate_by = 6
    ordering = ["location_name"]

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
        api_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=50&key={settings.NOMINATIM_API_KEY}"
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

    def _extract_form_data(self, form: SearchForm) -> Tuple[str, str]:
        location_name = form.cleaned_data.get("location_name")
        place_type = form.cleaned_data.get("place_type")
        return location_name, place_type

    def get_queryset(self) -> QuerySet[Location]:
        queryset = super().get_queryset()
        form = SearchForm(self.request.POST)
        if form.is_valid():
            logging.debug("Filtering results.")
            location_name, place_type = self._extract_form_data(form)
            queryset = Location.objects.filter(
                Q(city__icontains=location_name) & Q(place_type=place_type)
            )

            if not queryset.exists():
                self.fetch_and_save_from_api(place_type, location_name)
                queryset = Location.objects.filter(
                    Q(city__icontains=location_name) & Q(place_type=place_type)
                )

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(
            initial={
                "location_name": self.request.session.get("location_name", ""),
                "place_type": self.request.session.get("place_type", ""),
            }
        )
        return context

    def post(self, request, *args: Any, **kwargs: Any):
        form = SearchForm(self.request.POST)
        if form.is_valid():
            queryset = self.get_queryset()
            if not queryset:
                logging.warning("Places not found")
                messages.warning(self.request, "Places not found.")

            location_name, place_type = self._extract_form_data(form)
            paginator = Paginator(queryset, self.paginate_by)
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            logging.debug(f"Rendering results for {location_name}, {place_type}")
            return render(
                self.request,
                "home.html",
                {
                    "form": form,
                    "locations": page_obj,
                    "location_name": location_name,
                    "place_type": place_type,
                },
            )

        return render(self.request, "home.html", {"form": form})
