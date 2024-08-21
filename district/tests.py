from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import District_School_Registration, DistrictAdminProfile

class CreateDistrictAdminProfileTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword', is_superuser=True
        )
        self.client.login(username='testuser', password='testpassword')
        self.district_school = District_School_Registration.objects.create(
            # Add necessary fields
        )

    def test_create_district_admin_profile(self):
        response = self.client.post(
            reverse('create_districtAdmin_profile', args=[self.user.id]),
            {'field1': 'value1', 'field2': 'value2'}  # Add necessary form data
        )
        self.assertEqual(response.status_code, 302)
        profile = DistrictAdminProfile.objects.get(user=self.user)
        self.assertIn(self.district_school, profile.district_schools.all())
