from rest_framework import viewsets
from core.models import *
from recipe import serializers

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in db"""
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Retrieve recipes"""
        queryset = Recipe.objects.all()
        name_filter = self.request.query_params.get('name')
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset