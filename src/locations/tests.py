from django.test import TestCase
from django.urls import reverse

from .factories import LocationFactory


class LocationListViewTestCase(TestCase):
    def setUp(self):
        self.location = LocationFactory()
        self.url = reverse("home")
        self.locations = LocationFactory.create_batch(size=6)

    def test_location_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "home.html")

    def test_location_list_view_with_valid_form_data(self):
        form_data = {"location_name": "Example City", "place_type": "Restaurant"}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_location_list_view_with_invalid_form_data(self):
        form_data = {"location_name": "", "place_type": ""}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_location_list_view_with_no_results(self):
        form_data = {
            "location_name": "Nonexistent City",
            "place_type": "Nonexistent Type",
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_location_list_view_with_results(self):
        form_data = {
            "location_name": self.location.city,
            "place_type": self.location.place_type,
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_location_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(len(self.locations), 6)
