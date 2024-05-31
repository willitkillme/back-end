from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Child, Allergy

class AllAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.child = Child.objects.create(name='Test Child', parent=self.user)
        self.allergy = Allergy.objects.create(name='Peanut', user=self.user)

    # Test cases for register user
    def test_register_user_with_invalid_data(self):
        data = {'username': '', 'password': 'new_password'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_existing_username(self):
        data = {'username': 'test_user', 'password': 'new_password'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for login user
    def test_login_user_with_invalid_credentials(self):
        data = {'username': 'test_user', 'password': 'wrong_password'}
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test cases for update profile
    def test_update_profile_with_invalid_data(self):
        data = {'first_name': '', 'last_name': 'User'}
        response = self.client.put('/api/profile/update/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for set allergies
    def test_set_allergies_with_invalid_data(self):
        data = {'allergies': 'Peanut'}  # Allergies should be provided as a list
        response = self.client.put('/api/set_allergies/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for check allergies
    def test_check_allergies_with_invalid_barcode(self):
        response = self.client.get('/api/checkAllergies/?barcode=123')  # Invalid barcode
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for set children
    def test_set_children_with_missing_name(self):
        data = {'allergies': [{'name': 'Peanut'}]}  # Missing name field
        response = self.client.post('/api/set-children/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_children_with_invalid_allergies_data(self):
        data = {'name': 'Test Child 2', 'allergies': 'Peanut'}  # Allergies should be provided as a list of objects
        response = self.client.post('/api/set-children/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for set child allergy
    def test_set_child_allergy_with_invalid_child_id(self):
        data = {'allergies': ['Peanut']}
        response = self.client.put('/api/children/9999/set_allergies/', data)  # Invalid child ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
