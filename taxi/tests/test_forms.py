from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsDriverTests(TestCase):

    def test_driver_creation_form(self):
        form_data = {
            "username": "username",
            "password1": "23232lll",
            "password2": "23232lll",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "FVG45432",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
