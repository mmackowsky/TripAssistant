from django.test import TestCase, tag
from django.urls import reverse

from .factories import LocationFactory, ReviewsFactory, UserFactory
from .models import Location, Reviews


class ReviewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.location = LocationFactory()
        self.location_1 = LocationFactory()
        self.location_2 = LocationFactory()
        self.review = ReviewsFactory(user=self.user.profile, location=self.location)
        self.review_1 = ReviewsFactory(
            user=self.user_1.profile, location=self.location_1
        )
        self.review_2 = ReviewsFactory(
            user=self.user_2.profile, location=self.location_2
        )

    def test_get_reviews_view(self):
        url = reverse("reviews", args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.location_name)
        self.assertContains(response, self.review.content)

    def test_add_review_view(self):
        print(Location.objects.all())
        self.client.force_login(self.user_1)
        url = reverse("add-review", args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "content": "New Test Review Content",
                "stars": 4.0,
                "user": self.user,
                "location": self.location,
            },
        )
        obj = Reviews.objects.last()
        self.assertEqual(obj.stars, 4.0)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Reviews.objects.filter(content="New Test Review Content").exists()
        )

    def test_review_delete_view(self):
        self.client.force_login(self.user_1)
        url = reverse("reviews", args=[self.review_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reviews.objects.filter(id=self.review_1.id).exists())

    def test_review_update_view(self):
        self.client.force_login(self.user)
        url = reverse("edit-review", args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {"content": "New Test Edit", "stars": 3.0})
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.content, "New Test Edit")
