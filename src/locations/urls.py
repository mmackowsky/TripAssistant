from django.urls import path

from .views import LocationListView, SearchView

urlpatterns = [
    path(
        "search/<str:location_name>/<str:place_type>",
        LocationListView.as_view(),
        name="search",
    ),
    path("", SearchView.as_view(), name="home"),
]
