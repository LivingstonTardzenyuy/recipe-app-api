from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from .models import Recipe
from recipe.api.serializers import RecipeSerializer
# Create your tests here.


RECIPES_URL = reverse('recipe:recipe-list')

class PublicRecipeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """ Test auth is required to call API. """
        response = self.client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        


class PrivateRecipeAPITests(TestCase):
    """ Test Authenticated API requests """
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='test Name'
        )
        
        self.user2 = get_user_model().objects.create_user(
            email='test2@example.com',
            password='testpass123',
            name='test Name'
        )
        
        
        self.client.force_authenticate(user = self.user1)
        
    def test_get_recipes(self):
        response = self.client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_recipe_list_limited_to_user(self):
        """ Test list of recipes is limited to authenticated users """
        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user1)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)