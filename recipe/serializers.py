from django.db.models.query import QuerySet
from rest_framework import serializers
from core.models import *


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize an ingredient"""

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, data):
        recipe = Recipe.objects.create(**data)
        # if 'ingredients' in data:
        #     ingredients_data = data.pop('ingredients')
        #     for i in ingredients_data:
        #         Ingredient.objects.create(**i, recipe=recipe)
        return recipe

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        if 'ingredients' in data:
            ingredients_data = data.pop('ingredients')
            if ingredients_data:
                Ingredient.objects.filter(recipe=instance).delete()
                for i in ingredients_data:
                    Ingredient.objects.create(**i, recipe=instance)
            instance.save()
        return instance
            