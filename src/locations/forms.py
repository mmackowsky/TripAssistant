from django import forms

from .models import Location


class SearchForm(forms.Form):
    place_type = forms.CharField(label="place_type", max_length=100, required=True)
    location_name = forms.CharField(
        label="location_name", max_length=100, required=True
    )

    class Meta:
        model = Location()
        fields = ["place_type", "location_name"]
