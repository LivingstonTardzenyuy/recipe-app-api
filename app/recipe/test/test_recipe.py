from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from recipe.models import Recipe, Tag
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
        
        
        
    
    def test_partial_update(self):
        """ Partial update of a recipe """
        original_link = 'https://exmaple.com/recipe.pdf'
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1
        )
        
        payload = {
            'title': 'new reicpe title',
        }
        response = self.client.patch(detail_url(recipe.id), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.user, self.user1)
        
        
    def test_full_update(self):
        """ Test full update of Recipe """
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1,
            link = 'https://exmaple.com/recipe.pdf'
        )
        
        payload = {
            'title': 'new reicpe title',
            'time_minutes': 10,
            'price': Decimal('5.5'),
            'description': 'New reicpe title',
            'link': 'https://new.example.com/recipe.pdf',
        }
        
        response = self.client.put(detail_url(recipe.id), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user1)
        self.assertEqual(recipe.title, payload['title'])
       
        
        
    def delete_recipe(self):
        """ Test deleting a recipe successful """
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1,
        )
        
        response = self.client.delete(detail_url(recipe.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
        
        
    def test_recipe_other_users_recipe_error(self):
        """ 
            Test trying to delete another users recipe gives error.
            Not in our setUp method we are authenticating user1. So let's user2 create recipe
        """
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user2,
        )
        
        response = self.client.delete(detail_url(recipe.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
        
        
    # def test_create_recipe_with_new_tag(self):
    #     """ Test creating recipe with new tag """
    #     payload = {
    #         'title': 'thia prawn curry',
    #         'time_minutes': 30,
    #         'price': Decimal('6.5'),
    #         'link': 'https://example.com/prawn-curry',
    #         'tags': [
    #                 {'name': 'Thia'},
    #                 {'name': 'Dinner'}
    #                 ]
    #             }
    #     response = self.client.post(RECIPES_URL, payload, format='json')
    #     # print(response.body)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     recipes = Recipe.objects.filter(user=self.user)
    #     self.assertEqual(recipes.count(), 1)
    #     recipe = recipes[0]
    #     self.assertEqual(recipe.tags.count(), 2)
    #     for tag in payload['tags']:
    #         exists = recipe.tags.filter(
    #             name=tag['name'],
    #             user=self.user
    #         ).exists()
    #         self.assertTrue(exists)
        
    # def test_create_recipe_with_existing_tag(self):
    #     """ Test creating recipe with existing tag """
    #     tag = Tag.objects.create(name='tag', user=self.user1)
    #     payload = {
    #         'title': 'thia prawn curry',
    #         'time_minutes': 30,
    #         'price': Decimal('6.5'),
    #         'link': 'https://example.com/prawn-curry',
    #         'tags': [
    #             {'name':'tag'},
    #             {'name': 'Breakfast'}
    #             ]
    #     }
    #     response = self.client.post(RECIPES_URL, payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     recipes = Recipe.objects.filter(user = self.user1)
    #     self.assertEqual(recipes.count(), 1)
    #     recipe = recipes[0]
    #     self.assertEqual(recipes.tags.count(), 2)
    #     self.assertIn(tag, recipe.tags.all())
        
    #     for tag in payload['tags']:
    #         exists = recipe.tags.filter(
    #             name=tag['name'],
    #             user=self.user
    #         ).exists()
    #         self.assertTrue(exists)
    
    
    def test_create_tag_on_update(self):
        """ Test creating tag when updting a recipe """
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1,
        )
        
        payload = {'tags': [{'name': 'Launch'}]}
        url = detail_url(recipe.id) 
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_update_recipe_assign_tag(self):
        """ Test assigning an existing tag when updating a recipe."""
        tag_breakfast = Tag.objects.create(
            user=self.user1,
            name="breakfast"
        )
        
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1,
        )
        recipe.tag.add(tag_breakfast)
        tag_launch = Tag.objects.create(
            user = self.user1, name="Launch"
        )
        payload = {
            'tag': [{'name': 'Launch'}]
        }
        url = detail_url(recipe.id)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(tag_launch, recipe.tag.all())
        
        
    def test_clear_recipe_tags(self):
        """ Test clearing a recipes tags. """
        tag = Tag.objects.create(
            user=self.user1,
            name="tag"
        )
        recipe = Recipe.objects.create(
            title="Buy a loaf of bread",
            time_minutes = 5,
            price = Decimal(4.5),
            description = "Buy 2 loaves of bread, cut into 8 slices",
            user = self.user1,
        )
        recipe.tag.add(tag)
        
        payload = {"tag": []}
        url = detail_url(recipe.id)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tag.count(), 0)