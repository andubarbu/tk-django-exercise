from django.db.models.query import QuerySet
from rest_framework import serializers
from core.models import *
from rest_framework.fields import SerializerMethodField


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize an ingredient"""
    class Meta:
        model = Ingredient
        fields = ('name')


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""

    ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id', 'ingredients')