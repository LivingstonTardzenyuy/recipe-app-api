from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status 


CREATE_USER_URL = reverse('core:create')
TOKEN_URL = reverse('core:token')

def create_user(**params):
    """
        Create and return a new user
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    # def test_create_user_success(self):
    #     payload = {
    #         'email': 'test@example.com',
    #         'password': 'test123',
    #         'name': 'Test User'
    #     }
    #     response = self.client.post(CREATE_USER_URL,payload)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     user = get_user_model().objects.get(email = payload['email'])
        # self.assertTrue(user.check_password(payload['password']))
        
    
    def test_user_with_email_exists_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_password_too_short_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'te',
            'name': 'Test User'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)
        
    def test_create_token_for_user(self):
        user_details = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User'
        }
        
        create_user(**user_details)
        payload = {
            "email": user_details['email'],
            "password": user_details['password'],
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEual(response.status_code, HTTP_200_OK)
        
    def test_create_token_with_invalid_credentials(self):
        user_details = {
            "email": "user@example.com",
            "password": "test123",
            "name": "Test User"
        }
        
        create_user(**user_details)
        payload = {
            "email": user_details['email'],
            "password": "wrong_password",
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        
    def test_create_token_blank_password(self):
        user_details = {
            "email": "user@example.com",
            "password": "",
            "name": "Test User"
        }
        
        create_user(**user_details)
        payload = {
            "email": user_details['email'],
            "password": user_details['password'],
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)