from rest_framework.test import APIClient
from django.test import TestCase 
from recipe.models import Recipe, Tag, Ingredients
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipe.api.serializers import IngredientSerializer
from rest_framework import status


INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(email="user@example.com", password="testpass123"):
    """ Create and return user. """
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsApiTests(TestCase):
    """ Test unauthenticated API requests """
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """ Test auth is required for retrieving ingredients """
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
        
               
class IngredientsTest(TestCase):
    def test_create_ingredients(self):
        """ Test creating an ingredient is successful.. """
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='test Name'
        )
        
        ingredients = Ingredient.objects.create(
            user=user,
            name="ingredients"
        )
        
        self.assertEqual(str(ingredients), ingredients.name)
        
class PrivateIngredientsApiTests(TestCase):
    """ Test authenticated API requests """
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_retrieve_ingredients(self):
        """ Test retreiving a list of ingredients """
        Ingredients.objects.create(user = self.user,name="Kale")
        Ingredients.objects.create(user = self.user,name="Vannilla")

        response = self.client.get(INGREDIENTS_URL)
        
        ingredients = Ingredients.objects.all().order_by('-name')
        serializer= IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """ List of ingredients limited to authenticated user. """
        user2 = create_user(email="user2@example.com")
        Ingredients.objects.create(user=user2, name="Salepoint")
        ingredient = Ingredients.objects.create(user= self.user, name="Pepper")
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)
        