from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from .models import Recipe
from recipe.api.serializers import RecipeSerializer, RecipeDetailsSerializer
# Create your tests here.


RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """ Create and return a recipe detail URL """
    return reverse('recipe:recipe-detail', args=[recipe_id])
    
    
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
        
        
    def test_recipe_details(self):
        """ Test and get detail recipe """
        recipe = Recipe.objects.create(
            title="Buy a louf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            link = "https://www.example.com/bread",
            user = self.user1
        )
        
        response = self.client.get(detail_url(recipe.id))  
        serializer = RecipeDetailsSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        

    def test_create_recipe(self):
        """ Test for creating a new recipe """
        payload = {
            "title": "Buy a loaf of bread",
            "time_minutes": 5,
            "price": Decimal('4.5'),
            "description": "Buy 2 loaves of bread, cut into 8 slices",
            "link": "https://www.example.com/bread",            
        }
        
        # response = self.client.post(detial_url(recipe.id), payload=payload)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(RECIPES_URL, payload) # /api/recipes/recipe
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = response.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user1)