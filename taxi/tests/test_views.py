from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST = reverse("taxi:manufacturers")


class PublicManufacturersList(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_LIST)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturersList(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="user",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Honda")
        Manufacturer.objects.create(name="VAG")

        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURERS_LIST)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturers"]), list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="123sssss"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "username",
            "password1": "23232lll",
            "password2": "23232lll",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "FVG45432",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
