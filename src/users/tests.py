from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile
from .views import save_to_s3


class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_signup_view(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'xyz')

        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_save_to_s3(self):
        file_content = b"Test file content"
        uploaded_file = SimpleUploadedFile("test_file.txt", file_content)

        with self.subTest():
            try:
                save_to_s3(uploaded_file)
            except Exception as e:
                self.fail(f"save_to_s3 raised an exception: {str(e)}")

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_reset_password_view(self):
        response = self.client.get(reverse("password-reset"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("password-reset"), {"email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 302)
