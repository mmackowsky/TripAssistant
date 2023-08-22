import json

import requests
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from .forms import SearchForm
from core import settings


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            location_name = form.cleaned_data.get('location_name')
            place_type = form.cleaned_data.get('place_type')
            query = f"{place_type} near {location_name}"
            api_url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=12&key={settings.NOMINATIM_API_KEY}'
            data = requests.get(api_url).json()
            return data
    else:
        form = SearchForm()
    return render(request, 'home.html', {'form': form})



    # def get_query(self, city_name, place_type):
    #     location = self.GEOLOCATOR.geocode(city_name)
    #
    #     if location:
    #         lat = location.latitude
    #         lon = location.longitude
    #         query = f"{place_type} near {lat}, {lon}"
    #         return query, lat, lon
    #     else:
    #         return None
    #
    # def get_places(self, request, radius=5):
    #     if request.method == "GET":
    #         form = PlaceForm(request.GET)
    #         if form.is_valid():
    #             city_name = form.cleaned_data.get('city_name')
    #             place_type = form.cleaned_data.get('place_type')
    #             query, lat, lon = self.get_query(city_name=city_name, place_type=place_type)
    #             try:
    #                 places = self.GEOLOCATOR.geocode(query, exactly_one=False, limit=None)
    #                 if places:
    #                     for place in places:
    #                         place_coords = (place.latitude, place.longitude)
    #                         place_distance = geodesic((lat, lon), place_coords).kilometers
    #                         if place_distance <= radius:
    #                             print(f'{place.address} ({place_distance:.2f} km)')
    #                             return place.address
    #                 else:
    #                     return messages.warning(request, "No nearby places found for the given type.")
    #             except:
    #                 return messages.error(request, "Error: Unable to fetch nearby places.")

