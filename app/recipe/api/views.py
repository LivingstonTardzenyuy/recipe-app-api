from .serializers import RecipeSerializer
from recipe.models import Recipe
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RecipeViewSet(viewsets.ModelViewSet):
    """ View for maanaging recipe APIs """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ Filter the queryset based on the authenticated user """
        return self.queryset.filter(user = self.request.user).order_by('-id')