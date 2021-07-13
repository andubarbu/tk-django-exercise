from django.db.models.query import QuerySet
from rest_framework import serializers
from core.models import *
from rest_framework.fields import SerializerMethodField


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize an ingredient"""

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerializer(source='ingredient_set', many=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, data):
        ingredients_data = data.pop('ingredient_set')
        recipe = Recipe.objects.create(**data)
        for i in ingredients_data:
            Ingredient.objects.create(**i, recipe=recipe)
        return recipe

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        ingredients_data = data.pop('ingredient_set')
        if ingredients_data:
            Ingredient.objects.filter(recipe=instance).delete()
            for i in ingredients_data:
                Ingredient.objects.create(**i, recipe=instance)
        instance.save()
        return instance
            