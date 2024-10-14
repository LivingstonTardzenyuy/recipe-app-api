from rest_framework import serializers
from recipe.models import Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for Recipe """
    class Meta:
        model = Recipe 
        fields = ["id", "title", "time_minutes", "price", "link"] 
        read_only_fields = ['id']
        
        
class RecipeDetailsSerializer(RecipeSerializer):
    """ Serializers for recipe detail view. We are inheriting from RecipeSerializer sine we will use all it's properties """
    
    class Meta(RecipeSerializer.Meta):
        model = Recipe 
        fields = RecipeSerializer.Meta.fields + ['description']
        
class TagSerializer(serializers.ModelSerializer):
    """ 
        Serializers for Tag
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']