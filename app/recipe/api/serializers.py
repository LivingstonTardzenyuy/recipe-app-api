from rest_framework import serializers
from recipe.models import Recipe, Tag, Ingredients



class TagSerializer(serializers.ModelSerializer):
    """ 
        Serializers for Tag
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ["id", "name"]
        read_only_field = ["id"]

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for Recipe """
    tag = TagSerializer(many=True, required=False)
  
    class Meta:
        model = Recipe 
        fields = ["id", "title", "time_minutes", "price", "link", "tag"] 
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """ Create a recipe """
        tags_data = validated_data.pop('tags', [])  # Remove tags from validated data
        validated_data['user'] = self.context['request'].user  # Add user to validated data
        recipe = Recipe.objects.create(**validated_data)  # Now just pass validated_data
        for tag_data in tags_data:
            tag_obj, created = Tag.objects.get_or_create(
                user=self.context['request'].user,
                name=tag_data['name']  # Ensure only the name is passed
            )
            recipe.tags.add(tag_obj)
        return recipe
    
    # def update(self, instance, validated_data):
    #     tags_data = validated_data.pop('tags', None)
        
    #     # Update other fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     # Update tags if they exist
    #     if tags_data is not None:
    #         instance.tags.clear()  # Clear existing tags
    #         for tag_data in tags_data:
    #             tag_obj, created = Tag.objects.get_or_create(
    #                 user=self.context['request'].user,
    #                 name=tag_data['name']
    #             )
    #             instance.tags.add(tag_obj)

    #     instance.save()
    #     return instance
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag', None)
    
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        # Update tags if they exist
        if tags_data is not None:
            instance.tag.clear()  # Clear existing tags
            tag_objects = []
            for tag_data in tags_data:
                tag_obj, created = Tag.objects.get_or_create(
                    user=self.context['request'].user,
                    name=tag_data['name']
                )
                instance.tag.add(tag_obj)
            # instance.tags.set(tag_objects)  # Use set() to assign new tags
        instance.save()
        return instance

    
class RecipeDetailsSerializer(RecipeSerializer):
    """ Serializers for recipe detail view. We are inheriting from RecipeSerializer sine we will use all it's properties """
    
    class Meta(RecipeSerializer.Meta):
        model = Recipe 
        fields = RecipeSerializer.Meta.fields + ['description']
        

    