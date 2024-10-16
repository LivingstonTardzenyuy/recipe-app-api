from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from recipe.models import Recipe, Tag
from recipe.api.serializers import TagSerializer
# Create your tests here.



TAGS_URL = reverse('recipe:tag-list')

def create_user(email="user@example.com", password="password01@"):
    """ 
        Function for creating a sample user
    """
    return get_user_model().objects.create_user(email, password)


class PublickTagsAPITests(TestCase):
    """ 
        Test aunauthenticated API requests
    """
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """ 
            Test auth is required for retrieving tags
        """
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateTagsAPiTest(TestCase):
    """ 
       Test authenticated API requests. T
    """
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user = self.user)
        
    
    def test_retrieve_tags(self):
        """ 
            Test retrieving a list of tags
        """
        Tag.objects.create(user=self.user, name="tag1")
        Tag.objects.create(user=self.user, name="tag2")
        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    
    def test_create_tag(self):
        """ 
            Test for creating a list of tags
        """
        payload = {
            "name": "tag1",
        }
        
        response = self.client.post(TAGS_URL,payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_tags_limited_to_user(self):
        """ 
            Test list of tags is limited to authenticated users
        """
        user2 = create_user(email="user2@example.com")
        Tag.objects.create(user=user2, name='Fruitly')
        tag = Tag.objects.create(user = self.user, name='Comfort food')
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # self.assertEqual(response[0]['id'], tag.id)
        
        
    def test_update_tag(self):
        """ Test updating a tag."""
        tag = Tag.objects.create(
            user= self.user,
            name="Comfort food"
        )
        
        payload = {
            "name": "Healthy food"
        }
        url = reverse('recipe:tag-detail', args=[tag.id])
        response = self.client.patch(url, payload)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload.get("name"))