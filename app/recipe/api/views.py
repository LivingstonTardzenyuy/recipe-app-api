from .serializers import RecipeSerializer, RecipeDetailsSerializer, TagSerializer
from recipe.models import Recipe, Tag
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

class RecipeViewSet(viewsets.ModelViewSet):
    """ View for managing recipe APIs """
    serializer_class = RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ Filter the queryset based on the authenticated user """
        return self.queryset.filter(user = self.request.user).order_by('-id')
    
    def post(self):
        """ Overried the creation of a new recipe to belong to the created user """
        
    
    def get_serializer_class(self):
        """ Return the serializer class for request """
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class
    
    
    def perform_create(self, serializer):
        """ Create a new recipe """
        user = self.request.user 
        serializer.save(user=user)
        
        
class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ 
            Filters the queryset to authenticated user
        """
        self.user = self.request.user 
        return self.queryset.filter(user = self.user).order_by("-name")
    
    def perform_create(self, serializer):
        """ Create a new tag """
        serializer.save(user=self.request.user)