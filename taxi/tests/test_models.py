from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Honda")
        car = Car.objects.create(model="Honda", manufacturer_id=manufacturer.pk)

        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="danchik",
            password="1231244fff",
            first_name="Danylo",
            last_name="Kriuchock"
        )

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Honda")

        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_create_driver_with_license_number(self):
        username = "test username"
        password = "test password"
        license_number = "test license"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
