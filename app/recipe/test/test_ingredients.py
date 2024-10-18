from rest_framework.test import APIClient
from django.test import TestCase 
from recipe.models import Recipe, Tag 
from django.urls import reverse
from django.contrib.auth import get_user_model


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
        
    