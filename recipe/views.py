from rest_framework import viewsets, mixins
from core.models import *
from recipe import serializers

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in db"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve all recipes"""
        return self.queryset.all()