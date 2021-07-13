from rest_framework import viewsets, generics
from core.models import *
from recipe import serializers

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
# class RecipeViewSet(generics.ListAPIView):
    """Manage recipes in db"""
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Retrieve recipes"""
        queryset = Recipe.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset