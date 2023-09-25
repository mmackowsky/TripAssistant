from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .factories import LocationFactory
from .models import Location
from .views import LocationListView


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

    @patch("locations.views.requests.get")
    def test_fetch_and_save_from_api_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "name": "Test Location",
                "type": "Restaurant",
                "address": {
                    "city": "Example City",
                    "road": "Example Street",
                    "postcode": "12345",
                },
            }
        ]
        form_data = {
            "location_name": "Example City",
            "place_type": "Restaurant",
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Location.objects.count(), 1)

    def test_parse_response_data(self):
        input_data = [
            {"name": "Location 1", "type": "Restaurant",
             "address": {"city": "City 1", "road": "Road 1", "postcode": "12345"}},
            {"name": "Location 2", "type": "Cafe",
             "address": {"town": "Town 2", "road": "Road 2", "postcode": "67890"}},
        ]
        expected_output = [
            {"location_name": "Location 1", "place_type": "Restaurant", "city": "City 1", "street": "Road 1",
             "postcode": "12345"},
            {"location_name": "Location 2", "place_type": "Cafe", "city": "Town 2", "street": "Road 2",
             "postcode": "67890"},
        ]
        parsed_data = LocationListView()._LocationListView__parse_response_data(input_data)
        self.assertEqual(parsed_data, expected_output)
