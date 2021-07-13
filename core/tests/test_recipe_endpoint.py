from django.test import TestCase
from django.urls import reverse
from rest_framework import test, status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def sample_recipe(**params):
    defaults = {
        'name': 'Sample recipe',
        'description': 'This is a sample recipe'
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Retrieving a list of recipes"""
        sample_recipe()
        sample_recipe(name='sample recipe 2')
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)