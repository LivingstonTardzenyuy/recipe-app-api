from .serializers import RecipeSerializer
from recipe.models import Recipe
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()