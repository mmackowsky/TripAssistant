from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse


# class GoogleAPI:
#     def __init__(self, api_key):
#         self.api_key = api_key
#
#
#     def get_data(self, url, query):
#         response = requests.get(url)
#         data = response.json()

def get_places(request):
    api_key = settings.GOOGLE_API_KEY
    query = ""
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    return JsonResponse(data)
