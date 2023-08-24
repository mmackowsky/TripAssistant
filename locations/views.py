import json
from typing import Any, Dict
import requests
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.core.paginator import Paginator


from .forms import SearchForm
from .models import Location
from core import settings


class LocationListView(ListView):
    model = Location
    context_object_name = 'locations'
    template_name = 'home.html'
    paginate_by = 6

    def __parse_response_data(self, data):
        parsed_data = []

        for item in data:
            parsed_item = {
                'location_name': item['name'],
                'place_type': item['type'],
                'city': item['address'].get('city') or item['address'].get('town'),
                'street': item['address']['road'],
                'postcode': item['address']['postcode']
            }
            parsed_data.append(parsed_item)

        self.__save_to_db(parsed_data)

    def _get_from_api(self, place_type, location_name):
        query = f"{place_type} near {location_name}"
        api_url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=9&key={settings.NOMINATIM_API_KEY}'
        data = requests.get(api_url).json()
        self.__parse_response_data(data)

    def __save_to_db(self, data):
        Location.objects.bulk_create([
            Location(**item) for item in data
        ])

    def get_queryset(self):
        queryset = Location.objects.all()
        form = SearchForm(self.request.POST or None)
        if form.is_valid():
            location_name = form.cleaned_data.get('location_name')
            place_type = form.cleaned_data.get('place_type')

            if location_name and place_type:
                queryset = queryset.filter(city__icontains=location_name, place_type=place_type)
        return queryset


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            location_name = form.cleaned_data.get('location_name')
            place_type = form.cleaned_data.get('place_type')
            self._get_from_api(place_type, location_name)

            queryset = self.get_queryset()

            # paginator = Paginator(queryset, self.paginate_by)


            return render(request, 'home.html', {'form': form, 'locations': queryset})
        return render(request, 'home.html', {'form': form})


    # @staticmethod
    # def search(request):
    #     if request.method == "POST":
    #         form = SearchForm(request.POST)
    #         if form.is_valid():
    #             location_name = form.cleaned_data.get('location_name')
    #             place_type = form.cleaned_data.get('place_type')
    #             query = f"{place_type} near {location_name}"
    #             api_url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=9&key={settings.NOMINATIM_API_KEY}'
    #             data = requests.get(api_url).json()
    #             parsed_data = parse_response_data(data)
    #             return render(request, 'home.html', {'form': form, 'data': parsed_data})
    #     else:
    #         form = SearchForm()
    #     return render(request, 'home.html', {'form': form})
