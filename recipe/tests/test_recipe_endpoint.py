from django.test import TestCase
from django.test.testcases import SerializeMixin
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient, Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(**params):
    defaults = {
        'name': 'Sample recipe',
        'description': 'This is a sample recipe',
        'ingredients': [{'name': 'Ingredient 1'},{'name': 'Ingredient 2'}]
    }
    defaults.update(params)
    if defaults['ingredients'] is not None:
        ingredients = defaults.pop('ingredients')
        recipe = Recipe.objects.create(**defaults)
        for i in ingredients:
            Ingredient.objects.create(name=i['name'], recipe=recipe)
        return recipe
    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Retrieving a list of all recipes"""
        sample_recipe()
        sample_recipe(name="Another one")
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_detail(self):
        """Retrieving a specific recipe"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_new_recipe(self):
        """Create a new recipe"""
        payload = {
            'name': 'Sample recipe',
            'description': 'This is a sample recipe',
            'ingredients': [
                {'name': 'ingr1'},
                {'name': 'ingr2'},
            ]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        for idx, val in enumerate(ingredients):
            self.assertEqual(val.name, payload['ingredients'][idx]['name'])

    def test_search_recipe_by_name(self):
        """Search recipe using url parameter for partial word"""
        sample_recipe(name="Pizza")
        sample_recipe(name="Pistachio")
        sample_recipe(name="Choc")
        url = RECIPES_URL + "?name=ch"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for item in res.data:
            self.assertTrue('ch' in item['name'].lower())

    def test_edit_recipe(self):
        """Edit a recipe using patch"""
        recipe = sample_recipe(name="Pizza")
        payload = {
            'name': 'Not pizza'
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Not pizza')

    def test_delete_recipe(self):
        """Delete a recipe"""
        recipe = sample_recipe(name="Pizza")
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.filter(id=recipe.id).count(), 0)
