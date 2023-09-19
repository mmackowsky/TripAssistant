from django.test import TestCase
from django.urls import reverse

from .factories import ImagesFactory, LocationFactory, ProfileFactory, UserFactory
from .models import Images


class MultiUploadViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        if not self.user.profile:
            self.profile = ProfileFactory.create(user=self.user)
        else:
            self.profile = self.user.profile

        self.location = LocationFactory()

    def test_multi_upload_view(self):
        self.client.force_login(self.user)
        image1 = ImagesFactory(location=self.location, uploaded_by=self.profile)
        image2 = ImagesFactory(location=self.location, uploaded_by=self.profile)

        data = {"attachments": [image1.image.path, image2.image.path]}

        response = self.client.post(
            reverse("add-image", args=[self.location.id]), data=data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Images.objects.count(), 2)
