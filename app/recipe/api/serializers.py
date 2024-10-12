from rest_framework import serializers
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for Recipe """
    class Meta:
        models = Recipe 
        fields = "__all__" 
        read_only_fields = ['id']