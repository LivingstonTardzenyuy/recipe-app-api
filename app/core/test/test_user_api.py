from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status 


CREATE_USER_URL = reverse('core:create')
TOKEN_URL = reverse('core:token')
ME_URL = reverse('core:me')

def create_user(**params):
    """
        Create and return a new user
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ 
        Sets of methods with no authentication
    """
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_user_unauthorized(self):
        """ 
            Test Authentication is required for user 
        """
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
  
  
  
class PrivateUserAPITests(TestCase):
    """
        API requests that required authentication
    """      
    def setUp(self):
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
            name='test Name'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)      # force auth 
        
    def test_retrieve_profile_success(self):
        """ 
            Test retrieving profiel for log in user 
        """
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
        
    def test_post_me_not_allowed(self):
        """ 
            Test post is not allowed for the endpoint.
        """
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_user_profile(self):
        """ 
            Update user profile
        """
        payload = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()    # detecth the change by refreshing our db
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        